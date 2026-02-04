class ContextSchemaError(Exception):
    pass


REQUIRED_FIELDS = {
    "assets": list,
    "http_services": list,
    "openapi_endpoints": list,
    "identities": list,
    "findings": list,
    "evidence": dict,
}


def validate_context(context):
    missing = []
    wrong_type = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if not hasattr(context, field):
            missing.append(field)
            continue

        value = getattr(context, field)
        if not isinstance(value, expected_type):
            wrong_type.append(
                f"{field} (expected {expected_type.__name__}, got {type(value).__name__})"
            )

    if missing or wrong_type:
        msg = ["Context schema validation failed:"]

        if missing:
            msg.append(f"- Missing fields: {', '.join(missing)}")

        if wrong_type:
            msg.append("- Type errors:")
            for e in wrong_type:
                msg.append(f"  - {e}")

        raise ContextSchemaError("\n".join(msg))

