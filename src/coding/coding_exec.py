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
from coding_utils import (
    path_to_text, 
    visualize_graph, 
    save_final_markdown,
    generate_markdown
)
from coding_prompt import (
    coding_agent_prompt_header,
    coding_agent_prompt_codes,
    coding_agent_prompt_footer,
    text_to_code_prompt,
    combine_code_and_research_question_prompt
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
    This function takes the combine_code_and_research_question_prompt and fills it with the research question.
    """
    combine_code_and_research_question = combine_code_and_research_question_prompt.format(
        research_question=state['research_question']
    )
    # Store the formatted header in the state
    return {"combine_code_and_research_question": combine_code_and_research_question}

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
                                    + coding_agent_prompt_codes.format(code=c)
                                    + coding_agent_prompt_footer,
                "charity_id": state['charity_id'],
                "charity_directory": state['charity_directory'],
                "code": c,
                "doc_text": d
            }
        )
        for c in state['code_list']
        for d in doc_text_list
    ]

def output_to_markdown(state: CodingAgentState) -> CodingAgentOutputState:
    """
    This function generates the markdown output from the collected results.
    """
    markdown_doc = generate_markdown(state['list_output_per_code_per_doc'])
    return {"markdown_output": markdown_doc}

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

    # This is the first (and presumably only) tool call in result
    if result.tool_calls:
        tool_call = result.tool_calls[0]['args']['quote']
        print("Tool Call: ", tool_call)

        # Return the structured JSON string so it can be aggregated
        structured_output = {
            "code": state['code'],
            "charity_id": state['charity_id'],
            "quote": tool_call,
            "reasoning": result.tool_calls[0]['args']['reasoning']
        }
        return {"list_output_per_code_per_doc": [structured_output]}
    else:
        # If no tool call was made, fallback
        print("No tool call was made")
        return {"list_output_per_code_per_doc": [result.content]}




main_graph = StateGraph(CodingAgentState, output=CodingAgentOutputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_prompt',invoke_prompt)
main_graph.add_node("structure_answer", ToolNode(tools))
main_graph.add_node('output_to_markdown_node', output_to_markdown)

# add the edge for the main graph
main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges('fill_info_prompt_node', continue_to_invoke_prompt, ['invoke_prompt'])
main_graph.add_edge('invoke_prompt', 'structure_answer')
main_graph.add_edge('structure_answer', 'output_to_markdown_node')
main_graph.add_edge('output_to_markdown_node', END)


main_graph = main_graph.compile()

def main():
    # Hardcode the CodingAgentInputState
    charity_id = 'GiveDirectly'
    charity_overview = "Its social goal is 'Extreme poverty'. Its intervention is 'Distribution of wealth transfers'."
    charity_directory = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/storage/nougat_extracted_text/01_GiveDirectly"
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

    # Run the main graph
    
    main_graph.invoke(input_state)

    # Save the output to a markdown file
    # output_filepath = os.path.join('output_directory', 'final_output.md')  # Replace 'output_directory' with the desired path
    # save_final_markdown(output_filepath, result['output'])

    # Visualize the graph
    visualize_graph(main_graph, "coding_graph")

if __name__ == "__main__":
    main()
