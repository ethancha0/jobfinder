# Server Data Seeding

## Validate Greenhouse board tokens

From the `server` directory:

```bash
python3 scripts/validate_companies_csv.py
```

This generates:

- `companies.cleaned.csv`: valid `name,board_token` rows only
- `companies.invalid.csv`: excluded rows with `reason`, `status`, and `error`

## Validate and seed in one flow

From the `server` directory:

```bash
python3 scripts/validate_companies_csv.py && python3 -m db.seed
```

`db.seed` will prefer `companies.cleaned.csv` when it exists, and fall back to `companies.csv` otherwise.
