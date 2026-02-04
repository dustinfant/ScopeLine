import requests

COMMON_OPENAPI_PATHS = [
    "/swagger.json",
    "/v3/api-docs",
    "/openapi.json",
]

TIMEOUT = 5

def run(context):
    context.openapi_endpoints = []

    if not context.http_services:
        print("[AUTHZ] No HTTP services discovered, skipping OpenAPI discovery")
        return

    for svc in context.http_services:
        base = svc["url"].rstrip("/")

        for path in COMMON_OPENAPI_PATHS:
            url = f"{base}{path}"

            try:
                r = requests.get(
                    url,
                    headers=context.headers,
                    cookies=context.cookies,
                    timeout=TIMEOUT,
                    allow_redirects=False,
                    verify=False
                )

                if r.status_code == 200 and "openapi" in r.text.lower():
                    print(f"[OPENAPI] Discovered OpenAPI spec at {url}")

                    context.openapi_endpoints.append({
                        "url": url,
                        "service": base,
                        "auth_required": True,  # conservative default
                    })

            except Exception:
                continue

