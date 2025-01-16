import os
from dotenv import load_dotenv
from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.constants import Send
from coding_state import (
    CodingAgentState,
    CodingAgentOutputState,
    AgentPerCodeState,
    StructuredOutputPerCode
)
from coding_utils import path_to_text, visualize_graph, save_final_markdown
from coding_prompt import (
    coding_agent_prompt_header,
    coding_agent_prompt_codes,
    coding_agent_prompt_footer,
    text_to_code_prompt
)

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

# Load environment variables from .env file
load_dotenv()

# initialize the LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)

# This is the LLM with JSON mode
llm_json_mode = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0,
    response_format={"type": "json_object"}
)

# This is the LLM with tools
llm_with_tools = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)

tools = [StructuredOutputPerCode]

llm_with_tools = llm_with_tools.bind_tools(tools, tool_choice="any")

def fill_info_prompt(state: CodingAgentState):
    """
    This function takes the generic prompt header and fills it with the charity and research specific information.
    """
    prompt_with_charity_research_information = coding_agent_prompt_header.format(
        project_description=state['project_description'],
        charity_overview=f"{state['charity_id']}: {state['charity_overview']}",
        research_question=state['research_question']
    )
    # Store the formatted header in the state
    return {"prompt_for_project": prompt_with_charity_research_information}

def continue_to_invoke_prompt(state: CodingAgentState):
    """
    This function sends the formatted prompt to the subgraph to invoke the prompt per code per document.
    """
    prompt_with_charity_research_information = state['prompt_for_project']

    doc_path_list = []
    doc_text_list = []

    for root, dirs, files in os.walk(state['charity_directory']):
        for file in files:
            if file.endswith('.md'):
                doc_path = os.path.join(root, file)
                doc_path_list.append(doc_path)
                doc_text = path_to_text(doc_path)
                doc_text_list.append(doc_text)

    return [
        Send(
            "invoke_prompt",
            {
                "prompt_per_code": prompt_with_charity_research_information
                                    + coding_agent_prompt_codes.replace("$$code$$", c)
                                    + coding_agent_prompt_footer,
                "charity_directory": state['charity_directory'],
                "doc_text": d
            }
        )
        for c in state['code_list']
        for d in doc_text_list
    ]

def invoke_prompt(state: AgentPerCodeState):
    """
    This function takes in the full prompt and invokes the LLM (with bound tools) for each document.
    We then parse the resulting tool call into the structured schema.
    """
    system_message = SystemMessage(content=state['prompt_per_code'])
    # text_to_code_prompt must only have placeholders for {text}.
    human_message = HumanMessage(content=text_to_code_prompt.format(text=state['doc_text']))

    # Make the LLM call using the model bound with the StructuredOutputPerCode tool
    result = llm_with_tools.invoke([system_message, human_message])

    print('TESTING TOOLS')
    # This is the first (and presumably only) tool call in result
    if result.tool_calls:
        tool_call = result.tool_calls[0]
        print("Tool Call: ", tool_call)

        # Parse arguments into our structured schema
        # "args" is a dict with keys matching StructuredOutputPerCode fields
        structured_data = StructuredOutputPerCode(**tool_call["args"])
        # Convert to JSON (or keep as a Python object)
        structured_json_str = structured_data.json(indent=2)
        print("Parsed structured data: ", structured_json_str)

        # Return the structured JSON string so it can be aggregated
        return {"list_output_per_code_per_doc": [structured_json_str]}
    else:
        # If no tool call was made, fallback
        return {"list_output_per_code_per_doc": [result.content]}

def aggregate_all_results(state: CodingAgentState) -> CodingAgentOutputState:
    """
    This function aggregates all the structured results 
    from each code/doc invocation.
    """
    output_per_code = ''.join(state['list_output_per_code_per_doc'])
    return {"output_per_code": output_per_code}



main_graph = StateGraph(CodingAgentState, output=CodingAgentOutputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_prompt',invoke_prompt)
main_graph.add_node("structure_answer", ToolNode(tools))
main_graph.add_node('aggregate_all_results_node', aggregate_all_results)

# add the edge for the main graph
main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges('fill_info_prompt_node', continue_to_invoke_prompt, ['invoke_prompt'])
main_graph.add_edge('invoke_prompt', 'structure_answer')
main_graph.add_edge('structure_answer', 'aggregate_all_results_node')
main_graph.add_edge('aggregate_all_results_node', END)


main_graph = main_graph.compile()

def main():
    # Hardcode the CodingAgentInputState
    charity_id = 'GiveDirectly'
    charity_overview = "Its social goal is 'Extreme poverty'. Its intervention is 'Distribution of wealth transfers'."
    charity_directory = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/storage/nougat_extracted_text/01_GiveDirectly"
    research_question = "What operational processes enable charities to be cost effective?"
    project_description = (
        "In this research project, each case focuses on a charity known for its cost-effectiveness, "
        "i.e., its ability to pursue its social mission at a low cost.\n\n"
        "Each case contains numerous data sources, including interview notes, third party assessments, "
        "webpages from a charity website and other data sources.\n\n"
        "Each charity is seeking to address a social cause and it does so by implementing its intervention(s)."
    )
    code_list = [
        "Calibrating the approach: Changing the charity's intervention depending on the specifics of the location."
    ]

    input_state = {
        'charity_id': charity_id,
        'charity_overview': charity_overview,
        'charity_directory': charity_directory,
        'research_question': research_question,
        'project_description': project_description,
        'prompt_for_project': '',  # Will be populated later
        'code_list': code_list  # Replace with actual code list
    }

    # Run the main graph
    
    main_graph.invoke(input_state)

    # Save the output to a markdown file
    # output_filepath = os.path.join('output_directory', 'final_output.md')  # Replace 'output_directory' with the desired path
    # save_final_markdown(output_filepath, result['output'])

    # Visualize the graph
    visualize_graph(main_graph, "coding_graph")

if __name__ == "__main__":
    main()
