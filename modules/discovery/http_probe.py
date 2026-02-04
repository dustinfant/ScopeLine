import requests

TIMEOUT = 5

def run(context):
    context.http_services = []  # 🔒 always initialize here

    for asset in context.assets:
        for scheme in ("http", "https"):
            url = f"{scheme}://{asset}/"

            try:
                r = requests.get(
                    url,
                    headers=context.headers,
                    cookies=context.cookies,
                    timeout=TIMEOUT,
                    allow_redirects=True,
                    verify=False
                )

                if r.status_code < 500:
                    service = {
                        "asset": asset,
                        "url": url,
                        "scheme": scheme,
                        "status": r.status_code,
                        "headers": dict(r.headers),
                    }

                    print(f"[DISCOVERY] {url} ({r.status_code})")
                    context.http_services.append(service)

            except Exception:
                continue

