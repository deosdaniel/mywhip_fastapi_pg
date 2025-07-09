EXCEPTIONS = {"BMW", "KIA", "GMC"}


def normalize_make_model(value: str) -> str:

    if not value:
        return value
    value_clean = value.strip().upper()
    if value_clean in EXCEPTIONS:
        return value_clean
    return " ".join(word.capitalize() for word in value.strip().split())
