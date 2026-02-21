const DEFAULT_DEV_API_BASE_URL = "http://localhost:8000";
const DEFAULT_PROD_API_BASE_URL = "https://jobfinder-h8b6.onrender.com";

function stripTrailingSlashes(url: string) {
  return url.replace(/\/+$/, "");
}

export function getApiBaseUrl() {
  const configured = process.env.NEXT_PUBLIC_API_URL?.trim();
  if (configured) return stripTrailingSlashes(configured);

  if (process.env.NODE_ENV !== "production") return DEFAULT_DEV_API_BASE_URL;
  return DEFAULT_PROD_API_BASE_URL;
}

