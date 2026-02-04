from core.mitre import technique

def run(context):
    if not context.openapi_endpoints:
        print("[AUTHZ] No OpenAPI endpoints available, skipping")
        return

    if not context.identities:
        print("[AUTHZ] No identities available, skipping")
        return

    for identity in context.identities:
        print(f"[AUTHZ] Testing OpenAPI access as {identity['name']}")

        for ep in context.openapi_endpoints:
            # Placeholder logic — this is where real authz testing will expand
            if ep.get("auth_required") and identity.get("role") != "admin":
                context.add_finding({
                    "title": "Potential Broken Object Level Authorization",
                    "severity": "High",
                    "url": ep.get("url"),
                    "evidence": f"Accessible as role: {identity.get('role')}",
                    "mitre": technique("T1190"),
                    "risk": 8.5
                })

