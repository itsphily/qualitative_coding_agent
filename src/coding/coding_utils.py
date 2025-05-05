import argparse
import json
from typing import List, Dict, Any, Optional, Tuple, cast, TYPE_CHECKING
if TYPE_CHECKING:
    from coding_state import CodingState, Code, CaseInfo


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


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for the main execution script."""
    parser = argparse.ArgumentParser(description="Run Multi-Phase Qualitative Analysis Workflow using LangGraph")
    parser.add_argument(
        "--research_question",
        required=True,
        help="Overall research question guiding the analysis."
    )
    parser.add_argument(
        "--code_list",
        required=True,
        nargs='+',
        help="List of code strings, typically 'Name: Definition' or just 'Description'."
    )
    parser.add_argument(
        "--charities",
        required=True,
        type=json.loads,
        help='JSON string representing a list of dictionaries, each with "charity_id", "charity_directory", and optional "charity_overview".'
    )
    return parser.parse_args()


def initialize_state(args: argparse.Namespace) -> 'CodingState':
    """
    Initializes the graph state dictionary from parsed command-line arguments.
    """
    print("--- Initializing Graph State ---")

    # 1. Process Codes
    initial_codes: Dict[str, Code] = {}
    print(f"Processing {len(args.code_list)} input codes...")
    for code_string in args.code_list:
        name, definition = parse_code_string(code_string)
        code_desc_key = code_string
        if name and definition:
            code_desc_key = f"{name}: {definition}"
        elif definition:
             code_desc_key = definition
        else:
             print(f"Warning: Using full string as key for possibly malformed code: {code_string}")

        if code_desc_key in initial_codes:
            print(f"Warning: Duplicate code description key detected: '{code_desc_key}'. Skipping duplicate.")
            continue
        initial_codes[code_desc_key] = Code(code_description=code_desc_key, key_aspects=None)
    print(f"Created {len(initial_codes)} code entries.")

    # 2. Process Cases (Charities)
    initial_cases_info: Dict[str, CaseInfo] = {}
    print(f"Processing {len(args.charities)} input cases/charities...")
    if isinstance(args.charities, list):
        for charity_data in args.charities:
            if isinstance(charity_data, dict):
                case_name = charity_data.get("charity_id")
                directory = charity_data.get("charity_directory")
                description = charity_data.get("charity_overview")

                if case_name and directory:
                    if case_name in initial_cases_info:
                         print(f"Warning: Duplicate case name (charity_id) detected: '{case_name}'. Overwriting.")
                    initial_cases_info[case_name] = CaseInfo(
                        directory=directory,
                        description=description,
                        intervention=None
                    )
                else:
                     print(f"Warning: Skipping charity data due to missing 'charity_id' or 'charity_directory': {charity_data}")
            else:
                print(f"Warning: Item in charities input is not a dictionary: {charity_data}")
    else:
        print(f"Error: --charities input was not parsed as a list. Received type: {type(args.charities)}")
        raise TypeError("--charities argument must be a valid JSON list of objects.")
    print(f"Created {len(initial_cases_info)} case entries.")

    initial_graph_state = cast(CodingState, {
        "research_question": args.research_question,
        "codes": initial_codes,
        "cases_info": initial_cases_info,

    })
    print("--- Initial Graph State Created ---")
    return initial_graph_state