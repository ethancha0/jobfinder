import argparse
import csv
import time
from pathlib import Path

import requests


DEFAULT_INPUT = Path(__file__).resolve().parents[1] / "companies.csv"
DEFAULT_CLEANED_OUTPUT = Path(__file__).resolve().parents[1] / "companies.cleaned.csv"
DEFAULT_INVALID_OUTPUT = Path(__file__).resolve().parents[1] / "companies.invalid.csv"

RETRYABLE_STATUSES = {429, 500, 502, 503, 504}


def validate_board_token(
    session: requests.Session,
    board_token: str,
    retries: int,
    timeout: tuple[float, float],
) -> dict:
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"
    last_error = ""

    for attempt in range(retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            if response.status_code == 200:
                return {"kind": "valid", "status": 200, "error": ""}

            if response.status_code in RETRYABLE_STATUSES and attempt < retries:
                time.sleep(0.4 * (2 ** attempt))
                continue

            return {
                "kind": "invalid_status",
                "status": response.status_code,
                "error": "",
            }
        except requests.exceptions.Timeout:
            last_error = "timeout"
            if attempt < retries:
                time.sleep(0.4 * (2 ** attempt))
                continue
        except requests.exceptions.RequestException as exc:
            last_error = str(exc)
            if attempt < retries:
                time.sleep(0.4 * (2 ** attempt))
                continue

        break

    return {"kind": "transient_error", "status": "", "error": last_error}


def clean_csv(
    input_path: Path,
    cleaned_output_path: Path,
    invalid_output_path: Path,
    retries: int,
    timeout: tuple[float, float],
) -> dict:
    valid_rows: list[dict] = []
    invalid_rows: list[dict] = []
    token_cache: dict[str, dict] = {}
    seen_tokens: set[str] = set()
    total_rows = 0

    with input_path.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        headers = set(reader.fieldnames or [])
        required_headers = {"name", "board_token"}
        missing_headers = required_headers - headers
        if missing_headers:
            raise ValueError(
                f"CSV missing required header(s): {', '.join(sorted(missing_headers))}"
            )

        with requests.Session() as session:
            for row in reader:
                total_rows += 1
                name = (row.get("name") or "").strip()
                board_token = (row.get("board_token") or "").strip()

                if not name or not board_token:
                    invalid_rows.append(
                        {
                            "name": name,
                            "board_token": board_token,
                            "reason": "missing_required_fields",
                            "status": "",
                            "error": "",
                        }
                    )
                    continue

                if board_token in seen_tokens:
                    invalid_rows.append(
                        {
                            "name": name,
                            "board_token": board_token,
                            "reason": "duplicate_board_token",
                            "status": "",
                            "error": "",
                        }
                    )
                    continue

                seen_tokens.add(board_token)
                verdict = token_cache.get(board_token)
                if verdict is None:
                    verdict = validate_board_token(
                        session=session,
                        board_token=board_token,
                        retries=retries,
                        timeout=timeout,
                    )
                    token_cache[board_token] = verdict

                if verdict["kind"] == "valid":
                    valid_rows.append({"name": name, "board_token": board_token})
                else:
                    invalid_rows.append(
                        {
                            "name": name,
                            "board_token": board_token,
                            "reason": verdict["kind"],
                            "status": verdict["status"],
                            "error": verdict["error"],
                        }
                    )

    cleaned_output_path.parent.mkdir(parents=True, exist_ok=True)
    invalid_output_path.parent.mkdir(parents=True, exist_ok=True)

    with cleaned_output_path.open("w", newline="", encoding="utf-8") as cleaned_file:
        writer = csv.DictWriter(cleaned_file, fieldnames=["name", "board_token"])
        writer.writeheader()
        writer.writerows(valid_rows)

    with invalid_output_path.open("w", newline="", encoding="utf-8") as invalid_file:
        writer = csv.DictWriter(
            invalid_file,
            fieldnames=["name", "board_token", "reason", "status", "error"],
        )
        writer.writeheader()
        writer.writerows(invalid_rows)

    return {
        "total_rows": total_rows,
        "valid_rows": len(valid_rows),
        "invalid_rows": len(invalid_rows),
        "cleaned_output": str(cleaned_output_path),
        "invalid_output": str(invalid_output_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Greenhouse board tokens and write cleaned CSV output."
    )
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--clean-output", default=str(DEFAULT_CLEANED_OUTPUT))
    parser.add_argument("--invalid-output", default=str(DEFAULT_INVALID_OUTPUT))
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--connect-timeout", type=float, default=5.0)
    parser.add_argument("--read-timeout", type=float, default=20.0)
    args = parser.parse_args()

    summary = clean_csv(
        input_path=Path(args.input),
        cleaned_output_path=Path(args.clean_output),
        invalid_output_path=Path(args.invalid_output),
        retries=max(0, args.retries),
        timeout=(args.connect_timeout, args.read_timeout),
    )

    print(
        "Validation complete: "
        f"total={summary['total_rows']}, "
        f"valid={summary['valid_rows']}, "
        f"invalid={summary['invalid_rows']}"
    )
    print(f"Cleaned CSV: {summary['cleaned_output']}")
    print(f"Invalid CSV: {summary['invalid_output']}")


if __name__ == "__main__":
    main()
