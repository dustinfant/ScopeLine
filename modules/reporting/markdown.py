def run(context):
    with open("report.md", "w") as f:
        f.write("# Pentest Report\n\n")

        if not context.findings:
            f.write("No confirmed findings.\n")
            print("[REPORT] Written to report.md")
            return

        for finding in context.findings:
            f.write(f"## {finding['title']}\n")
            f.write(f"- Severity: {finding['severity']}\n")
            f.write(f"- URL: {finding['url']}\n")
            f.write(f"- Evidence: {finding['evidence']}\n")

            if finding.get("mitre"):
                f.write(
                    f"- MITRE: {finding['mitre'].get('id')} "
                    f"({finding['mitre'].get('name')})\n"
                )

            f.write("\n")

    print("[REPORT] Written to report.md")

