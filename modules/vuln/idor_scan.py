def run(context):
    if not hasattr(context, "http_services") or not context.http_services:
        print("[IDOR] No HTTP services discovered, skipping")
        return

    for svc in context.http_services:  # ✅ standardized
        base = svc["url"].rstrip("/")

        # Example placeholder for object ID scanning
        test_paths = ["/user/1", "/user/2"]
        for path in test_paths:
            url = base + path
            try:
                resp = context.http_get(url)
                if not resp:
                    continue

                status = resp.get("status", 0)
                if status == 200:
                    context.findings.append({
                        "type": "idor",
                        "issue": "Insecure Direct Object Reference",
                        "severity": "High",
                        "impact": "Unauthorized access to object",
                        "details": {
                            "url": url,
                            "status": status
                        }
                    })
                    print(f"[IDOR] 🚨 IDOR detected: {url}")

            except Exception:
                continue

