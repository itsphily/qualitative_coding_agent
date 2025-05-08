case_processing_graph.add_node("identify_evidence_node", identify_evidence_node)  

# Keep for backwards compatibility
case_processing_graph.add_edge("identify_evidence_node", END)


def identify_evidence_node(state: CaseProcessingState) -> Dict:
    """
    Worker node that processes a single text file for a given code.
    Uses LLM with tool binding to extract evidence.
    
    Args:
        state: Current subgraph state containing code_description, file_path and aspects
        
    Returns:
        Empty dict as state updates come from tool calls
    """
    file_path = state.get("file_path")
    code_description = state.get("code_description")
    aspects = state.get("aspects", [])  # Get aspects directly from state
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
    intervention = state.get("intervention", "Unknown intervention")
    research_question = state.get("research_question", "")
    case_id = state.get("case_id", "unknown")
    doc_name = os.path.basename(file_path)
    
    # Get LLM from config
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
        llm_with_tools.invoke(messages, config=runnable_config)
        logging.info(f"[{node_name}] Successfully processed file {file_path} for code {code_description}")
        return {}  # Tool calls will update the state
    except Exception as e:
        logging.error(f"[{node_name}] Error processing file {file_path}: {e}", exc_info=True)
        return {}