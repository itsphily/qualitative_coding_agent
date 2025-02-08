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

from coding_state_new import (
    InvokePromptInputState,
    InvokePromptState,
    CodingAgentState,
    CodingAgentOutputState,
    InvokePromptPerCodeState,
    StructuredOutputPerCode
)
from coding_utils import (
    path_to_text,
    visualize_graph,
    save_final_markdown,
    path_to_doc_name,
    generate_markdown
)
from coding_utils import path_to_text, visualize_graph, save_final_markdown
from coding_prompt import (
    combine_code_and_research_question_prompt,
    coding_agent_prompt,
    text_to_code_prompt,
    coding_agent_prompt_footer
)
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

# Load environment variables from .env file
load_dotenv()

model = "deepseek-reasoner"
tools = [StructuredOutputPerCode]
model_openai = "o3-mini"

# initialize the LLM
llm = ChatOpenAI(
    model=model,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)
# This is the LLM with JSON mode
llm_json_mode = ChatOpenAI(
    model=model,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)

# This is the LLM with tools
llm_with_tools = ChatOpenAI(
    model=model,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)

llm_with_tools = llm_with_tools.with_structured_output(StructuredOutputPerCode)


llm_o3 = ChatOpenAI(
    model = model_openai,
    reasoning_effort="high"
)

llm_o3_with_tools = ChatOpenAI(
    model= model_openai,
    reasoning_effort="high"
)


llm_o3_with_tools = llm_o3_with_tools.bind_tools(tools, tool_choice="any")

llm_o3_with_structured_output = llm_o3_with_tools.with_structured_output(StructuredOutputPerCode)


def fill_info_prompt(state: CodingAgentState):
    """
    This function takes the generic prompt header and fills it with the research question.
    """
    code_and_research_question_prompt_variable = combine_code_and_research_question_prompt.format(
        research_question=state['research_question']
    )
    return {"code_and_research_question_prompt_variable": code_and_research_question_prompt_variable}

def continue_to_invoke_subgraph_research_question(state: CodingAgentState):
    """
    This function sends the formatted prompt to the subgraph to invoke the prompt per code per document.
    """
    code_and_research_question_prompt_variable = state['code_and_research_question_prompt_variable']

    return [
        Send(
            "invoke_subgraph_node",
            {
                "code_and_research_question_prompt_variable": code_and_research_question_prompt_variable + "<code>" + c + "</code>",
                "charity_id": state['charity_id'],
                "charity_directory": state['charity_directory'],
                "code": c,
            }
        )
        for c in state['code_list']
    ]

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
                "doc_text": path_to_text(d)
            }
        )
        for d in doc_path_list
    ]

def invoke_prompt(state:InvokePromptPerCodeState):
    """
    This function invokes the LLM with the prepared prompt for each document.
    """
    system_message = SystemMessage(content=state['prompt_per_code'])
    human_message = HumanMessage(content=text_to_code_prompt.format(text=state['doc_text']))
    data_list = []

    try:
        result = llm_o3_with_structured_output.invoke([system_message, human_message])
        
        # Assuming result is a dict with keys "quote_reasoning_pairs" and "document_importance"
        for pair in result.quote_reasoning_pairs:
            data = {
                "code": state['code'],
                "charity_id": state["charity_id"],
                "doc_name": state["doc_name"],
                "quote": pair["quote"],
                "reasoning": pair["reasoning"],
                "document_importance": result["document_importance"]
            }
            data_list.append(data)
                    
    except Exception as e:
        # Log the error but continue processing
        logging.warning(f"Error processing document {state['doc_name']}: {str(e)}")
        # Return empty list to allow processing to continue
        data_list = []

    return {"prompt_per_code_results": data_list, "unprocessed_documents": unprocessed_documents}



def output_to_markdown(state: CodingAgentState) -> CodingAgentOutputState:
    """
    This function generates the markdown output from the collected results.
    """
    markdown_doc = generate_markdown(state['prompt_per_code_results'], state['unprocessed_documents'])
    # Save the output to a markdown file
    save_final_markdown('final_output.md', markdown_doc)
    
    return {"markdown_output": markdown_doc}

# Define the subgraph
invoke_subgraph = StateGraph(InvokePromptState, input=InvokePromptInputState)
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
main_graph = StateGraph(CodingAgentState, output=CodingAgentOutputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_subgraph_node', invoke_subgraph.compile())
main_graph.add_node('output_to_markdown_node', output_to_markdown)

main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges(
    'fill_info_prompt_node',
    continue_to_invoke_subgraph_research_question,
    ['invoke_subgraph_node']
)
main_graph.add_edge('invoke_subgraph_node', 'output_to_markdown_node')
main_graph.add_edge('output_to_markdown_node', END)

main_graph = main_graph.compile()


def main():
    # Hardcode the CodingAgentInputState
    charity_id = 'GiveDirectly'
    charity_overview = "Its social goal is 'Extreme poverty'. Its intervention is 'Distribution of wealth transfers'."
    charity_directory = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/storage/nougat_extracted_text/01_GiveDirectly_short"
    research_question = "What operational processes enable charities to be cost effective?"
    code_list = [
        "Calibrating the approach: Changing the charity's intervention depending on the specifics of the location."
    ]

    input_state = {
        'charity_id': charity_id,
        'charity_overview': charity_overview,
        'charity_directory': charity_directory,
        'research_question': research_question,
        'prompt_for_project': '',  # Will be populated later
        'code_list': code_list  # Replace with actual code list
    }


    # Visualize the graph
    visualize_graph(main_graph, "coding_graph")
    # Run the main graph
    main_graph.invoke(input_state)



if __name__ == "__main__":
    main()
