def extract_roles(jwt_payload):
    roles = set()

    common_keys = [
        "role", "roles",
        "groups", "group",
        "scope", "scopes",
        "permissions", "perms",
        "authorities"
    ]

    for key in common_keys:
        value = jwt_payload.get(key)
        if isinstance(value, str):
            roles.update(value.split())
        elif isinstance(value, list):
            roles.update(value)

    return list(roles)


def run(context):
    findings = []

    jwt_payload = context.evidence.get("jwt_payload")
    if not jwt_payload:
        print("[PRIV] No JWT payload available, skipping privilege inference")
        return findings

    roles = extract_roles(jwt_payload)

    if roles:
        findings.append({
            "type": "privilege_inference",
            "issue": "Roles or scopes exposed in JWT",
            "severity": "Info",
            "impact": "Token reveals authorization model",
            "details": roles
        })
        print(f"[PRIV] Roles inferred from JWT: {roles}")
    else:
        print("[PRIV] No explicit roles found in JWT")

    # ---- Response-based privilege inference ----
    sensitive_paths = [
        "/admin",
        "/api/admin",
        "/api/users",
        "/api/internal",
        "/management",
        "/actuator"
    ]

    for service in context.services:
        base = service["url"].rstrip("/")
        for path in sensitive_paths:
            url = base + path
            response = context.http_get(url)

            if not response:
                continue

            status = response["status"]

            if status == 403:
                findings.append({
                    "type": "privilege_inference",
                    "issue": "Access denied to privileged endpoint",
                    "severity": "Low",
                    "impact": "Endpoint exists but requires elevated role",
                    "details": url
                })
                print(f"[PRIV] 403 indicates privileged endpoint: {url}")

            if status == 200:
                findings.append({
                    "type": "privilege_inference",
                    "issue": "Privileged endpoint accessible",
                    "severity": "High",
                    "impact": "Possible over-privileged token",
                    "details": url
                })
                print(f"[PRIV] 🚨 Privileged endpoint accessible: {url}")

    context.findings.extend(findings)
    return findings

