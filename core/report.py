def write_report(context, path="report.md"):
    findings = context.findings.all()

    with open(path, "w") as f:
        f.write("# Pentest Report\n\n")

        if not findings:
            f.write("No confirmed findings.\n")
            return

        for finding in findings:
            f.write(f"## {finding['title']}\n")
            f.write(f"- Target: {finding.get('target')}\n")
            f.write(f"- Technique: {finding.get('technique')}\n")
            f.write(f"- Confidence: **{finding.get('confidence')}**\n")
            f.write(f"- Evidence Count: {finding.get('evidence_count')}\n\n")

            f.write("### Evidence\n")
            for ev in finding.get("evidence", []):
                f.write(
                    f"- [{ev.get('identity')}] "
                    f"{ev.get('module')}: {ev.get('detail')}\n"
                )

            f.write("\n")

