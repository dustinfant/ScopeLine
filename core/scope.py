import yaml


def load_scope(path="scope.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def apply_scope(context, scope_data):
    # Assets
    context.assets = scope_data.get("scope", {}).get("assets", [])

    # Auth
    auth = scope_data.get("auth", {})
    context.headers = auth.get("headers", {}) or {}
    context.cookies = auth.get("cookies", {}) or {}

    # Options
    opts = scope_data.get("options", {})
    context.verify_ssl = bool(opts.get("verify_ssl", False))

