#!/usr/bin/env python3
import warnings
import urllib3

# Suppress SSL warnings globally
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

from core.context import Context

# Discovery
from modules.discovery.http_probe import run as http_discovery
from modules.discovery.dir_search import run as dir_search
from modules.discovery.openapi import run as openapi_discovery

# Vulnerability modules
from modules.vuln.jwt_scan import run as jwt_scan
from modules.vuln.privilege_inference import run as privilege_inference
from modules.vuln.ssrf_scan import run as ssrf_scan
from modules.vuln.openapi_authz import run as openapi_authz

# Reporting
from modules.reporting.markdown import run as report


def main():
    # Initialize context (scope.yaml is loaded internally)
    ctx = Context()

    # -----------------------------
    # DISCOVERY PHASE
    # -----------------------------
    http_discovery(ctx)
    dir_search(ctx)
    openapi_discovery(ctx)

    # -----------------------------
    # VULNERABILITY PHASE
    # -----------------------------
    jwt_scan(ctx)
    privilege_inference(ctx)
    ssrf_scan(ctx)
    openapi_authz(ctx)

    # -----------------------------
    # FINDINGS OUTPUT
    # -----------------------------
    print("\n=== FINDINGS ===")

    findings = ctx.findings

    if not findings:
        print("No confirmed findings.")
    else:
        for f in findings:
            print(f"- [{f.severity}] {f.title}")

    # -----------------------------
    # REPORTING
    # -----------------------------
    report(ctx)


if __name__ == "__main__":
    main()

