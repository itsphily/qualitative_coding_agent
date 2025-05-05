from coding_state import CodingState, Code, CaseInfo
from coding_utils import parse_arguments, initialize_state
from langgraph.types import Send
from typing import Dict, Any, List, Optional
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import START, END, StateGraph
from coding_prompt import identify_key_aspects_prompt

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

llm_long_context_with_structured_output = llm_long_context.with_structured_output(KeyAspectsOutput)

runtime_config = {  "configurable": {
                    "llm_aspect_identifier_structured": llm_long_context_with_structured_output
                    }
}

def start_llm(state: CodingState):
    """
    Empty start node
    """
    return state


def continue_to_aspect_definition(state: CodingState) -> List[Send]:
    codes = state.get("codes", {})
    if not codes:
        logging.warning("No codes found in state.")
        return []

    logging.info("Dispatching %d codes", len(codes))

    return [
        Send(
            "aspect_definition_node",
            {
                "identifier": desc,
                "code_description_for_prompt": desc 
            }
        )
        for desc in codes
    ]


def aspect_definition_node(payload: dict, config: RunnableConfig) -> Dict[str, Dict[str, Any]]:
    """
    Worker Node: Receives payload via Send, identifies key aspects for one code
    using a structured output LLM passed via runtime config.

    Args:
        payload (dict): The dictionary sent via Send, containing
                        'identifier' (code_description) and
                        'code_description_for_prompt'.
        config (RunnableConfig): The runtime configuration, expected to contain
                                 the pre-configured structured LLM client under
                                 config['configurable']['llm_aspect_identifier_structured'].

    Returns:
        Dict[str, Dict[str, Any]]: An update dictionary targeting the 'codes' key
                                   in the state, formatted for the custom reducer.
                                   e.g., {"codes": {"identifier": "...", "key_aspects": [...]}}
    """
    identifier = payload.get("identifier")
    code_description_for_prompt = payload.get("code_description_for_prompt")
    node_name = "aspect_definition_node" # For logging clarity
    logging.info(f"[{node_name}] Running for code: {identifier[:60]}...")

    # --- Input Validation ---
    if not identifier or not code_description_for_prompt:
        logging.error(f"[{node_name}] Invalid payload received: {payload}")
        # Return payload indicating error for the reducer
        return {"codes": {"identifier": identifier or "Unknown Error", "key_aspects": ["Error: Invalid Payload Received"]}}

    # --- Retrieve LLM from Config ---
    try:
        llm_aspect_identifier = config.get("configurable", {}).get("llm_aspect_identifier_structured")
        if not llm_aspect_identifier or not isinstance(llm_aspect_identifier, Runnable):
            raise ValueError("Required 'llm_aspect_identifier_structured' Runnable not found in config['configurable']")
    except Exception as e:
        logging.error(f"[{node_name}] Error retrieving LLM from config for code {identifier[:60]}: {e}")
        return {"codes": {"identifier": identifier, "key_aspects": [f"Error: LLM config missing - {e}"]}}

    # --- Prepare LLM Input ---
    try:
        system_message_content = identify_key_aspects_prompt
        # Use the code description received in the payload for the human message
        human_message_content = f"here is the code to deconstruct into core components: {code_description_for_prompt}"
        messages = [
            SystemMessage(content=system_message_content),
            HumanMessage(content=human_message_content)
        ]
        logging.debug(f"[{node_name}] Prepared messages for LLM for code: {identifier[:60]}")
    except Exception as e:
        logging.error(f"[{node_name}] Error formatting messages for code {identifier[:60]}: {e}")
        return {"codes": {"identifier": identifier, "key_aspects": ["Error: Prompt formatting failed"]}}

    # --- Invoke LLM and Parse Output ---
    aspects_list: List[str] = ["Error: LLM Call Failed"] # Default error value
    try:
        structured_output: KeyAspectsOutput = llm_aspect_identifier.invoke(messages, config) # Pass config if needed
        aspects_list = structured_output.key_aspects
        # Basic validation of the output structure
        if not isinstance(aspects_list, list) or not all(isinstance(item, str) for item in aspects_list):
             logging.warning(f"[{node_name}] LLM output for {identifier[:60]} not List[str]: {aspects_list}")
             aspects_list = ["Error: Invalid format parsed"]
        else:
             logging.info(f"[{node_name}] Successfully generated {len(aspects_list)} aspects for code: {identifier[:60]}")
    except Exception as e:
        logging.error(f"[{node_name}] LLM call/parsing failed for code {identifier[:60]}: {e}", exc_info=True)
        aspects_list = [f"Error: LLM/Parsing failed - {e}"]

    return {
        "codes": { 
            identifier: aspects_list
        }
    }

def place_holder(state: CodingState):
    """
    Placeholder node to ensure the graph ends
    """
    return state


coding_graph = StateGraph(CodingState)

# --- Add Nodes ---
coding_graph.add_node("start", start_llm)
coding_graph.add_node("aspect_definition_node", aspect_definition_node)
coding_graph.add_node("place_holder", place_holder)

# --- Add Edges ---
coding_graph.add_edge(START, "start")
coding_graph.add_conditional_edges("start",continue_to_aspect_definition, ['aspect_definition_node'])
coding_graph.add_edge("aspect_definition_node", 'place_holder')
coding_graph.add_edge("place_holder", END)

coding_graph = coding_graph.compile()


if __name__ == "__main__":
    parsed_args = parse_arguments()

    # --- Initialize the State ---
    initial_state = initialize_state(parsed_args)
    coding_graph.invoke(initial_state, config=runtime_config)

    print("\n--- Initial State Content ---")
    print(f"Research Question: {initial_state['research_question']}")
    print(f"\nCodes ({len(initial_state['codes'])}):")
    for desc, aspects in initial_state["codes"].items():
        print(f'  – {desc[:60]}...  →  {aspects}')
    print(f"\nCases ({len(initial_state['cases_info'])}):")
    for case_name, case_obj in initial_state['cases_info'].items():
        print(f"  - Key: \"{case_name}\"")

    print("\n--- Graph Definition and Execution Starts Here ---")
