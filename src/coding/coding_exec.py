import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.constants import Send
import json
import logging
from datetime import datetime
from langgraph.checkpoint.memory import MemorySaver
import argparse

# Create debug directory if it doesn't exist, configurable via DEBUG_DIR env var
debug_dir = os.getenv("DEBUG_DIR", "debug")
os.makedirs(debug_dir, exist_ok=True)

# Configure logging to write to both file and console
debug_file = os.path.join(debug_dir, f'debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(debug_file),
        logging.StreamHandler()  # This will maintain console output
    ]
)

# Log the start of the script
logging.info(f"Starting script execution. Debug log file: {debug_file}")


from coding_state import (
    InvokePromptInputState,
    InvokePromptState,
    CodingAgentState,
    InvokePromptPerCodeState,
    StructuredOutputPerCode,
    CodingAgentInputState,
    InvokePromptOutputState,
    QAStructuredOutputPerCode,
    SynthesisLayer1State,
    SynthesisLayer2PerCodeInputState,
    SynthesisLayer2PerCharityInputState,
    QAQuoteReasoningPairsSubState
)
from coding_utils import (
    path_to_text,
    visualize_graph,
    save_final_markdown,
    path_to_doc_name,
    generate_markdown, 
    format_results_to_json, 
    transform_qa_results_to_list,
    generate_synthesis_markdown
)

from coding_prompt import (
    combine_code_and_research_question_prompt,
    coding_agent_prompt,
    text_to_code_prompt,
    coding_agent_prompt_footer,
    quality_control_prompt,
    quote_reasoning_pairs_prompt,
    QA_output_format,
    QA_feedback_received_format,
    layer_1_synthesis_prompt,
    layer_2_code_synthesis_prompt,
    layer_2_charity_synthesis_prompt,
    final_layer_research_question_prompt,
    text_to_synthesis_prompt,
    text_to_synthesis_layer_2_prompt,
    text_to_synthesis_final_report_prompt
)
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

# Load environment variables from .env file
load_dotenv()

# Define model and tools
model_openai = "o3-mini"
tools = [StructuredOutputPerCode]
tools_qa = [QAStructuredOutputPerCode]

# Base LLM without tools
llm_o3 = ChatOpenAI(
    model=model_openai,
    reasoning_effort="high"
)

# LLM with tools for coding agent
llm_o3_with_tools = ChatOpenAI(
    model=model_openai, 
    reasoning_effort="high"
)
llm_o3_with_structured_output = llm_o3_with_tools.with_structured_output(StructuredOutputPerCode)

# LLM with tools for QA agent
llm_o3_with_tools_qa = ChatOpenAI(
    model=model_openai,
    reasoning_effort="high"
)
llm_o3_with_structured_output_qa = llm_o3_with_tools_qa.with_structured_output(QAStructuredOutputPerCode)


def fill_info_prompt(state: CodingAgentInputState):
    """
    This function takes the generic prompt header and fills it with the research question.
    """

def continue_to_invoke_subgraph_research_question(state: CodingAgentInputState) -> CodingAgentState:
    code_and_research_question_prompt_variable = combine_code_and_research_question_prompt.format(
        research_question=state['research_question']
    )
    sends = []
    for charity in state['charities']:
        for c in state['code_list']:
            sends.append(
                Send(
                    "invoke_subgraph_node",
                    {
                        "code_and_research_question_prompt_variable": f"{code_and_research_question_prompt_variable}<code>{c}</code>",
                        "charity_id": charity["charity_id"],
                        "charity_directory": charity["charity_directory"],
                        "code": c,
                    }
                )
            )
    return sends

def combine_code_and_research_question_function(state: InvokePromptInputState) -> InvokePromptState:
    """
    This function combines the code and research question into a more specific research question.
    """
    result = llm_o3.invoke([HumanMessage(content=state['code_and_research_question_prompt_variable'])])

    return {
        "research_question_with_code": result.content,
        "charity_id": state['charity_id'],
        "charity_directory": state['charity_directory'],
        "code": state['code']
    }


def continue_invoke_research_question(state: InvokePromptState):
    """
    This function sends the formatted prompt to invoke the prompt per code per document.
    """
    prompt = coding_agent_prompt.format(
        research_question=state['research_question_with_code'],
        project_specific_instructions="It is important to distinguish between actions, processes or activities that happened before, during or after the intervention. For example when asked to find quotes for Pre-intervention data collection, you must only include quotes from the data that were collected before the intervention. Use the context to determine when the action, process or activity happened.",
    ) + coding_agent_prompt_footer

    doc_path_list = []

    for root, dirs, files in os.walk(state['charity_directory']):
        for file in files:
            if file.endswith('.md'):
                doc_path = os.path.join(root, file)
                doc_path_list.append(doc_path)

    return [
        Send(
            "invoke_research_question_prompt_node",
            {
                "prompt_per_code": prompt,
                "code": state['code'],
                "charity_id": state['charity_id'],
                "doc_name": path_to_doc_name(d),
                "doc_path": d,
                "doc_text": path_to_text(d)
            }
        )
        for d in doc_path_list
    ]

def invoke_prompt(state:InvokePromptPerCodeState) -> InvokePromptOutputState:
    """
    This function invokes the LLM with the prepared prompt for each document.
    """
    system_message = SystemMessage(content=state['prompt_per_code'])
    human_message = HumanMessage(content=text_to_code_prompt.format(text=state['doc_text']))
    data_list = []
    unprocessed_documents = []    
    try:
        result = llm_o3_with_structured_output.invoke([system_message, human_message])
        # Assuming result is a dict with keys "quote_reasoning_pairs" and "document_importance"
        if result.quote_reasoning_pairs:
            # If there are quote-reasoning pairs, process them as before
            for quote,reasoning in result.quote_reasoning_pairs:
                data = {
                    "code": state['code'],
                    "charity_id": state['charity_id'],
                    "doc_path": state['doc_path'],
                    "doc_name": state['doc_name'],
                    "quote": quote[1],
                    "reasoning": reasoning[1],
                    "document_importance": result.document_importance
                }
                data_list.append(data)
        else:
            # If no quote-reasoning pairs, still add a document entry for importance tracking
            data = {
                "code": state['code'],
                "charity_id": state['charity_id'],
                "doc_path": state['doc_path'],
                "doc_name": state['doc_name'],
                "quote": "",
                "reasoning": "",
                "document_importance": result.document_importance
            }
            data_list.append(data)
                    
    except Exception as e:
        # Log the error but continue processing
        logging.warning(f"Error processing document {state['doc_name']}: {str(e)}")
        unprocessed_documents.append(state["doc_name"])

    return {"prompt_per_code_results": data_list, "unprocessed_documents": unprocessed_documents}


# function to split prompt_per_code_results into subsets via Send
def continue_to_qa_quote_reasoning_pairs(state: CodingAgentState):
    """
    Use the Send API to partition the prompt_per_code_results by charity and code.
    Each Send sends a subset of quote–reasoning pairs (all results for a given charity and code)
    to the qa_quote_reasoning_pairs_subnode.
    """
    groups = {}
    for item in state.get("prompt_per_code_results", []):
        key = (item.get("charity_id"), item.get("code"))
        groups.setdefault(key, []).append(item)
    sends = []
    for (charity_id, code), subset in groups.items():
        sends.append(
            Send("qa_quote_reasoning_pairs_node", {
                "subset_prompt_per_code_results": subset,
                "charity_id": charity_id,
                "code": code
            })
        )
    return sends

# QA function to process each subset
def qa_quote_reasoning_pairs(state: QAQuoteReasoningPairsSubState, config):
    """
    This node processes a subset of prompt_per_code_results corresponding to a specific charity and code.
    It uses the send API to receive only the quote–reasoning pairs for that group.
    """
    research_question = config["configurable"].get("research_question")
    # Convert the subset to JSON string using your formatting helper.
    json_quote_reasoning_pairs_string = format_results_to_json(state["subset_prompt_per_code_results"])
    
    system_message = SystemMessage(content=quality_control_prompt.format(
        research_question=research_question,
        QA_output=QA_output_format,
        QA_feedback_received=QA_feedback_received_format
    ))
    human_message = HumanMessage(content=quote_reasoning_pairs_prompt.format(text=json_quote_reasoning_pairs_string))
    
    # Invoke the QA LLM with structured output
    result = llm_o3_with_structured_output_qa.invoke([system_message, human_message])
    
    # Transform the returned list of QAValuePerCode objects into your desired dictionary format.
    qa_results = transform_qa_results_to_list(result.qa_results)
    
    # Return the result using an annotated key so that when merged back into the overall state,
    # the lists from each Send are combined without collision.
    return {"qa_results": qa_results}


def output_to_markdown(state: CodingAgentState):
    state['prompt_per_code_results'] = state['qa_results'] 
    markdown_output = generate_markdown(state['prompt_per_code_results'], state['unprocessed_documents'])
    save_final_markdown("quote_reasoning_output.md", markdown_output)
    return {"markdown_output": markdown_output}

def continue_to_synthesis_layer_1(state: CodingAgentState):
    groups = {}
    # Loop over each result and only process dictionaries
    for item in state["prompt_per_code_results"]:
        if not isinstance(item, dict):
            logging.warning(f"Skipping unexpected item of type {type(item)}: {item}")
            continue
        # Group by charity_id and code
        key = (item.get("charity_id"), item.get("code"))
        groups.setdefault(key, []).append(item)
    
    sends = []
    # For each group, combine the quotes and reasoning
    for (charity, code), items in groups.items():
        combined_text = ""
        for entry in items:
            quote = entry.get("quote", "").strip()
            reasoning = entry.get("reasoning", "").strip()
            # Only add if there is at least some text
            if quote or reasoning:
                combined_text += f"Quote: {quote}\nReasoning: {reasoning}\n\n"
        combined_text = combined_text.strip()  # remove extra whitespace
        sends.append(
            Send("synthesis_layer_1_node", {
                "synthesis_layer_1_text": combined_text,
                "synthesis_layer_1_charity_id": charity,
                "synthesis_layer_1_code": code,
            })
        )
    return sends
    
def synthesis_layer_1(state: SynthesisLayer1State, config):
    """
    Invoke LLM to do per-code per-charity synthesis.
    """
    system_message = SystemMessage(content=layer_1_synthesis_prompt.format(
        research_question=config["configurable"].get("research_question")
    ))
    human_message = HumanMessage(content=text_to_synthesis_prompt.format(text=state['synthesis_layer_1_text']))
    result = llm_o3.invoke([system_message, human_message])
    
    return {"synthesis_layer_1": [{
                "synthesis_layer_1_result": result.content,
                "synthesis_layer_1_charity_id": state['synthesis_layer_1_charity_id'],
                "synthesis_layer_1_code": state['synthesis_layer_1_code']
           }]}


def synthesis_layer_1_to_markdown(state: CodingAgentState) -> dict:
    """
    Aggregates the list of SynthesisLayer1State objects by charity.
    For each charity, groups the synthesis texts by their code and produces a markdown string of the form:
    
    # Code1
    synthesis_layer_1_text for Code1
    
    # Code2
    synthesis_layer_1_text for Code2
    
    Returns:
        dict: A dictionary with the key "synthesis_layer_1_markdown" mapping to a dict of {charity_id: markdown_string}.
    """
    # Retrieve the synthesis_layer_1 list from the state.
    synthesis_list = state.get("synthesis_layer_1", [])
    
    # Create a nested dictionary: charity_id -> code -> aggregated text
    charity_groups = {}
    for item in synthesis_list:
        charity = item.get("synthesis_layer_1_charity_id")
        code = item.get("synthesis_layer_1_code")
        result_text = item.get("synthesis_layer_1_result")
        
        # Skip items missing any of these
        if not (charity and code and result_text):
            continue
        
        if charity not in charity_groups:
            charity_groups[charity] = {}
        # If the same code appears more than once for the charity, concatenate the texts.
        if code in charity_groups[charity]:
            charity_groups[charity][code] += "\n" + result_text
        else:
            charity_groups[charity][code] = result_text
    
    # Build the markdown string for each charity.
    markdown_dict = {}
    for charity, codes in charity_groups.items():
        md_lines = []
        for code, combined_text in codes.items():
            md_lines.append(f"# {code}\n{combined_text}\n")
        # Join all sections with newlines.
        markdown_dict[charity] = "\n".join(md_lines).strip()
    
    # Save the markdown files using your utility function.
    save_final_markdown("per_code_analysis_for.md", markdown_dict)
    

def continue_to_synthesis_layer_2_per_code(state: CodingAgentState):
    """
    Iterate over state['synthesis_layer_1'] (a list) to group and send per-code across charities.
    """
    groups = {}
    for val in state.get("synthesis_layer_1", []):
        group_key = val["synthesis_layer_1_code"]
        groups.setdefault(group_key, []).append(val)
    sends = []
    for code, group in groups.items():
        group_json = json.dumps(group, indent=2)
        sends.append(
            Send("synthesis_layer_2_per_code_node", {
                "synthesis_layer_2_all_charity_text": group_json,
                "synthesis_layer_2_code": code
            })
        )
    return sends

def synthesis_layer_2_per_code(state: SynthesisLayer2PerCodeInputState, config):
    system_message = SystemMessage(content=layer_2_code_synthesis_prompt.format(
        research_question=config["configurable"].get("research_question")
    ))
    human_message = HumanMessage(content=text_to_synthesis_layer_2_prompt.format(text=state['synthesis_layer_2_all_charity_text']))
    result = llm_o3.invoke([system_message, human_message])
    return {"synthesis_layer_2_per_code": [{
                "synthesis_layer_2_per_code_result": result.content,
                "synthesis_layer_2_code": state['synthesis_layer_2_code']
           }]}

def continue_to_synthesis_layer_2_per_charity(state: CodingAgentState):
    """
    Iterate over state['synthesis_layer_1'] grouping by charity,
    then send aggregated JSON string to synthesis_layer_2_per_charity node.
    """
    groups = {}
    for val in state.get("synthesis_layer_1", []):
        charity = val["synthesis_layer_1_charity_id"]
        groups.setdefault(charity, []).append(val)
    sends = []
    for charity, group in groups.items():
        group_json = json.dumps(group, indent=2)
        sends.append(
            Send("synthesis_layer_2_per_charity_node", {
                "synthesis_layer_2_all_code_text": group_json,
                "synthesis_layer_2_charity_id": charity
            })
        )
    return sends

def synthesis_layer_2_per_charity(state: SynthesisLayer2PerCharityInputState, config):
    system_message = SystemMessage(content=layer_2_charity_synthesis_prompt.format(
        research_question=config["configurable"].get("research_question")
    ))
    human_message = HumanMessage(content=text_to_synthesis_layer_2_prompt.format(text=state['synthesis_layer_2_all_code_text']))
    result = llm_o3.invoke([system_message, human_message])
    return {"synthesis_layer_2_per_charity": [{
                "synthesis_layer_2_per_charity_result": result.content,
                "synthesis_layer_2_charity_id": state['synthesis_layer_2_charity_id']
           }]}

def synthesis_output_to_markdown(state: CodingAgentState):
    """
    Aggregate synthesis_layer_2 outputs and structure as markdown.
    Calls generate_synthesis_markdown for per charity and per code outputs.
    """
    # Get the lists from state (default to empty lists)
    per_charity_list = state.get("synthesis_layer_2_per_charity", [])
    per_code_list = state.get("synthesis_layer_2_per_code", [])
    
    # Group the per-charity results by charity_id
    charity_dict = {}
    for item in per_charity_list:
        charity = item.get("synthesis_layer_2_charity_id")
        result_text = item.get("synthesis_layer_2_per_charity_result", "")
        if charity:
            charity_dict.setdefault(charity, "")
            charity_dict[charity] += "\n" + result_text
    
    # Group the per-code results by code
    code_dict = {}
    for item in per_code_list:
        code = item.get("synthesis_layer_2_code")
        result_text = item.get("synthesis_layer_2_per_code_result", "")
        if code:
            code_dict.setdefault(code, "")
            code_dict[code] += "\n" + result_text

    # Build markdown strings
    synthesis_md_charity = ""
    for charity, text in charity_dict.items():
        synthesis_md_charity += f"## Charity: {charity}\n{text.strip()}\n\n"

    synthesis_md_code = ""
    for code, text in code_dict.items():
        synthesis_md_code += f"## Code: {code}\n{text.strip()}\n\n"

    output_charity = generate_synthesis_markdown(synthesis_md_charity, 'synthesis_output_per_charity', 'coding_output')
    output_code = generate_synthesis_markdown(synthesis_md_code, 'synthesis_output_per_code', 'coding_output')
    
    return {"synthesis_output_per_charity": output_charity,
            "synthesis_output_per_code": output_code}


def final_report(state: CodingAgentState, config):
    """
    Generate a final comprehensive synthesis report.
    """
    system_message = SystemMessage(content=final_layer_research_question_prompt.format(
        research_question=config["configurable"].get("research_question")
    ))
    human_message = HumanMessage(content=text_to_synthesis_final_report_prompt.format(
        per_charity_aggregated_outputs=state['synthesis_output_per_charity'],
        per_code_aggregated_outputs=state['synthesis_output_per_code']
    ))
    result = llm_o3.invoke([system_message, human_message])
    final_md = generate_synthesis_markdown(result.content, 'final_report', 'coding_output')
    return {"final_report_result": final_md}




# Define the subgraph
invoke_subgraph = StateGraph(InvokePromptState, input=InvokePromptInputState, output=InvokePromptOutputState)
invoke_subgraph.add_node("combine_code_and_research_question_prompt_node", combine_code_and_research_question_function)
invoke_subgraph.add_node("invoke_research_question_prompt_node", invoke_prompt)

invoke_subgraph.add_edge(START, "combine_code_and_research_question_prompt_node")
invoke_subgraph.add_conditional_edges(
    "combine_code_and_research_question_prompt_node",
    continue_invoke_research_question,
    ["invoke_research_question_prompt_node"]
)
invoke_subgraph.add_edge("invoke_research_question_prompt_node", END)

# Define the main graph
main_graph = StateGraph(CodingAgentState, input = CodingAgentInputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_subgraph_node', invoke_subgraph.compile())
main_graph.add_node('qa_quote_reasoning_pairs_node', qa_quote_reasoning_pairs)
main_graph.add_node('output_to_markdown_node', output_to_markdown)
main_graph.add_node('synthesis_layer_1_node', synthesis_layer_1)
main_graph.add_node('synthesis_layer_1_to_markdown_node', synthesis_layer_1_to_markdown)
main_graph.add_node('synthesis_layer_2_per_code_node', synthesis_layer_2_per_code)
main_graph.add_node('synthesis_layer_2_per_charity_node', synthesis_layer_2_per_charity)
main_graph.add_node('synthesis_output_to_markdown_node', synthesis_output_to_markdown)
main_graph.add_node('final_report_node', final_report)

# Define the edges
main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges(
    'fill_info_prompt_node',
    continue_to_invoke_subgraph_research_question,
    ['invoke_subgraph_node']
)
main_graph.add_conditional_edges('invoke_subgraph_node', continue_to_qa_quote_reasoning_pairs, ['qa_quote_reasoning_pairs_node'])
main_graph.add_edge('qa_quote_reasoning_pairs_node', 'output_to_markdown_node')

main_graph.add_conditional_edges('output_to_markdown_node', continue_to_synthesis_layer_1, ['synthesis_layer_1_node'])
main_graph.add_edge('synthesis_layer_1_node', 'synthesis_layer_1_to_markdown_node')
main_graph.add_conditional_edges('synthesis_layer_1_to_markdown_node',continue_to_synthesis_layer_2_per_code, ['synthesis_layer_2_per_code_node'])
main_graph.add_conditional_edges('synthesis_layer_1_to_markdown_node',continue_to_synthesis_layer_2_per_charity, ['synthesis_layer_2_per_charity_node'])
main_graph.add_edge('synthesis_layer_2_per_charity_node', 'synthesis_output_to_markdown_node')
main_graph.add_edge('synthesis_layer_2_per_code_node', 'synthesis_output_to_markdown_node')
main_graph.add_edge('synthesis_output_to_markdown_node', 'final_report_node')
main_graph.add_edge('final_report_node', END)

checkpointer = MemorySaver()
main_graph = main_graph.compile(checkpointer=checkpointer)


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the coding agent with specified parameters')
    parser.add_argument('--research_question', type=str, required=True, 
                        help='The research question to investigate')
    parser.add_argument('--code_list', type=str, nargs='+', required=True,
                        help='List of codes to analyze')
    parser.add_argument('--charities', type=json.loads, required=True,
                        help='JSON string containing charity information')
    
    args = parser.parse_args()
    
    # Extract arguments
    research_question = args.research_question
    code_list = args.code_list
    charities = args.charities

    input_state = {
         "charities": charities,
         "research_question": research_question,
         "code_list": code_list,
    }

    # Define the config that includes the research question
    config = {"configurable": {"thread_id": "1", 
                            "research_question": research_question}
                            }

    # Visualize the graph
    visualize_graph(main_graph, "coding_graph")
    # Run the main graph
    main_graph.invoke(input_state, config = config)

    # retrieve the final state 
    final_state = main_graph.get_state(config)
    final_state_dict = final_state.values 

    logging.info("Final State:")
    logging.info(final_state_dict)

    logging.info("Markdown Output:")
    logging.info(final_state_dict.get("markdown_output"))

    logging.info("Prompt per Code Results:")
    logging.info(final_state_dict.get("prompt_per_code_results"))

    logging.info("Unprocessed Documents:")
    logging.info(final_state_dict.get("unprocessed_documents"))


if __name__ == "__main__":
    main()

