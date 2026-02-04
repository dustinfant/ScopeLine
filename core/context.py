# core/context.py

import yaml


class Context:
    def __init__(self, scope_file=None):
        # Scope
        self.assets = []

        # Discovery
        self.http_services = []
        self.openapi_endpoints = []

        # Auth
        self.headers = {}
        self.cookies = {}

        # Identity / evidence
        self.identity = None
        self.evidence = {}

        # Findings
        self.findings = []

        # Options
        self.verify_ssl = False

        if scope_file:
            self.load_scope(scope_file)

    def load_scope(self, scope_file):
        with open(scope_file, "r") as f:
            data = yaml.safe_load(f) or {}

        # ---- Scope ----
        self.assets = data.get("scope", {}).get("assets", [])

        # ---- Auth ----
        auth = data.get("auth", {})
        self.headers = auth.get("headers", {}) or {}
        self.cookies = auth.get("cookies", {}) or {}

        # ---- Options ----
        opts = data.get("options", {})
        self.verify_ssl = bool(opts.get("verify_ssl", False))

        print(f"[SCOPE] Loaded {len(self.assets)} assets from {scope_file}")

