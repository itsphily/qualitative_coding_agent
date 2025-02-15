import os
from dotenv import load_dotenv
from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.constants import Send
import json
import logging
from datetime import datetime
from langgraph.checkpoint.memory import MemorySaver
import json

# Create debug directory if it doesn't exist
debug_dir = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/debug"
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

from langchain_core.output_parsers import JsonOutputParser

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
    SynthesisLayer2PerCodeState,
    SynthesisLayer2PerCharityState
)
from coding_utils import (
    path_to_text,
    visualize_graph,
    save_final_markdown,
    path_to_doc_name,
    generate_markdown, 
    format_results_to_json, 
    transform_qa_results_to_dict,
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
                        "code_and_research_question_prompt_variable": code_and_research_question_prompt_variable + "<code>" + c + "</code>",
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



def qa_quote_reasoning_pairs(state: CodingAgentState, config):
    """
    This function sends the quote-reasoning pairs to the LLM to evaluate whether they are relevant to the research question.
    """
    research_question = config["configurable"].get("research_question")

    # Convert results to JSON string
    json_quote_reasoning_pairs_string = format_results_to_json(state['prompt_per_code_results'])

    system_message = SystemMessage(content=quality_control_prompt.format(research_question=research_question, 
                                                                       QA_output = QA_output_format,
                                                                       QA_feedback_received = QA_feedback_received_format))
    human_message = HumanMessage(content=quote_reasoning_pairs_prompt.format(text=json_quote_reasoning_pairs_string))
    
    result = llm_o3_with_structured_output_qa.invoke([system_message, human_message])
    
    # Transform the list of results into a dictionary
    qa_results_dict = transform_qa_results_to_dict(result.qa_results)
    
    
    return {"prompt_per_code_results": qa_results_dict}


def output_to_markdown(state: CodingAgentState):
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
                "synthesis_layer_1_result": result,
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
        # Each item is expected to have:
        # - "synthesis_layer_1_result": the synthesis text
        # - "synthesis_layer_1_charity_id": the charity identifier
        # - "synthesis_layer_1_code": the code identifier
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
    save_final_markdown("synthesis_for.md", markdown_dict)
    

def continue_to_synthesis_layer_2_per_code(state: CodingAgentState):
    """
    Iterate over state['synthesis_layer_1'] to group and send per-code across charities.
    """
    
    groups = {}
    for key, val in state.get("synthesis_layer_1", {}).items():
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

def synthesis_layer_2_per_code(state: SynthesisLayer2PerCodeState, config):
    system_message = SystemMessage(content=layer_2_code_synthesis_prompt.format(
        research_question=config["configurable"].get("research_question")
    ))
    human_message = HumanMessage(content=text_to_synthesis_layer_2_prompt.format(text=state['synthesis_layer_2_all_charity_text']))
    result = llm_o3.invoke([system_message, human_message])
    return {"synthesis_layer_2_per_code": {
                "synthesis_layer_2_per_code_result": result,
                "synthesis_layer_2_per_code_charity_id": state.get('synthesis_layer_2_code', '')
           }}

def continue_to_synthesis_layer_2_per_charity(state: CodingAgentState):
    """
    Iterate over state['synthesis_layer_1'] grouping by charity,
    then send aggregated JSON string to synthesis_layer_2_per_charity node.
    """
    import json
    groups = {}
    for key, val in state.get("synthesis_layer_1", {}).items():
        charity = val["synthesis_layer_1_charity_id"]
        groups.setdefault(charity, []).append(val)
    sends = []
    for charity, group in groups.items():
        group_json = json.dumps(group, indent=2)
        sends.append(
            Send("synthesis_layer_2_per_charity", {
                "synthesis_layer_2_all_code_text": group_json,
                "synthesis_layer_2_charity_id": charity
            })
        )
    return sends

def synthesis_layer_2_per_charity(state: SynthesisLayer2PerCharityState, config):
    system_message = SystemMessage(content=layer_2_charity_synthesis_prompt.format(
        research_question=config["configurable"].get("research_question")
    ))
    human_message = HumanMessage(content=text_to_synthesis_layer_2_prompt.format(text=state['synthesis_layer_2_all_code_text']))
    result = llm_o3.invoke([system_message, human_message])
    return {"synthesis_layer_2_per_charity": {
                "synthesis_layer_2_per_charity_result": result,
                "synthesis_layer_2_per_charity_code": state['synthesis_layer_2_charity_id']
           }}

def synthesis_output_to_markdown(state):
    """
    Aggregate synthesis_layer_2 outputs and structure as markdown.
    Calls generate_synthesis_markdown for per charity and per code outputs.
    """
    per_charity = state.get("synthesis_layer_2_per_charity", {})
    per_code = state.get("synthesis_layer_2_per_code", {})
    synthesis_md_charity = ""
    for charity, text in per_charity.items():
        synthesis_md_charity += f"## Charity: {charity}\n{text}\n\n"
    synthesis_md_code = ""
    for code, text in per_code.items():
        synthesis_md_code += f"## Code: {code}\n{text}\n\n"
    output_charity = generate_synthesis_markdown(synthesis_md_charity, 'synthesis_output_per_charity', 'coding_output')
    output_code = generate_synthesis_markdown(synthesis_md_code, 'synthesis_output_per_code', 'coding_output')
    return {"synthesis_output_per_charity": output_charity,
            "synthesis_output_per_code": output_code}


def generate_synthesis_output(state: CodingAgentState):
    synthesis_outputs = synthesis_output_to_markdown(state)
    return synthesis_outputs

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
    final_md = generate_synthesis_markdown(result, 'final_report', 'coding_output')
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
main_graph.add_edge('invoke_subgraph_node', 'qa_quote_reasoning_pairs_node')
main_graph.add_edge('qa_quote_reasoning_pairs_node', 'output_to_markdown_node')

main_graph.add_conditional_edges('output_to_markdown_node', continue_to_synthesis_layer_1, ['synthesis_layer_1_node'])
main_graph.add_edge('synthesis_layer_1_node', 'synthesis_layer_1_to_markdown_node')
main_graph.add_conditional_edges('synthesis_layer_1_to_markdown_node',continue_to_synthesis_layer_2_per_code, ['synthesis_layer_2_per_code_node'])
main_graph.add_conditional_edges('synthesis_layer_1_to_markdown_node',continue_to_synthesis_layer_2_per_charity, ['synthesis_layer_2_per_charity_node'])
main_graph.add_edge('synthesis_layer_2_per_charity_node', 'synthesis_output_to_markdown_node')
main_graph.add_edge('synthesis_output_to_markdown_node', 'final_report_node')
main_graph.add_edge('final_report_node', END)

checkpointer = MemorySaver()
main_graph = main_graph.compile(checkpointer=checkpointer)


def main():
    # Hardcode the CodingAgentInputState

    research_question = "What operational processes enable charities to be cost effective?"
    code_list = [
        "Calibrating the approach: Changing the charity's intervention depending on the specifics of the location.",
        "Pre-intervention data collection: Collecting information about the charitable cause before implementing the charity's intervention."
    ]

    charities = [
        {
            "charity_id": 'GiveDirectly',
            "charity_overview": "Its social goal is 'Extreme poverty'. Its intervention is 'Distribution of wealth transfers'.",
            "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/storage/nougat_extracted_text/01_GiveDirectly_short"
        },
        {
            "charity_id": "MalariaConsortium",
            "charity_overview": "Its social goal is 'Malaria'. Its intervention is 'Distribution of seasonal malaria chemoprevention'.",
            "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/04_Malaria_Consortium short"
        }
    ]

    input_state = {
         "charities": charities,
         "research_question": research_question,
         "code_list": code_list,
    }

    # Define the config that includes the research question
    config = {"configurable": {"thread_id": "1", 
                            "research_question": "What operational processes enable charities to be cost effective?"}
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

