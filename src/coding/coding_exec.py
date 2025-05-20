from coding_state import (CodingState, 
                          CaseInfo, 
                          CaseProcessingState, 
                          CodeProcessingState, 
                          SynthesisState, 
                          EvaluateSynthesisState,
                          CrossCaseAnalysisState, 
                          FinalInsightState,
                          FindEvidenceInputState, FinalInsight, FinalEvidence)
from coding_utils import parse_arguments, initialize_state
from langgraph.types import Send
from typing import Dict, Any, List
from langgraph.config import get_config
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langchain_core.runnables import Runnable
from langgraph.graph import START, END, StateGraph
from coding_prompt import (
    identify_key_aspects_prompt,
    identify_intervention,
    identify_evidence_prompt,
    synthesize_evidence,
    evaluate_synthesis_prompt,
    cross_case_analysis_prompt_without_summary, 
    final_insights_prompt,
    find_evidence_prompt
)
from coding_utils import visualize_graph
from coding_tools import QUOTE_REASONING_TOOL, INSIGHT_TOOL, LOG_EVIDENCE_RELATIONSHIP_TOOL
from langgraph.types import Command
import json


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


reasoning_cfg = {
    "effort": "high",  
    "summary": "auto",
}

llm_long_context_tool_use = ChatOpenAI(
    model="o4-mini",
    use_responses_api=True, 
    model_kwargs={"reasoning": reasoning_cfg},
    timeout=None,
    max_retries=4
)

llm_short_context_high_processing = ChatOpenAI(model="o3",
                                               timeout=None,
                                               max_retries=4,
                                               reasoning_effort="high"
)

## Google LLM initialization
llm_long_context_high_processing =  ChatGoogleGenerativeAI(model="gemini-2.5-pro-preview-05-06",
                                                           temperature=0,
                                                           max_tokens=None,
                                                           timeout=None,
                                                           max_retries=35,
                                                           google_api_key=os.getenv("GOOGLE_API_KEY")
)

## Google LLM initialization
llm_long_context =  ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17",
                                           temperature=0,
                                           max_tokens=None,
                                           timeout=None,
                                           max_retries=35,
                                           google_api_key=os.getenv("GOOGLE_API_KEY")

)

llm_long_context_with_structured_output = llm_long_context.with_structured_output(KeyAspectsOutput)

# Bind the tool to the LLM upfront
llm_evidence_extractor_with_tools = llm_long_context_high_processing.bind_tools(QUOTE_REASONING_TOOL)
llm_insight_extractor_with_tools = llm_long_context_high_processing.bind_tools(INSIGHT_TOOL)
llm_log_evidence_relationship_with_tools = llm_long_context.bind_tools(LOG_EVIDENCE_RELATIONSHIP_TOOL)

runtime_config = {  "configurable": {
                    "llm_aspect_identifier_structured": llm_long_context_with_structured_output,
                    "llm_intervention_identifier": llm_long_context,
                    "llm_evidence_extractor": llm_evidence_extractor_with_tools,
                    "llm_synthesize_evidence": llm_short_context_high_processing,
                    "llm_evaluate_synthesis": llm_long_context_high_processing,
                    "llm_cross_case_analysis": llm_long_context_high_processing,
                    "llm_final_insights": llm_insight_extractor_with_tools,
                    "llm_evidence_relationship": llm_log_evidence_relationship_with_tools,
                    "code_description": "unknown_code",
                    "doc_name": "unknown_doc"
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
    node_name = "aspect_definition_node" 
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

def aspect_aggregation_node(state: CodingState) -> CodingState:
    """
    Aggregates aspects from all codes into a single list.
    """
    return state

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
    
    case_id = case_info.get("case_id", None)
    
    # If case_id isn't available fall back to using a derived ID
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
        # Return error instead of an empty dict
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
    
    return state

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
        
        # Create proper case-specific state to send to subgraph
        sends.append(
            Send(
                "case_processing",
                {
                    "case_id": case_id,  # Use the case_id from the loop
                    "directory": directory,  # Use the directory from case_info
                    "intervention": intervention,  # Use the intervention from case_info
                    "research_question": research_question,
                    "codes": codes,  # Pass all codes to each case
                    "evidence_list": [],  # Initialize as empty list
                    "messages": []  # Initialize as empty list
                }
            )
        )
    
    logging.info(f"[continue_to_case_processing] Dispatching {len(sends)} cases for evidence extraction")
    return sends

def case_subgraph_start(state: CaseProcessingState):
    """
    Starting node for the case processing subgraph.
    Converts input dictionary to CaseProcessingState.
    """
    case_id = state.get("case_id", "unknown")
    return CaseProcessingState(
          case_id=case_id,  # Store for internal use, won't be returned to parent
          directory=state.get("directory", ""),
          intervention=state.get("intervention", ""),
          research_question=state.get("research_question", ""),
          codes=state.get("codes", {}),
          synthesis_results={},
          revised_synthesis_results={},  
          cross_case_analysis_results={},  
          evidence_list=[],  
          final_insights_list=[]  
      )

def continue_to_identify_evidence(state: CaseProcessingState) -> List[Send]:
    """
    Routing function that sends each code + file combination directly to the agent_node.
    
    Args:
        state: Current subgraph state containing case info and codes
        
    Returns:
        List of Send objects for each code-file combination
    """
    directory = state.get("directory", "")
    codes = state.get("codes", {})
    case_id = state.get("case_id", "unknown")
    intervention = state.get("intervention", "")
    research_question = state.get("research_question", "")
    
    if not directory or not codes:
        logging.warning(f"[continue_to_identify_evidence] Missing directory or codes in state for case {case_id}")
        return []
    
    sends = []
    
    text_files = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    text_files.append(file_path)
                    
        logging.info(f"[continue_to_identify_evidence] Found {len(text_files)} text files in {directory} and subdirectories for case {case_id}")
    except Exception as e:
        logging.error(f"[continue_to_identify_evidence] Error walking directory {directory}: {e}")
        return []
    
    # Iterate over all codes and files
    for code_description in codes:
        aspects = codes.get(code_description, [])
        for file_path in text_files:
                code_state: CodeProcessingState = {
                  "file_path": file_path,
                  "code_description": code_description,
                  "aspects": aspects,
                  "intervention": intervention,
                  "research_question": research_question,
                  "case_id": case_id,
                  "evidence_list": []
              }
                sends.append(Send("agent_node", code_state))
                logging.info(f"[continue_to_identify_evidence] Dispatching {len(sends)} evidence extraction tasks for case {case_id}")
                
    return sends

def agent_node(state: CodeProcessingState) -> Dict:
    """
    Analyzes text using an LLM to identify evidence.
    Properly initializes messages on first call and preserves context.
    
    Args:
        state: Current state with file path, code description, aspects, etc.
        
    Returns:
        Updated state with messages from the LLM and preserved context
    """
    # Get file information
    file_path = state.get("file_path")
    if not file_path or not os.path.exists(file_path):
        logging.error(f"[agent_node] Invalid or missing file: {file_path}")
        return {"messages": [HumanMessage(content=f"Error: Invalid file path {file_path}")]}
    
    # Extract filename for doc_name
    doc_name = os.path.basename(file_path)
    code_description = state.get("code_description", "Unknown code")

    # Read the text file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
    except Exception as e:
        logging.error(f"[agent_node] Error reading file {file_path}: {e}")
        return {"evidence_list": []}
    
    # Get LLM from config
    config = get_config()
    llm_with_tools = config.get("configurable", {}).get("llm_evidence_extractor")
    if not llm_with_tools:
        logging.error(f"[agent_node] LLM for evidence extraction not found in config")
        return {"evidence_list": []}
   
    # format the prompt
    system_content = identify_evidence_prompt.format(
        code= state.get("code_description", "Unknown code"),
        aspects="\n".join([f"- {aspect}" for aspect in state.get("aspects", [])]),
        research_question=state.get("research_question", ""),
        intervention=state.get("intervention", "Unknown intervention")
    )

    system_msg = SystemMessage(content=system_content)
    human_msg = HumanMessage(content=f"Text to analyze: {text_content}")
    logging.info(f"[agent_node] Preparing to execute with CONFIGURATION: code_description='{code_description}', doc_name='{doc_name}'")
    ai_message = llm_with_tools.invoke([system_msg, human_msg])
    logging.info(f"[agent_node] Completed processing file {doc_name}, tool should have logged evidence")
    
    # Following the pattern from the update-state-from-tools documentation
    tool_calls = []
    if isinstance(ai_message, AIMessage) and hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
        tool_calls = ai_message.tool_calls
        logging.info(f"[agent_node] Found {len(tool_calls)} tool calls in LLM response")
    else:
        logging.warning(f"[agent_node] No tool calls found in LLM response")
        return []
    # Execute the tools and collect Commands
    commands = []
    tools_by_name = {tool.name: tool for tool in QUOTE_REASONING_TOOL}

    for tool_call in tool_calls:
        try:
            # Get tool by name
            tool_name = tool_call.get("name", "")
            if tool_name not in tools_by_name:
                logging.error(f"[agent_node] Unknown tool: {tool_name}")
                continue

            # Execute tool with arguments from tool call
            tool = tools_by_name[tool_name]
            args = tool_call.get("args", {})
            args["tool_call_id"] = tool_call.get("id", "unknown")

            args["state"] = {
                "code_description": state.get("code_description", "Unknown code"),
                "file_path": state.get("file_path", "Unknown file")
                }

            logging.info(f"[agent_node] Executing tool {tool_name} with args: {args}")

            # Following exactly the pattern from documentation
            command = tool.invoke(args)
            if isinstance(command, Command):
                commands.append(command)
                logging.info(f"[agent_node] Added Command from tool {tool_name}")
        except Exception as e:
            logging.error(f"[agent_node] Error executing tool {tool_call.get('name', 'unknown')}: {e}")

    logging.info(f"[agent_node] Returning {len(commands)} Commands to update state")
    return commands

def aggregation_node(state: CaseProcessingState) -> CaseProcessingState:
    """
    Aggregates evidence from all cases and codes.
    """
    return state

def continue_to_synthesize_evidence(state: CaseProcessingState) -> List[Send]:
    """
    Routing function that sends each code with its relevant evidence to the synthesize_evidence_node.
    
    Args:
        state: Current aggregated state with all evidence
        
    Returns:
        List of Send objects for each code with its evidence
    """
    case_id = state.get("case_id", "unknown")
    codes = state.get("codes", {})
    research_question = state.get("research_question", "")
    intervention = state.get("intervention", "")
    evidence_list = state.get("evidence_list", [])

    if not codes:
        logging.warning(f"[continue_to_synthesize_evidence] No codes found in state for case {case_id}")
        return []

    sends = []
    for code_description in codes:
        evidence_subset = []
        for evidence in evidence_list:
            if evidence.get("code_description") == code_description:
                filtered_evidence = {
                    "chronology": evidence.get("chronology", ""),
                    "quote": evidence.get("quote", ""),
                    "reasoning": evidence.get("reasoning", ""),
                    "aspect": evidence.get("aspect", [])
                }
                evidence_subset.append(filtered_evidence)

        if evidence_subset:
            synthesis_input = {
                "case_id": case_id,
                "code_description": code_description,
                "research_question": research_question,
                "intervention": intervention,
                "evidence_subset": evidence_subset
            }

            sends.append(Send("synthesize_evidence_node", synthesis_input))
            logging.info(f"[continue_to_synthesize_evidence] Sending {len(evidence_subset)} evidence items for code {code_description} to synthesis node")

    return sends
    
def synthesize_evidence_node(state: SynthesisState) -> Dict[str, Dict[str, str]]:
    """
    Worker Node: Synthesizes evidence for a specific code within a case.
    Formats evidence records according to the synthesize_evidence prompt 
    and invokes an LLM to generate synthesis.
    
    Args:
        state: Input state containing case_id, code, and filtered evidence
        
    Returns:
        Dict with synthesis results to be merged into the state
    """
    node_name = "synthesize_evidence_node"
    case_id = state.get("case_id", "unknown")
    code_description = state.get("code_description", "unknown")
    research_question = state.get("research_question", "")
    intervention = state.get("intervention", "")
    evidence_subset = state.get("evidence_subset", [])

    logging.info(f"[{node_name}] Processing {len(evidence_subset)} evidence items for code '{code_description[:60]}...' in case {case_id}")

    if not evidence_subset:
        logging.warning(f"[{node_name}] No evidence to synthesize for code {code_description} in case {case_id}")
        return {"synthesis_results": {code_description: "No evidence to synthesize"}}

    # --- Retrieve LLM from Config ---
    try:
        config = get_config()
        llm_synthesize_evidence = config.get("configurable", {}).get("llm_synthesize_evidence")
        if not llm_synthesize_evidence or not isinstance(llm_synthesize_evidence, Runnable):
            raise ValueError("Required 'llm_synthesize_evidence' Runnable not found in config")
    except Exception as e:
        logging.error(f"[{node_name}] Error retrieving LLM from config: {e}")
        return {"synthesis_results": {code_description: f"Error: LLM config missing - {e}"}}

    # --- Format Evidence for Prompt using new Markdown format ---
    evidence_text = ""
    for i, evidence in enumerate(evidence_subset):
        # Format each evidence item in Markdown as specified in the prompt
        evidence_text += f"# Evidence#{i}: \n"
        evidence_text += f"- chronology: \"{evidence.get('chronology', '')}\"\n"
        evidence_text += f"- quote: \"{evidence.get('quote', '').replace('\"', '\\\"')}\"\n"
        evidence_text += f"- reasoning: \"{evidence.get('reasoning', '').replace('\"', '\\\"')}\"\n"

        # Format the aspect list
        aspects = evidence.get("aspect", [])
        aspects_str = str(aspects).replace("'", "\"")
        evidence_text += f"- aspect: {aspects_str}\n\n"

    # --- Prepare LLM Input ---
    try:
        # Log a sample to debug
        sample = evidence_text[:200] + "..." if len(evidence_text) > 200 else evidence_text
        logging.info(f"[{node_name}] Evidence format sample: {sample}")

        system_message_content = synthesize_evidence.format(
            case_name=case_id,
            code=code_description,
            research_question=research_question,
            intervention=intervention,
            data=evidence_text
        )

        messages = [SystemMessage(content=system_message_content)]
        logging.debug(f"[{node_name}] Prepared messages for LLM for case {case_id} and code {code_description[:60]}")
    except Exception as e:
        error_msg = str(e)
        logging.error(f"[{node_name}] Error formatting messages: {error_msg}")
        return {"synthesis_results": {code_description: f"Error: Message formatting failed - {error_msg}"}}

    # --- Invoke LLM and Process Output ---
    synthesis_result = f"Error: LLM call failed for code {code_description}"
    try:
        result = llm_synthesize_evidence.invoke(messages)
        synthesis_result = result.content.strip()
        logging.info(f"[{node_name}] Successfully synthesized evidence for code {code_description[:60]} in case {case_id}")
    except Exception as e:
        logging.error(f"[{node_name}] LLM call failed: {e}", exc_info=True)
        synthesis_result = f"Error: LLM call failed - {e}"

    # Return results to be merged into state
    return {
        "synthesis_results": {
            code_description: synthesis_result
        }
    }

def aggregation_synthesis_node(state: CaseProcessingState) -> CaseProcessingState:
    """
    Aggregates synthesis results from all codes.
    """
    return state

def continue_to_evaluate_synthesis(state: CaseProcessingState) -> List[Send]:
    """
    Routing function that sends each synthesis result with case context to the evaluate_synthesis_node.
    
    Args:
        state: Current aggregated state with all synthesis results
        
    Returns:
        List of Send objects for each synthesis result
    """
    case_id = state.get("case_id", "unknown")
    directory = state.get("directory", "")
    research_question = state.get("research_question", "")
    intervention = state.get("intervention", "")
    synthesis_results = state.get("synthesis_results", {})

    if not synthesis_results:
        logging.warning(f"[continue_to_evaluate_synthesis] No synthesis results found in state for case {case_id}")
        return []

    sends = []
    for code_description, synthesis_result in synthesis_results.items():
        # Create input state for evaluate_synthesis_node
        evaluation_input = {
            "case_id": case_id,
            "directory": directory,
            "code_description": code_description,
            "research_question": research_question,
            "intervention": intervention,
            "synthesis_result": synthesis_result
        }

        sends.append(Send("evaluate_synthesis_node", evaluation_input))
        logging.info(f"[continue_to_evaluate_synthesis] Sending synthesis for code {code_description} to evaluation node")

    return sends

def evaluate_synthesis_node(state: EvaluateSynthesisState) -> Dict[str, Dict[str, str]]:
    """
    Worker Node: Evaluates synthesis for a specific code against all source texts.
    
    Args:
        state: Input state containing case_id, directory, code_description, etc.
        
    Returns:
        Dict with revised synthesis results to be merged into the state
    """
    node_name = "evaluate_synthesis_node"
    case_id = state.get("case_id", "unknown")
    directory = state.get("directory", "")
    code_description = state.get("code_description", "unknown")
    research_question = state.get("research_question", "")
    intervention = state.get("intervention", "")
    synthesis_result = state.get("synthesis_result", "")

    logging.info(f"[{node_name}] Evaluating synthesis for code '{code_description[:60]}...' in case {case_id}")

    if not synthesis_result:
        logging.warning(f"[{node_name}] No synthesis to evaluate for code {code_description} in case {case_id}")
        return {"revised_synthesis_results": {code_description: "No synthesis to evaluate"}}

    # --- Aggregate all text files ---
    source_texts = ""
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text_content = f.read()
                            doc_name = os.path.basename(file_path)
                            # Wrap the content in XML tags with document name
                            source_texts += f"<beginning of text: {doc_name}>\n{text_content}\n<end of text: {doc_name}>\n\n"
                    except Exception as file_e:
                        logging.warning(f"[{node_name}] Could not read file {file_path}: {file_e}")
                        continue
    except Exception as e:
        logging.error(f"[{node_name}] Error walking directory {directory}: {e}")
        return {"revised_synthesis_results": {code_description: f"Error: Directory processing failed - {e}"}}

    if not source_texts:
        logging.warning(f"[{node_name}] No text files found in directory: {directory}")
        return {"revised_synthesis_results": {code_description: "Error: No text files found"}}

    # --- Retrieve LLM from Config ---
    try:
        config = get_config()
        llm_evaluate_synthesis = config.get("configurable", {}).get("llm_evaluate_synthesis")
        if not llm_evaluate_synthesis or not isinstance(llm_evaluate_synthesis, Runnable):
            raise ValueError("Required 'llm_evaluate_synthesis' Runnable not found in config")
    except Exception as e:
        logging.error(f"[{node_name}] Error retrieving LLM from config: {e}")
        return {"revised_synthesis_results": {code_description: f"Error: LLM config missing - {e}"}}

    # --- Prepare LLM Input ---
    try:

        system_message_content = evaluate_synthesis_prompt
        human_message_content = f"""
        Please evaluate this synthesis result:

        # Context
        * **Case Name:** {case_id}
        * **Research Code (Name and Description):** {code_description}
        * **Research Question (Optional Context):** {research_question}
        * **Intervention (Optional Context):** {intervention}
        * **Context Usage:** Use the overall context (Research Question, Intervention) to judge the significance, relevance, and necessary refinements (for accuracy, completeness, and nuance) of findings during the validation process across all source texts.

        Synthesis Result:
        <preliminary_findings_summary>
        {synthesis_result}
        </preliminary_findings_summary>

        Source Texts:
        <Complete Source Texts>
        {source_texts}
        </Complete Source Texts>
        """

        messages = [SystemMessage(content=system_message_content), HumanMessage(content=human_message_content)]
        logging.debug(f"[{node_name}] Prepared messages for LLM for case {case_id} and code {code_description[:60]}")
    except Exception as e:
        error_msg = str(e)
        logging.error(f"[{node_name}] Error formatting messages: {error_msg}")
        return {"revised_synthesis_results": {code_description: f"Error: Message formatting failed - {error_msg}"}}

    # --- Invoke LLM and Process Output ---
    revised_synthesis_result = f"Error: LLM call failed for code {code_description}"
    try:
        result = llm_evaluate_synthesis.invoke(messages)
        revised_synthesis_result = result.content.strip()
        logging.info(f"[{node_name}] Successfully evaluated synthesis for code {code_description[:60]} in case {case_id}")
    except Exception as e:
        logging.error(f"[{node_name}] LLM call failed: {e}", exc_info=True)
        revised_synthesis_result = f"Error: LLM call failed - {e}"

    # Return results to be merged into state
    return {
        "revised_synthesis_results": {
            code_description: revised_synthesis_result
        }
    }

def aggregation_synthesis_evaluation_node(state: CaseProcessingState) -> CaseProcessingState:
    """
    Aggregates synthesis results from all codes.
    """
    return state

def continue_to_cross_case_analysis(state: CaseProcessingState) -> List[Send]:
    """
    Routing function that sends each code with its aspects to the cross_case_analysis_node.
    
    Args:
        state: Current aggregated state with all synthesis evaluation results
        
    Returns:
        List of Send objects for each code with its aspects
    """
    case_id = state.get("case_id", "unknown")
    directory = state.get("directory", "")
    research_question = state.get("research_question", "")
    intervention = state.get("intervention", "")
    codes = state.get("codes", {})
    revised_synthesis_results = state.get("revised_synthesis_results", {})

    if not codes or not revised_synthesis_results:
        logging.warning(f"[continue_to_cross_case_analysis] No codes or revised synthesis results found in state for case {case_id}")
        return []

    sends = []
    for code_description, aspects in codes.items():
        if code_description in revised_synthesis_results:
            cross_case_input = {
                "case_id": case_id,
                "code_description": code_description,
                "directory": directory,
                "research_question": research_question,
                "intervention": intervention,
                "aspects": aspects
            }

            sends.append(Send("cross_case_analysis_node", cross_case_input))
            logging.info(f"[continue_to_cross_case_analysis] Sending code {code_description} to cross-case analysis node")

    return sends

def cross_case_analysis_node(state: CrossCaseAnalysisState) -> Dict[str, Dict[str, str]]:
      """
      Worker Node: Analyzes all texts in a directory for a specific code.
      Creates a comprehensive cross-case analysis considering all source texts.
      
      Args:
          state: Input state containing case_id, code_description, directory, etc.
          
      Returns:
          Dict with cross-case analysis results to be merged into the state
      """
      node_name = "cross_case_analysis_node"
      case_id = state.get("case_id", "unknown")
      directory = state.get("directory", "")
      code_description = state.get("code_description", "unknown")
      research_question = state.get("research_question", "")
      intervention = state.get("intervention", "")
      aspects = state.get("aspects", [])

      logging.info(f"[{node_name}] Performing cross-case analysis for code '{code_description[:60]}...' in case {case_id}")

      # --- Aggregate all text files ---
      source_texts = ""
      try:
          for root, _, files in os.walk(directory):
              for file in files:
                  if file.endswith('.md') or file.endswith('.txt'):
                      file_path = os.path.join(root, file)
                      try:
                          with open(file_path, 'r', encoding='utf-8') as f:
                              text_content = f.read()
                              doc_name = os.path.basename(file_path)
                              # Wrap the content in XML tags with document name
                              source_texts += f"<beginning of text: {doc_name}>\n{text_content}\n<end of text: {doc_name}>\n\n"
                      except Exception as file_e:
                          logging.warning(f"[{node_name}] Could not read file {file_path}: {file_e}")
                          continue
      except Exception as e:
          logging.error(f"[{node_name}] Error walking directory {directory}: {e}")
          return {"cross_case_analysis_results": {code_description: f"Error: Directory processing failed - {e}"}}

      if not source_texts:
          logging.warning(f"[{node_name}] No text files found in directory: {directory}")
          return {"cross_case_analysis_results": {code_description: "Error: No text files found"}}

      # --- Retrieve LLM from Config ---
      try:
          config = get_config()
          llm_cross_case_analysis = config.get("configurable", {}).get("llm_cross_case_analysis")
          if not llm_cross_case_analysis or not isinstance(llm_cross_case_analysis, Runnable):
              raise ValueError("Required 'llm_cross_case_analysis' Runnable not found in config")
      except Exception as e:
          logging.error(f"[{node_name}] Error retrieving LLM from config: {e}")
          return {"cross_case_analysis_results": {code_description: f"Error: LLM config missing - {e}"}}

      # --- Prepare LLM Input ---
      try:
          # Format the aspects for the prompt
          aspects_text = "\n".join([f"- {aspect}" for aspect in aspects])

          system_message_content = cross_case_analysis_prompt_without_summary.format(
            case_name=case_id,
            code=code_description,
          )
          human_message_content = f"""
          Please analyze this case:
          # Context
          * **Case Name:** {case_id}
          * **Research Code (Name and Description):** {code_description}
          * **Defined Aspects of the research code:** 
          {aspects_text}
          * **Research Question:** {research_question}
          * **Intervention:** {intervention}
          * **Context Usage:** Use the overall context (Research Question, Intervention) to interpret the significance of the synthesis patterns you identify across the full texts as they relate to each aspect of the research code.
          
          # Input Data
          **Complete Source Texts (Primary and Only Data for this Task):**
          <source_texts>
          {source_texts}
          </source_texts>
          * You **must** base your entire deep synthesis analysis *directly and exclusively* on a fresh, holistic review of these `source_texts`. Do not refer to or expect any pre-existing summaries for this specific task.
          """

          messages = [SystemMessage(content=system_message_content), HumanMessage(content=human_message_content)]
          logging.debug(f"[{node_name}] Prepared messages for LLM for case {case_id} and code {code_description[:60]}")
      except Exception as e:
          error_msg = str(e)
          logging.error(f"[{node_name}] Error formatting messages: {error_msg}")
          return {"cross_case_analysis_results": {code_description: f"Error: Message formatting failed - {error_msg}"}}

      # --- Invoke LLM and Process Output ---
      cross_case_result = f"Error: LLM call failed for code {code_description}"
      try:
          result = llm_cross_case_analysis.invoke(messages)
          cross_case_result = result.content.strip()
          logging.info(f"[{node_name}] Successfully completed cross-case analysis for code {code_description[:60]} in case {case_id}")
      except Exception as e:
          logging.error(f"[{node_name}] LLM call failed: {e}", exc_info=True)
          cross_case_result = f"Error: LLM call failed - {e}"

      # Return results to be merged into state
      return {
          "cross_case_analysis_results": {
              code_description: cross_case_result
          }
      }

def aggregation_cross_case_analysis_node(state: CaseProcessingState) -> CaseProcessingState:
    """
    Aggregates cross-case analysis results from all codes.
    """
    return state

def continue_to_final_insight(state: CaseProcessingState) -> List[Send]:
    """
    Routing function that sends each code with its revised synthesis and cross-case analysis
    to the generate_final_insight node.
    
    Args:
        state: Current aggregated state with synthesis and cross-case analysis results
        
    Returns:
        List of Send objects for each code with its results
    """
    case_id = state.get("case_id", "unknown")
    research_question = state.get("research_question", "")
    intervention = state.get("intervention", "")
    codes = state.get("codes", {})
    revised_synthesis_results = state.get("revised_synthesis_results", {})
    cross_case_analysis_results = state.get("cross_case_analysis_results", {})

    if not codes or not revised_synthesis_results or not cross_case_analysis_results:
        logging.warning(f"[continue_to_final_insight] Missing codes, synthesis, or cross-case analysis in state for case {case_id}")
        return []

    sends = []
    for code_description, aspects in codes.items():
        # Only proceed if we have both revised synthesis and cross-case analysis for this code
        if code_description in revised_synthesis_results and code_description in cross_case_analysis_results:
            final_insight_input = {
                "case_id": case_id,
                "code_description": code_description,
                "research_question": research_question,
                "intervention": intervention,
                "aspects": aspects,
                "revised_synthesis_result": revised_synthesis_results[code_description],
                "cross_case_analysis_result": cross_case_analysis_results[code_description],
                "final_insights_list": []
            }

            sends.append(Send("generate_final_insight_node", final_insight_input))
            logging.info(f"[continue_to_final_insight] Sending code {code_description} to final insight generation")

    return sends

def generate_final_insight_node(state: FinalInsightState) -> Dict:
      """
      Worker Node: Generates final insights by analyzing revised synthesis and cross-case analysis.
      Uses an LLM that can make tool calls to log insights.
      
      Args:
          state: Input state containing case_id, code_description, synthesis results
          
      Returns:
          Updated state with insights added via tool calls
      """
      node_name = "generate_final_insight_node"
      case_id = state.get("case_id", "unknown")
      code_description = state.get("code_description", "unknown")
      aspects = state.get("aspects", [])
      research_question = state.get("research_question", "")
      intervention = state.get("intervention", "")
      revised_synthesis_result = state.get("revised_synthesis_result", "")
      cross_case_analysis_result = state.get("cross_case_analysis_result", "")

      logging.info(f"[{node_name}] Generating final insights for code '{code_description[:60]}...' in case {case_id}")

      # Validate inputs
      if not revised_synthesis_result or not cross_case_analysis_result:
          logging.warning(f"[{node_name}] Missing synthesis or cross-case analysis for code {code_description} in case {case_id}")
          return {"final_insights_list": []}

      # Get LLM with tool binding from config
      config = get_config()
      llm_with_tools = config.get("configurable", {}).get("llm_final_insights")
      if not llm_with_tools:
          logging.error(f"[{node_name}] LLM for final insights not found in config")
          return {"final_insights_list": []}

      # Format the prompt
      system_content = final_insights_prompt.format(
          case_name=case_id,
          code=code_description,
          aspects=aspects,
          research_question=research_question,
          intervention=intervention,
          adjusted_summary_text=revised_synthesis_result,
          deep_synthesis_report_text=cross_case_analysis_result
      )

      system_msg = SystemMessage(content=system_content)
      human_msg = HumanMessage(content="Please analyze these reports and generate final insights.")

      # Set up the state object for the tool to access
      code_state = {
          "code_description": code_description
      }

      # Execute the LLM with tool
      logging.info(f"[{node_name}] Preparing to execute with code_description='{code_description}'")
      ai_message = llm_with_tools.invoke([system_msg, human_msg], {"configurable": {"state": code_state}})
      logging.info(f"[{node_name}] Completed generating insights for code {code_description}, tool should have logged insights")

      # Process tool calls
      tool_calls = []
      if isinstance(ai_message, AIMessage) and hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
          tool_calls = ai_message.tool_calls
          logging.info(f"[{node_name}] Found {len(tool_calls)} tool calls in LLM response")
      else:
          logging.warning(f"[{node_name}] No tool calls found in LLM response")
          return {"final_insights_list": []}

      # Execute the tools and collect Commands
      commands = []
      tools_by_name = {tool.name: tool for tool in INSIGHT_TOOL}

      for tool_call in tool_calls:
          try:
              # Get tool by name
              tool_name = tool_call.get("name", "")
              if tool_name not in tools_by_name:
                  logging.error(f"[{node_name}] Unknown tool: {tool_name}")
                  continue

              # Execute tool with arguments from tool call
              tool = tools_by_name[tool_name]
              args = tool_call.get("args", {})
              args["tool_call_id"] = tool_call.get("id", "unknown")

              args["state"] = {
                  "code_description": code_description
              }

              logging.info(f"[{node_name}] Executing tool {tool_name} with args: {args}")

              # Execute tool and collect command
              command = tool.invoke(args)
              if isinstance(command, Command):
                  commands.append(command)
                  logging.info(f"[{node_name}] Added Command from tool {tool_name}")
          except Exception as e:
              logging.error(f"[{node_name}] Error executing tool {tool_call.get('name', 'unknown')}: {e}")

      logging.info(f"[{node_name}] Returning {len(commands)} Commands to update state")
      return commands

def aggregation_final_insights_node(state: CaseProcessingState) -> CaseProcessingState:
    """
    Aggregates final insights from all codes and prepares them for evidence finding.
    """
    final_insights_list = state.get("final_insights_list", [])

    # Ensure each final insight has a final_evidence_list field initialized
    for insight in final_insights_list:
        if "final_evidence_list" not in insight:
            insight["final_evidence_list"] = []

    logging.info(f"[aggregation_final_insights_node] Aggregated {len(final_insights_list)} final insights")
    return state

def continue_to_find_evidence_for_insights(state: CaseProcessingState) -> List[Send]:
    """
    Routing function that sends each final insight to the find_relevant_evidence_node
    along with the full evidence corpus.
    
    Args:
        state: Current state with final insights and evidence corpus
        
    Returns:
        List of Send objects, one for each final insight, or END if no insights to process
    """
    case_id = state.get("case_id", "unknown")
    final_insights_list = state.get("final_insights_list", [])
    evidence_list = state.get("evidence_list", [])
    
    if not final_insights_list:
        logging.warning(f"[continue_to_find_evidence_for_insights] No insights to process for case {case_id}")
        return [END]  # Return END if no insights to process
    
    if not evidence_list:
        logging.warning(f"[continue_to_find_evidence_for_insights] No evidence corpus available for case {case_id}")
        return [END]  # Return END if no evidence to process
    
    logging.info(f"[continue_to_find_evidence_for_insights] Processing {len(final_insights_list)} insights with {len(evidence_list)} evidence items")
    
    sends = []
    for insight in final_insights_list:
        insight_label = insight.get("insight_label", "unknown")
        # Create input state for find_relevant_evidence_node
        evidence_input = FindEvidenceInputState(
            current_final_insight=insight,
            full_evidence_list=evidence_list,
            processed_evidence_for_insight=[]  # Initialize as empty list
        )
        
        sends.append(Send("find_relevant_evidence_node", evidence_input))
        logging.info(f"[continue_to_find_evidence_for_insights] Sending insight '{insight_label[:30]}...' to evidence finder")
    
    return sends

def find_relevant_evidence_node(state: FindEvidenceInputState) -> FinalInsight:
    """
    Worker Node: Identifies evidence relevant to a specific final insight.
    Manually processes tool calls from the LLM to populate the insight's evidence list.
    Returns a single updated FinalInsight object.
    """
    node_name = "find_relevant_evidence_node"
    current_final_insight = state.get("current_final_insight", {})
    full_evidence_list = state.get("full_evidence_list", [])

    if not isinstance(current_final_insight, dict) or not current_final_insight.get("insight_label"):
        logging.error(f"[{node_name}] Invalid or incomplete current_final_insight: {current_final_insight}")
        # Return a structure that won't break the reducer, or raise error
        return FinalInsight(code_description="Error", insight_label="Error", insight_explanation="Invalid input insight", supporting_evidence_summary="", final_evidence_list=[])


    insight_label = current_final_insight.get("insight_label", "unknown_insight_label") # Should always exist due to check above
    insight_explanation = current_final_insight.get("insight_explanation", "")

    logging.info(f"[{node_name}] Finding evidence for insight '{insight_label[:50]}...'")

    if not insight_explanation:
        logging.warning(f"[{node_name}] Missing insight explanation for insight '{insight_label}'. Returning original.")
        # Ensure it has final_evidence_list initialized
        if "final_evidence_list" not in current_final_insight:
             current_final_insight["final_evidence_list"] = []
        return current_final_insight

    if not full_evidence_list:
        logging.warning(f"[{node_name}] No evidence corpus for insight '{insight_label}'. Returning original.")
        if "final_evidence_list" not in current_final_insight:
             current_final_insight["final_evidence_list"] = []
        return current_final_insight

    config_from_graph = get_config() 
    llm_with_tools = config_from_graph.get("configurable", {}).get("llm_evidence_relationship")
    if not llm_with_tools:
        logging.error(f"[{node_name}] LLM for evidence relationship not found in config for insight '{insight_label}'")
        if "final_evidence_list" not in current_final_insight:
             current_final_insight["final_evidence_list"] = []
        return current_final_insight

    evidence_corpus_for_prompt = {}
    for idx, evidence_item in enumerate(full_evidence_list):
        evidence_corpus_for_prompt[str(idx)] = {
            "chronology": evidence_item.get("chronology", "unclear"),
            "Doc Name": os.path.basename(evidence_item.get("doc_name", "Unknown Document")),
            "Quote": evidence_item.get("quote", ""),
            "Reasoning": evidence_item.get("reasoning", "")
        }
    formatted_evidence_corpus_str = json.dumps(evidence_corpus_for_prompt, indent=2)
    
    system_content = find_evidence_prompt 
    human_content = f"""
Single Final Insight to process:
{{
  "insight_label": "{insight_label}",
  "insight_explanation": "{insight_explanation.replace('"', '\\"')}",
  "supporting_evidence_summary": "{current_final_insight.get('supporting_evidence_summary','').replace('"', '\\"')}"
}}

Corpus of Evidence to search:
<corpus_of_evidence>
{formatted_evidence_corpus_str}
</corpus_of_evidence>

Remember to call the `log_evidence_relationship` tool for EVERY piece of evidence that has a discernible relationship to the insight explanation.
"""
    system_msg = SystemMessage(content=system_content)
    human_msg = HumanMessage(content=human_content)

    logging.info(f"[{node_name}] Preparing to execute LLM for insight_label='{insight_label}'")
    
    ai_message = llm_with_tools.invoke([system_msg, human_msg], {"configurable": {"state": state}})
    logging.info(f"[{node_name}] Completed LLM execution for insight '{insight_label}'")

    processed_evidence_list_for_this_insight = []

    # Manually parsing tool_calls from ai_message,
    if isinstance(ai_message, AIMessage) and hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
        logging.info(f"[{node_name}] Found {len(ai_message.tool_calls)} tool calls in LLM response for insight '{insight_label}'")
        for tool_call in ai_message.tool_calls:
            if tool_call.get("name") == "log_evidence_relationship":
                args = tool_call.get("args", {})
                try:
                    final_evidence_item = FinalEvidence(
                        insight_label=insight_label,
                        evidence_doc_name=args.get("evidence_doc_name", "N/A from tool call"),
                        evidence_quote=args.get("evidence_quote", "N/A from tool call"),
                        evidence_chronology=args.get("evidence_chronology", "unclear from tool call"),
                        agreement_level=args.get("agreement_level", "unknown from tool call"),
                        original_reasoning_for_quote=args.get("original_reasoning_for_quote", "N/A from tool call")
                    )
                    processed_evidence_list_for_this_insight.append(final_evidence_item)
                    logging.debug(f"[{node_name}] Manually processed tool call for insight '{insight_label}': {args.get('evidence_quote', 'N/A')[:30]}...")
                except KeyError as e:
                    logging.error(f"[{node_name}] Missing argument in tool call for log_evidence_relationship: {e}. Args: {args}")
                except Exception as e:
                    logging.error(f"[{node_name}] Error creating FinalEvidence from tool call args: {e}. Args: {args}")
            else:
                logging.warning(f"[{node_name}] Encountered unexpected tool call: {tool_call.get('name')}")
    else:
        logging.warning(f"[{node_name}] No tool calls found in LLM response for insight '{insight_label}'")
        # If state.get("processed_evidence_for_insight") was populated by Command, use it as fallback
        if state.get("processed_evidence_for_insight"):
             logging.info(f"[{node_name}] Using processed_evidence_for_insight from state as fallback for insight '{insight_label}'.")
             processed_evidence_list_for_this_insight = list(state.get("processed_evidence_for_insight", []))


    updated_insight = dict(current_final_insight)
    updated_insight["final_evidence_list"] = processed_evidence_list_for_this_insight

    logging.info(f"[{node_name}] Returning updated insight '{insight_label}' with {len(updated_insight['final_evidence_list'])} pieces of evidence.")
    return {"final_insights_list": [updated_insight]}

def aggregation_relevant_evidence(state: CaseProcessingState)-> Dict[str, Any]:
    """
    Aggregates evidence relationship results from all insights.
    Ensures each insight has its evidence properly associated.
    
    Args:
        state: Current state with all insights and their evidence
        
    Returns:
        Updated state with insights and their associated evidence
    """
    case_id = state.get("case_id")

    # Construct the dictionary of results for this specific case
    case_results_payload = {
        "directory": state.get("directory", ""),
        "intervention": state.get("intervention", ""),
        "research_question": state.get("research_question", ""),
        "synthesis_results": state.get("synthesis_results"),
        "revised_synthesis_results": state.get("revised_synthesis_results"),
        "cross_case_analysis_results": state.get("cross_case_analysis_results"),
        "evidence_list": state.get("evidence_list"),
        "final_insights_list": state.get("final_insights_list")
    }

    # The output must be structured to target the 'cases_info' field in CodingState,
    # with the current case_id as the key.
    
    logging.info(f"[aggregation_relevant_evidence] Returning case_results_payload for case {case_id}")
    return {
        "cases_info": {
            case_id: case_results_payload
        }
    }

def aggregation_case_processing(state: CaseProcessingState) -> CaseProcessingState:
    """
    Aggregates results from the case processing subgraph.
    """
    return state

# --- Create and Compile the Case Processing Subgraph ---
case_processing_graph = StateGraph(CaseProcessingState)

# Add nodes directly to the subgraph
case_processing_graph.add_node("case_start", case_subgraph_start)
case_processing_graph.add_node("agent_node", agent_node)
case_processing_graph.add_node("aggregation_node", aggregation_node)
case_processing_graph.add_node("synthesize_evidence_node", synthesize_evidence_node)
case_processing_graph.add_node("aggregation_synthesis_node", aggregation_synthesis_node)
case_processing_graph.add_node("evaluate_synthesis_node", evaluate_synthesis_node)
case_processing_graph.add_node("aggregation_synthesis_evaluation_node", aggregation_synthesis_evaluation_node)
case_processing_graph.add_node("cross_case_analysis_node", cross_case_analysis_node)
case_processing_graph.add_node("aggregation_cross_case_analysis_node", aggregation_cross_case_analysis_node)
case_processing_graph.add_node("generate_final_insight_node", generate_final_insight_node)
case_processing_graph.add_node("aggregation_final_insights_node", aggregation_final_insights_node)
case_processing_graph.add_node("find_relevant_evidence_node", find_relevant_evidence_node)
case_processing_graph.add_node("aggregation_relevant_evidence", aggregation_relevant_evidence)

# Add edges to implement the ReAct pattern
case_processing_graph.add_edge(START, "case_start")
case_processing_graph.add_conditional_edges(
    "case_start",
    continue_to_identify_evidence,
    ["agent_node"]
)
case_processing_graph.add_edge("agent_node", "aggregation_node")
case_processing_graph.add_conditional_edges("aggregation_node", continue_to_synthesize_evidence, ["synthesize_evidence_node"])
case_processing_graph.add_edge("synthesize_evidence_node", "aggregation_synthesis_node")
case_processing_graph.add_conditional_edges(
      "aggregation_synthesis_node",
      continue_to_evaluate_synthesis,
      ["evaluate_synthesis_node"]
  )
case_processing_graph.add_edge("evaluate_synthesis_node", "aggregation_synthesis_evaluation_node")
case_processing_graph.add_conditional_edges(
      "aggregation_synthesis_evaluation_node",
      continue_to_cross_case_analysis,
      ["cross_case_analysis_node"]
  )
case_processing_graph.add_edge("cross_case_analysis_node", "aggregation_cross_case_analysis_node")
case_processing_graph.add_conditional_edges("aggregation_cross_case_analysis_node", continue_to_final_insight, ["generate_final_insight_node"])
case_processing_graph.add_edge("generate_final_insight_node", "aggregation_final_insights_node")
case_processing_graph.add_conditional_edges("aggregation_final_insights_node",continue_to_find_evidence_for_insights,["find_relevant_evidence_node"] )
case_processing_graph.add_edge("find_relevant_evidence_node", "aggregation_relevant_evidence")
case_processing_graph.add_edge("aggregation_relevant_evidence", END)

# Compile the subgraph
case_processing_subgraph = case_processing_graph.compile()

# --- Create the Main Graph ---
coding_graph = StateGraph(CodingState)

# --- Add Nodes ---
coding_graph.add_node("start", start_llm)
coding_graph.add_node("aspect_definition_node", aspect_definition_node)
coding_graph.add_node("aspect_aggregation_node", aspect_aggregation_node)
coding_graph.add_node("intervention_definition_node", intervention_definition_node)
coding_graph.add_node("case_aggregation_node", case_aggregation_node)
coding_graph.add_node("case_processing", case_processing_subgraph)
coding_graph.add_node("aggregation_case_processing", aggregation_case_processing)

# --- Add Edges ---
coding_graph.add_edge(START, "start")
coding_graph.add_conditional_edges("start", continue_to_aspect_definition, ['aspect_definition_node'])
coding_graph.add_edge("aspect_definition_node", "aspect_aggregation_node")
coding_graph.add_conditional_edges("aspect_aggregation_node", continue_to_intervention_definition, ['intervention_definition_node'])
coding_graph.add_edge("intervention_definition_node", "case_aggregation_node")
coding_graph.add_conditional_edges("case_aggregation_node", continue_to_case_processing, ['case_processing'])
coding_graph.add_edge("case_processing", "aggregation_case_processing")
coding_graph.add_edge("aggregation_case_processing", END)

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
