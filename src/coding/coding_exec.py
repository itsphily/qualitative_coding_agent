from coding_state import CodingState, CaseInfo, CaseProcessingState, Evidence, merge_case_info, append_evidence, merge_evidence_from_subgraph
from coding_utils import parse_arguments, initialize_state
from langgraph.types import Send
from typing import Dict, Any, List, Optional, TypedDict, cast, Annotated
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.config import get_config
import os
import logging
from datetime import datetime
import glob
import pathlib
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import START, END, StateGraph
from coding_prompt import identify_key_aspects_prompt, identify_intervention
from coding_utils import visualize_graph


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

# --- Create evidence logging tool ---
@tool
def log_quote_reasoning(
    quote: str,
    reasoning: str,
    aspect: List[str],
    chronology: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
    code_description: str = None,
    doc_name: str = None
) -> Dict[str, Any]:
    """
    Tool for logging evidence found during text analysis.
    
    Args:
        quote: The text passage extracted as evidence
        reasoning: Explanation of why this quote is evidence
        aspect: List of aspects this quote relates to
        chronology: Timing relative to intervention (before/during/after/unclear)
        tool_call_id: Injected tool call ID
        code_description: The code this evidence relates to
        doc_name: Source document name
    """
    new_evidence = cast(Evidence, {
        "quote": quote,
        "reasoning": reasoning,
        "aspect": aspect,
        "chronology": chronology,
        "code_description": code_description,
        "doc_name": doc_name
    })
    
    # Return state update for the evidence_list
    return {"evidence_list": [new_evidence]}

# Initialize LLM for evidence extraction
llm_evidence_extractor = ChatOpenAI(model="o4-mini",
                                   temperature=0, 
                                   use_responses_api=True,
                                   timeout=None,
                                   max_retries=4,
                                   model_kwargs={"reasoning": reasoning}
)

# Bind the tool to the LLM upfront
llm_evidence_extractor_with_tools = llm_evidence_extractor.bind_tools(
    [log_quote_reasoning], 
    tool_choice={"type": "function", "function": {"name": "log_quote_reasoning"}}
)

runtime_config = {  "configurable": {
                    "llm_aspect_identifier_structured": llm_long_context_with_structured_output,
                    "llm_intervention_identifier": llm_long_context,
                    "llm_evidence_extractor": llm_evidence_extractor_with_tools
                    }
}

def start_llm(state: CodingState):
    """
    Empty start node
    """
    return state


def continue_to_aspect_definition(state: CodingState):
    codes = state.get("codes", {})
    if not codes:
        logging.warning("No codes found in state.")
        return []

    logging.info("Dispatching %d codes", len(codes))

    return [
        Send(
            "aspect_definition_node",
            code_description
        )
        for code_description in codes
    ]


def aspect_definition_node(code_description: str)-> Dict[str, Any]:
    """
    Worker Node: Identifies key aspects for a code using a structured output LLM.
    Uses the get_config() method to retrieve the LLM from runtime configuration.

    Args:
        code_description (str): The code description to analyze

    Returns:
        Dict[str, Dict[str, Any]]: An update dictionary targeting the 'codes' key
                                   in the state, with code_description as key
                                   and aspects list as value.
    """
    node_name = "aspect_definition_node" # For logging clarity
    logging.info(f"[{node_name}] Running for code: {code_description[:60]}...")

    # --- Retrieve LLM from Config using get_config() ---
    try:
        # Access configuration without explicit config parameter
        config = get_config()
        llm_aspect_identifier = config.get("configurable", {}).get("llm_aspect_identifier_structured")
        if not llm_aspect_identifier or not isinstance(llm_aspect_identifier, Runnable):
            raise ValueError("Required 'llm_aspect_identifier_structured' Runnable not found in config")
    except Exception as e:
        logging.error(f"[{node_name}] Error retrieving LLM from config for code {code_description[:60]}: {e}")
        return {"codes": {code_description: [f"Error: LLM config missing - {e}"]}}

    # --- Prepare LLM Input ---
    try:
        system_message_content = identify_key_aspects_prompt
        human_message_content = f"here is the code to deconstruct into core components: {code_description}"
        messages = [
            SystemMessage(content=system_message_content),
            HumanMessage(content=human_message_content)
        ]
        logging.debug(f"[{node_name}] Prepared messages for LLM for code: {code_description[:60]}")
    except Exception as e:
        logging.error(f"[{node_name}] Error formatting messages for code {code_description[:60]}: {e}")

    # --- Invoke LLM and Parse Output ---
    aspects_list: List[str] = ["Error: LLM Call Failed"]
    try:
        # Pass the current config when invoking the LLM
        structured_output: KeyAspectsOutput = llm_aspect_identifier.invoke(messages)
        aspects_list = structured_output.key_aspects
        if not isinstance(aspects_list, list) or not all(isinstance(item, str) for item in aspects_list):
             logging.warning(f"[{node_name}] LLM output for {code_description[:60]} not List[str]: {aspects_list}")
             aspects_list = ["Error: Invalid format parsed"]
        else:
             logging.info(f"[{node_name}] Successfully generated {len(aspects_list)} aspects for code: {code_description[:60]}")
    except Exception as e:
        logging.error(f"[{node_name}] LLM call/parsing failed for code {code_description[:60]}: {e}", exc_info=True)
        aspects_list = [f"Error: LLM/Parsing failed - {e}"]

    return {
        "codes": { 
            code_description: aspects_list
        }
    }

def intervention_definition_node(case_info: CaseInfo) -> Dict[str, Dict[str, Any]]:
    """
    Worker Node: Identifies the intervention from a case's directory of texts.
    Aggregates all text files, then uses an LLM to identify the single intervention.

    This node participates in a map operation, receiving a CaseInfo object and 
    returning a state update that will be merged with the main state.

    Args:
        case_info (CaseInfo): The case info object containing directory path

    Returns:
        Dict containing updates to cases_info that will be merged into the state
    """
    node_name = "intervention_definition_node"
    directory = case_info["directory"]
    description = case_info.get("description", "")
    
    # Get case_id by matching directory from the initial state (passed to this node)
    # We'll get this from the continue_to_intervention_definition function
    # which passed the entire case_info to us
    case_id = case_info.get("case_id", None)
    
    # If case_id isn't available (which shouldn't happen), fall back to using a derived ID
    if case_id is None:
        # Derive a case_id from the directory name as fallback
        case_id = os.path.basename(directory.rstrip("/"))
        logging.warning(f"[{node_name}] No case_id found, using derived id: {case_id}")
    
    logging.info(f"[{node_name}] Processing case {case_id} with directory: {directory}")
    
    # --- Aggregate all text files ---
    aggregated_texts = ""
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text_content = f.read()
                            aggregated_texts += f"path: {file_path}\n{text_content}\n\n"
                    except Exception as file_e:
                        logging.warning(f"[{node_name}] Could not read file {file_path}: {file_e}")
                        continue
    except Exception as e:
        logging.error(f"[{node_name}] Error walking directory {directory}: {e}")
        # Return a meaningful error instead of an empty dict
        return {"cases_info": {case_id: {"intervention": f"Error: Directory processing failed - {e}"}}}
    
    if not aggregated_texts:
        logging.warning(f"[{node_name}] No text files found in directory: {directory}")
        return {"cases_info": {case_id: {"intervention": "Error: No text files found"}}}
    
    # --- Retrieve LLM from Config ---
    try:
        config = get_config()
        llm_intervention_identifier = config.get("configurable", {}).get("llm_intervention_identifier")
        if not llm_intervention_identifier or not isinstance(llm_intervention_identifier, Runnable):
            raise ValueError("Required 'llm_intervention_identifier' Runnable not found in config")
    except Exception as e:
        logging.error(f"[{node_name}] Error retrieving LLM from config: {e}")
        return {"cases_info": {case_id: {"intervention": f"Error: LLM config missing - {e}"}}}
    
    # --- Prepare LLM Input ---
    try:
        system_message_content = identify_intervention
        human_message_content = f"here are the texts from which you need to find the **single intervention** : <texts>{aggregated_texts}</texts>"
        messages = [
            SystemMessage(content=system_message_content),
            HumanMessage(content=human_message_content)
        ]
        logging.debug(f"[{node_name}] Prepared messages for LLM for case with directory: {directory}")
    except Exception as e:
        logging.error(f"[{node_name}] Error formatting messages for directory {directory}: {e}")
        return {"cases_info": {case_id: {"intervention": f"Error: Message formatting failed - {e}"}}}
    
    # --- Invoke LLM and Parse Output ---
    intervention = "Error: LLM Call Failed"
    try:
        result = llm_intervention_identifier.invoke(messages)
        intervention = result.content.strip()
        logging.info(f"[{node_name}] Successfully identified intervention for case {case_id}: {intervention[:60]}...")
    except Exception as e:
        logging.error(f"[{node_name}] LLM call failed for directory {directory}: {e}", exc_info=True)
        intervention = f"Error: LLM call failed - {e}"
    
    # Use the case_id as the key, not the directory
    return {
        "cases_info": {
            case_id: {"intervention": intervention}
        }
    }

def continue_to_intervention_definition(state: CodingState) -> List[Send]:
    """
    Dispatches each case to the intervention_definition_node to identify interventions.
    Includes the case_id in the case_info to ensure proper tracking.
    """
    cases_info = state.get("cases_info", {})
    if not cases_info:
        logging.warning("No cases found in state.")
        return []

    logging.info("Dispatching %d cases for intervention identification", len(cases_info))

    # Create sends with case_id included in the case_info
    sends = []
    for case_id, case_info in cases_info.items():
        # Create a copy of the case_info with case_id added
        case_info_with_id = dict(case_info)
        case_info_with_id["case_id"] = case_id
        
        sends.append(Send("intervention_definition_node", case_info_with_id))
    
    return sends

def case_aggregation_node(state: CodingState) -> CodingState:
    """
    Aggregation node that ensures all parallel updates are properly combined 
    in the state before continuing to case processing.
    
    This node doesn't modify the state but ensures updates from aspect_definition_node
    and intervention_definition_node are fully applied before proceeding.
    
    Args:
        state: Current state of the graph
        
    Returns:
        The same state, ensuring all updates are aggregated
    """
    logging.info(f"[case_aggregation_node] Aggregating state before case processing")
    
    # Log what we have in the state
    codes = state.get("codes", {})
    cases_info = state.get("cases_info", {})
    
    logging.info(f"[case_aggregation_node] State contains {len(codes)} codes and {len(cases_info)} cases")
    
    for code, aspects in codes.items():
        logging.info(f"[case_aggregation_node] Code: {code[:60]}... has aspects: {aspects}")
    
    for case_id, info in cases_info.items():
        intervention = info.get("intervention", "No intervention specified")
        # Safely handle None values when displaying intervention
        intervention_display = intervention[:60] + "..." if intervention else "None"
        logging.info(f"[case_aggregation_node] Case: {case_id} has intervention: {intervention_display}")
    
    # Return the state unchanged - this node just ensures all updates are aggregated
    return state

# --- Case Processing Subgraph Implementation ---

def case_subgraph_start(state: CaseProcessingState) -> CaseProcessingState:
    """
    Starting node for the case processing subgraph.
    Validates input state and prepares for evidence extraction.
    """
    case_id = state.get("case_id")
    directory = state.get("directory")
    logging.info(f"[case_subgraph_start] Starting evidence extraction for case: {case_id} in directory: {directory}")
    return state

def identify_evidence_node(
    state: CaseProcessingState,
    code_description: str,
    file_path: str
) -> Dict:
    """
    Worker node that processes a single text file for a given code.
    Uses LLM with tool binding to extract evidence.
    
    Args:
        state: Current subgraph state
        code_description: The code to search for evidence
        file_path: Path to the text file to analyze
        
    Returns:
        Empty dict as state updates come from tool calls
    """
    node_name = "identify_evidence_node"
    logging.info(f"[{node_name}] Processing file {file_path} for code {code_description}")
    
    # Read the text file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
    except Exception as e:
        logging.error(f"[{node_name}] Error reading file {file_path}: {e}")
        return {}
    
    # Get information from state
    aspects = state["codes"].get(code_description, [])
    intervention = state.get("intervention", "Unknown intervention")
    research_question = state.get("research_question", "")
    case_id = state.get("case_id", "unknown")
    doc_name = os.path.basename(file_path)
    
    # Get LLM from config (already has tools bound)
    config = get_config()
    llm_with_tools = config.get("configurable", {}).get("llm_evidence_extractor")
    if not llm_with_tools:
        logging.error(f"[{node_name}] LLM for evidence extraction not found in config")
        return {}
    
    # Prepare prompt
    from coding_prompt import identify_evidence_prompt
    system_message = identify_evidence_prompt.format(
        code=code_description,
        aspects="\n".join([f"- {aspect}" for aspect in aspects]),
        research_question=research_question,
        intervention=intervention
    )
    
    # Call LLM with tools
    human_message = f"Text to analyze: {text_content}"
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=human_message)
    ]
    
    # Create a config with default values for the tool
    runnable_config = RunnableConfig(configurable={
        "code_description": code_description,
        "doc_name": doc_name
    })
    
    try:
        # Use the LLM with pre-bound tools, adding config
        result = llm_with_tools.invoke(messages, config=runnable_config)
        logging.info(f"[{node_name}] Successfully processed file {file_path} for code {code_description}")
        return {}  # Tool calls will update the state
    except Exception as e:
        logging.error(f"[{node_name}] Error processing file {file_path}: {e}", exc_info=True)
        return {}

def continue_to_identify_evidence(state: CaseProcessingState) -> List[Send]:
    """
    Routing function that sends each code + file combination to identify_evidence_node.
    
    Args:
        state: Current subgraph state containing case info and codes
        
    Returns:
        List of Send objects for each code-file combination
    """
    directory = state.get("directory", "")
    codes = state.get("codes", {})
    case_id = state.get("case_id", "unknown")
    
    if not directory or not codes:
        logging.warning(f"[continue_to_identify_evidence] Missing directory or codes in state for case {case_id}")
        return []
    
    sends = []
    
    # Find all text files in the directory (recursive)
    text_files = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    text_files.append(os.path.join(root, file))
    except Exception as e:
        logging.error(f"[continue_to_identify_evidence] Error walking directory {directory}: {e}")
        return []
    
    logging.info(f"[continue_to_identify_evidence] Found {len(text_files)} text files in {directory} for case {case_id}")
    
    # Create Send objects for each code and file combination
    for code_description in codes:
        for file_path in text_files:
            sends.append(
                Send(
                    "identify_evidence_node",
                    code_description=code_description,
                    file_path=file_path
                )
            )
    
    logging.info(f"[continue_to_identify_evidence] Dispatching {len(sends)} evidence extraction tasks for case {case_id}")
    return sends


# --- Create and Compile the Case Processing Subgraph ---
case_processing_graph = StateGraph(CaseProcessingState)

# Add nodes to the subgraph
case_processing_graph.add_node("case_start", case_subgraph_start)
case_processing_graph.add_node("identify_evidence_node", identify_evidence_node)

# Add edges to the subgraph
case_processing_graph.add_edge(START, "case_start")
case_processing_graph.add_conditional_edges(
    "case_start",
    continue_to_identify_evidence,
    ["identify_evidence_node"]
)
case_processing_graph.add_edge("identify_evidence_node", END)

# Compile the subgraph
case_processing_subgraph = case_processing_graph.compile()

# --- Create the Main Graph ---
coding_graph = StateGraph(CodingState)

def add_test(state: CodingState) -> CodingState:
    """
    Test node that returns the state unchanged.
    """
    return state

# --- Add Nodes ---
coding_graph.add_node("start", start_llm)
coding_graph.add_node("aspect_definition_node", aspect_definition_node)
coding_graph.add_node("add_test", add_test)
coding_graph.add_node("intervention_definition_node", intervention_definition_node)
coding_graph.add_node("case_aggregation_node", case_aggregation_node)
coding_graph.add_node("case_processing", case_processing_subgraph)

# --- Add Routing to Subgraph ---
def continue_to_case_processing(state: CodingState) -> List[Send]:
    """
    Routes each case to the case_processing subgraph.
    Passes only the necessary information for each case.
    
    Args:
        state: Main graph state with codes and cases
        
    Returns:
        List of Send objects, one for each case
    """
    cases_info = state.get("cases_info", {})
    codes = state.get("codes", {})
    research_question = state.get("research_question", "")
    
    if not cases_info or not codes:
        logging.warning("[continue_to_case_processing] Missing cases or codes in state, cannot route to case processing")
        return []
    
    sends = []
    for case_id, case_info in cases_info.items():
        directory = case_info.get("directory", "")
        intervention = case_info.get("intervention", "")
        
        if not directory:
            logging.warning(f"[continue_to_case_processing] Missing directory for case {case_id}, skipping")
            continue
        
        # Send specific case data to the subgraph
        sends.append(
            Send(
                "case_processing",
                {
                    "case_id":case_id,
                    "directory":directory,
                    "intervention":intervention,
                    "research_question":research_question,
                    "codes":codes,
                    "evidence_list":[]
                } 
            )
        )
    
    logging.info(f"[continue_to_case_processing] Dispatching {len(sends)} cases for evidence extraction")
    return sends



# --- Add Edges ---
coding_graph.add_edge(START, "start")
coding_graph.add_conditional_edges("start", continue_to_aspect_definition, ['aspect_definition_node'])
coding_graph.add_edge("aspect_definition_node", "add_test")
coding_graph.add_conditional_edges("add_test", continue_to_intervention_definition, ['intervention_definition_node'])
coding_graph.add_edge("intervention_definition_node", "case_aggregation_node")
coding_graph.add_conditional_edges("case_aggregation_node", continue_to_case_processing, ['case_processing'])
coding_graph.add_edge("case_processing", END)

coding_graph = coding_graph.compile()


if __name__ == "__main__":
    parsed_args = parse_arguments()

    # --- Initialize the State ---
    initial_state = initialize_state(parsed_args)
    visualize_graph(coding_graph, "coding_graph")
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
