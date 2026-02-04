# modules/discovery/dir_search.py

import requests

COMMON_DIRS = [
    "admin",
    "login",
    "dashboard",
    "api",
    "internal",
    ".git",
    ".env",
]

def run(context):
    if not context.http_services:
        print("[DIR] No HTTP services discovered, skipping")
        return

    for svc in context.http_services:
        base_url = svc.get("url", "").rstrip("/")
        if not base_url:
            continue

        for d in COMMON_DIRS:
            url = f"{base_url}/{d}"

            try:
                r = requests.get(
                    url,
                    headers=context.headers,
                    cookies=context.cookies,
                    timeout=5,
                    verify=context.verify_ssl,
                    allow_redirects=False,
                )
            except Exception:
                continue

            if r.status_code in (200, 301, 302, 401, 403):
                print(f"[DIR] {url} ({r.status_code})")

                finding = {
                    "title": "Exposed Directory or Endpoint",
                    "severity": "Medium",
                    "risk": 5.0,
                    "asset": base_url,
                    "evidence": {
                        "url": url,
                        "status": r.status_code,
                    },
                    "type": "directory_discovery",
                }

                # ---- De-duplication ----
                if finding not in context.findings:
                    context.findings.append(finding)

