def merge_dicts(dict_a: dict, dict_b: dict) -> dict:
    """
    Merge dict_b into dict_a.
    Returns a new dict, leaving the original dicts unchanged.
    """
    merged = dict_a.copy()
    merged.update(dict_b)
    return merged
