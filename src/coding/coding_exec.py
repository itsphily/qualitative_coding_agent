from coding_state import CodingState, Code, CaseInfo
from coding_utils import parse_arguments, initialize_state
from langgraph.constants import Send
from typing import Dict, Any, List
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

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

# --- Load Environment Variables ---
if os.path.exists(".env"):
    logging.info("Loading environment variables from .env file.")
    load_dotenv()
else:
    logging.warning("No .env file found.")


# --- initialize the LLMs ---
## structured outputs needed for the LLM
class KeyAspectsOutput(BaseModel):
    """Structured output model for identifying key aspects of a code."""
    key_aspects: List[str] = Field(..., description="List of concise key aspects identified from the code definition")

## OpenAI LLM initialization
reasoning = {
    "effort": "high",  # 'low', 'medium', or 'high'
    "summary": "auto",  # 'detailed', 'auto', or None
}

llm_long_context_tool_use = ChatOpenAI(model="o4-mini",
                                       temperature=0, 
                                       use_responses_api=True,
                                       timeout=None,
                                       max_retries=4,
                                       model_kwargs={"reasoning": reasoning}
)


llm_short_context_high_processing = ChatOpenAI(model="o3",
                                               temperature=0, 
                                               use_responses_api=True, 
                                               timeout=None,
                                               max_retries=4,
                                               model_kwargs={"reasoning": reasoning}
)

## Google LLM initialization
llm_long_context_high_processing =  ChatGoogleGenerativeAI(model="gemini-2.5-pro-preview-03-25",
                                                           temperature=0,
                                                           max_tokens=None,
                                                           timeout=None,
                                                           max_retries=4,
)

## Google LLM initialization
llm_long_context =  ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17",
                                           temperature=0,
                                           max_tokens=None,
                                           timeout=None,
                                           max_retries=4,
)




if __name__ == "__main__":
    parsed_args = parse_arguments()

    initial_state = initialize_state(parsed_args)

    print("\n--- Initial State Content ---")
    print(f"Research Question: {initial_state['research_question']}")
    print(f"\nCodes ({len(initial_state['codes'])}):")
    for code_obj in initial_state['codes']:
        code_desc = code_obj.get('code_description', 'N/A')
        print(f"  - Code Desc: \"{code_desc[:60]}...\"")
    print(f"\nCases ({len(initial_state['cases_info'])}):")
    for case_name, case_obj in initial_state['cases_info'].items():
        print(f"  - Key: \"{case_name}\"")

    print("\n--- Graph Definition and Execution Starts Here ---")
