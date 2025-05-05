import argparse
import json
from typing import List, Dict, cast
from coding_state import CodingState, Code, CaseInfo
from coding_utils import parse_code_string


def parse_arguments():
    """Parses command-line arguments."""
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

def initialize_state(args: argparse.Namespace) -> CodingState:
    """
    Initializes the graph state dictionary from parsed command-line arguments.
    """
    print("--- Initializing Graph State ---")

    initial_codes: Dict[str, Code] = {}
    print(f"Processing {len(args.code_list)} input codes...")
    for code_string in args.code_list:
        name, definition = parse_code_string(code_string)
        code_desc_key = code_string # Fallback key
        if name and definition:
            code_desc_key = f"{name}: {definition}" # Use combined as key
        elif definition: # If only description provided
             code_desc_key = definition
        else: # If only name or unparseable
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
                description = charity_data.get("charity_overview") # Maps to CaseInfo description

                if case_name and directory:
                    if case_name in initial_cases_info:
                         print(f"Warning: Duplicate case name (charity_id) detected: '{case_name}'. Overwriting.")
                    initial_cases_info[case_name] = CaseInfo(
                        directory=directory,
                        description=description,
                        intervention=None # Initialize intervention as None
                    )
                else:
                     print(f"Warning: Skipping charity data due to missing 'charity_id' or 'charity_directory': {charity_data}")
            else:
                print(f"Warning: Item in charities input is not a dictionary: {charity_data}")
    else:
        # This should ideally be caught by argparse type=json.loads if input isn't a valid JSON list representation
        print(f"Error: --charities input was not parsed as a list. Received type: {type(args.charities)}")
        # Handle error more robustly (e.g., raise ValueError)
        raise TypeError("--charities argument must be a valid JSON list of objects.")
    print(f"Created {len(initial_cases_info)} case entries.")


    # 3. Create Initial State Dictionary using Type Hint for Validation (Optional but good practice)
    # Using cast to satisfy type checker if needed, assumes structure matches CodingState
    initial_graph_state = cast(CodingState, {
        "research_question": args.research_question,
        "codes": initial_codes,
        "cases_info": initial_cases_info,
        # Initialize other potential top-level state fields expected by the graph later
        # These might be added by nodes/reducers if not initialized, but explicit is clearer
    })
    print("--- Initial Graph State Created ---")
    return initial_graph_state


# Main execution block
if __name__ == "__main__":
    # Parse command-line arguments
    parsed_args = parse_arguments()

    # Create the initial state dictionary
    initial_state = initialize_state(parsed_args)

    # Print the initial state for verification (optional)
    print("\n--- Initial State Content ---")
    print(f"Research Question: {initial_state['research_question']}")
    print(f"\nCodes ({len(initial_state['codes'])}):")
    for code_desc, code_obj in initial_state['codes'].items():
        print(f"  - Key: \"{code_desc}\"")
        # print(f"    Value: {code_obj}") # Can be verbose
    print(f"\nCases ({len(initial_state['cases_info'])}):")
    for case_name, case_obj in initial_state['cases_info'].items():
        print(f"  - Key: \"{case_name}\"")
        # print(f"    Value: {case_obj}") # Can be verbose

    print("\n--- Next Steps: Define and run the LangGraph workflow ---")
