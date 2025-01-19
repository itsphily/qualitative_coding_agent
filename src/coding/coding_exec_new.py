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
from coding_state_new import (
    InvokePromptInputState,
    InvokePromptState
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
    coding_agent_prompt_header,
    coding_agent_prompt_header_specific,
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
    This function takes the generic prompt header and fills it with the charity and research specific information.
    """
    code_and_research_question_prompt = combine_code_and_research_question_prompt.format(
        research_question=state['research_question']
    )
    # Store the formatted header in the state
    return {"code_and_research_question_prompt": code_and_research_question_prompt}

def continue_to_research_question(state: CodingAgentState):
    """
    This function sends the formatted prompt to the subgraph to invoke the prompt per code per document.
    """
    combine_code_and_research_question = state['combine_code_and_research_question']

    return [
        Send(
            "invoke_prompt_graph_research_question",
            {
                "combine_code_and_research_question": combine_code_and_research_question + "<code>" + c + "</code>",
                "charity_id": state['charity_id'],
                "charity_directory": state['charity_directory'],
                "code": c,
            }
        )
        for c in state['code_list']
    ]

def combine_code_and_research_question_with_code(state: CodingAgentState):
    """
    This function combines the research question with the code.
    """
    combine_code_and_research_question = state['combine_code_and_research_question']
    return [
        Send(
            "invoke_prompt_graph_research_question",
            {
                "combine_code_and_research_question": combine_code_and_research_question + "<code>" + code + "</code>",
                "charity_id": state['charity_id'],
                "charity_directory": state['charity_directory'],
                "code": code,
            }
        )
        for code in state['code_list']
    ]


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

def fill_info_prompt(state: CodingAgentState):
    """
    This function takes the generic prompt header and fills it with the research question.
    """
    code_and_research_question_prompt = combine_code_and_research_question_prompt.format(
        research_question=state['research_question']
    )
    return {"code_and_research_question_prompt": code_and_research_question_prompt}

def continue_to_invoke_subgraph_research_question(state: CodingAgentState):
    """
    This function sends the formatted prompt to the subgraph to invoke the prompt per code per document.
    """
    combine_code_and_research_question = state['code_and_research_question_prompt']

    return [
        Send(
            "invoke_subgraph_node",
            {
                "combine_code_and_research_question_prompt": combine_code_and_research_question + "<code>" + c + "</code>",
                "charity_id": state['charity_id'],
                "charity_directory": state['charity_directory'],
                "code": c,
            }
        )
        for c in state['code_list']
    ]

def combine_code_and_research_question_prompt(state: InvokePromptInputState) -> InvokePromptState:
    """
    This function combines the code and research question into a more specific research question.
    """
    prompt = combine_code_and_research_question_prompt.format(
        code_description=state['code'],
        research_question=state['combine_code_and_research_question_prompt']
    )

    human_message = HumanMessage(content=prompt)
    result = llm.invoke([human_message])

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
    prompt = coding_agent_prompt_header_specific.format(
        research_question=state['research_question_with_code']
    )

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

def invoke_prompt(state):
    """
    This function invokes the LLM with the prepared prompt for each document.
    """
    system_message = SystemMessage(content=state['prompt_per_code'])
    human_message = HumanMessage(content=text_to_code_prompt.format(text=state['doc_text']))

    result = llm_with_tools.invoke([system_message, human_message])

    if result.tool_calls:
        data = {
            "code": state['code'],
            "charity_id": state["charity_id"],
            "doc_name": state["doc_name"],
            "quote": result.tool_calls[0]['args']['quote'],
            "reasoning": result.tool_calls[0]['args']['reasoning']
        }
        return {"prompt_per_code_results": [data]}
    else:
        print("No tool call was made")
        return {"prompt_per_code_results": []}

def output_to_markdown(state: CodingAgentState) -> CodingAgentOutputState:
    """
    This function generates the markdown output from the collected results.
    """
    markdown_doc = generate_markdown(state['prompt_per_code_results'])
    return {"markdown_output": markdown_doc}

# Define the subgraph
invoke_subgraph = StateGraph(InvokePromptState, input=InvokePromptInputState)
invoke_subgraph.add_node("combine_code_and_research_question_prompt_node", combine_code_and_research_question_prompt)
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
    # Hardcode the CodingAgentState
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
        'code_list': code_list,
        'prompt_per_code_results': []
    }

    # Run the main graph
    result = main_graph.invoke(input_state)

    # Save the output to a markdown file
    save_final_markdown('final_output.md', result['markdown_output'])

    # Visualize the graph
    visualize_graph(main_graph, "coding_graph_new")

if __name__ == "__main__":
    main()






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
