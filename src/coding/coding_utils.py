from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from coding_state import Code


def update_codes_list_reducer(
    current_codes_list: Optional[List['Code']],
    new_results: Optional[List[Dict[str, Any]] | Dict[str, Any]]
    ) -> Optional[List['Code']]:
    """
    Reducer function to update the 'codes' list in the state.
    Merges new 'key_aspects' into the corresponding Code object based on 'identifier'.
    """
    if current_codes_list is None: current_codes_list = []
    if new_results is None: return current_codes_list

    updates_list = new_results if isinstance(new_results, list) else [new_results]

    codes_map = {code["code_description"]: code for code in current_codes_list}

    updates_applied_count = 0
    for update in updates_list:
        if isinstance(update, dict) and "identifier" in update and "key_aspects" in update:
            identifier = update["identifier"]
            key_aspects = update["key_aspects"]

            if identifier in codes_map:
                updated_code = codes_map[identifier].copy()
                updated_code["key_aspects"] = key_aspects
                codes_map[identifier] = updated_code
                updates_applied_count += 1
            else:
                 print(f"Warning: Reducer could not find code with identifier '{identifier}' to update aspects.")
        else:
             print(f"Warning: Reducer received invalid update format: {update}")

    print(f"--- Reducer applied {updates_applied_count} aspect updates ---")
    return list(codes_map.values())


def parse_code_string(code_string: str) -> Tuple[Optional[str], Optional[str]]:
    """Parses 'Code Name: Definition' string."""
    parts = code_string.split(':', 1)
    if len(parts) == 2:
        name = parts[0].strip()
        definition = parts[1].strip()
        return name, definition
    return None, None