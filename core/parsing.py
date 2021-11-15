def parse_boolean(value):
    if isinstance(value, str):
        if value.lower() in ("yes", "true"):
            return True
        else:
            return False
    return value
