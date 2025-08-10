def validate_schema(doc):
    """
    Minimal validation of the schema loaded from YAML or JSON.
    doc: dict
    Returns (ok: bool, message: str)
    """
    if not isinstance(doc, dict):
        return False, "Schema must be a mapping (dict)."
    if "type" not in doc:
        return False, "Schema must include 'type' (e.g. 'people' or 'ecommerce')."
    if "fields" in doc:
        if not isinstance(doc["fields"], list):
            return False, "The 'fields' field must be a list of definitions."
    return True, "OK"