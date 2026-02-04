def run(context):
    if not context.findings:
        return

    issues = [f.get("issue", "").lower() for f in context.findings]

    # ---- IDOR → Account Takeover ----
    if "insecure direct object reference" in issues:
        context.add_finding({
            "issue": "Attack Path: IDOR → Account Takeover",
            "severity": "Critical",
            "confidence": "Medium",
            "detail": {
                "path": [
                    "Access unauthorized object via IDOR",
                    "Enumerate sensitive data",
                    "Impersonate higher-privileged user"
                ]
            }
        })

    # ---- SSRF → Cloud Metadata ----
    if "confirmed ssrf" in issues:
        context.add_finding({
            "issue": "Attack Path: SSRF → Cloud Metadata → Credential Theft",
            "severity": "Critical",
            "confidence": "High",
            "detail": {
                "path": [
                    "Trigger SSRF via user-controlled parameter",
                    "Access cloud metadata service",
                    "Extract temporary credentials",
                    "Pivot to cloud control plane"
                ]
            }
        })

    # ---- Combined Path ----
    if (
        "insecure direct object reference" in issues and
        "confirmed ssrf" in issues
    ):
        context.add_finding({
            "issue": "Attack Path: IDOR → SSRF → Full Environment Compromise",
            "severity": "Critical",
            "confidence": "High",
            "detail": {
                "path": [
                    "Exploit IDOR as low-privileged user",
                    "Reach SSRF-capable endpoint",
                    "Extract cloud credentials",
                    "Achieve persistent administrative access"
                ]
            }
        })

