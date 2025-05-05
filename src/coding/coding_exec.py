from coding_state import CodingState, Code, CaseInfo
from coding_utils import parse_arguments, initialize_state
from langgraph.constants import Send
import os
import logging
from datetime import datetime


# --- Logging Setup ---
debug_dir = os.getenv("DEBUG_DIR", "debug")
os.makedirs(debug_dir, exist_ok=True)
debug_file = os.path.join(debug_dir, f'debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.FileHandler(debug_file), logging.StreamHandler()]
)
logging.info(f"Starting script execution. Debug log file: {debug_file}")







if __name__ == "__main__":
    parsed_args = parse_arguments()

    initial_state = initialize_state(parsed_args)

    print("\n--- Initial State Content ---")
    print(f"Research Question: {initial_state['research_question']}")
    print(f"\nCodes ({len(initial_state['codes'])}):")
    for code_desc, code_obj in initial_state['codes'].items():
        print(f"  - Key: \"{code_desc[:60]}...\"") # Truncate long keys
    print(f"\nCases ({len(initial_state['cases_info'])}):")
    for case_name, case_obj in initial_state['cases_info'].items():
        print(f"  - Key: \"{case_name}\"")

    print("\n--- Graph Definition and Execution Starts Here ---")
