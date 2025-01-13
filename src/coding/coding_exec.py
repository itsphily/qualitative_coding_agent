import os
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.constants import Send
from coding_state import (
    CodingAgentState,
    CodingAgentOutputState,
    CodingAgentInputState,
    AgentPerCodeState,
    AgentPerCodeInputState,
    AgentRunState,
    AgentRunOutputState,
    AgentPerCodeOutputState
)
from coding_utils import path_to_text, visualize_graph, save_final_markdown
from coding_prompt import coding_agent_prompt, text_to_code_prompt

# Initialize LLMs
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1/chat/completions",
    temperature=0.0
)

llm_json_mode = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1/chat/completions",
    temperature=0.0
)
llm_json_mode.bind(response_format={"type": "json_object"})

# Graph for per code per document processing
graph_per_code_per_doc = StateGraph(input=AgentRunState, output=AgentRunOutputState)
graph_per_code_per_doc.add_node('invoke_one_code_prompt_per_doc_node', invoke_one_code_prompt_per_doc)
graph_per_code_per_doc.add_edge(START, 'invoke_one_code_prompt_per_doc_node')
graph_per_code_per_doc.add_edge('invoke_one_code_prompt_per_doc_node', END)

# Graph for per code processing
graph_per_code = StateGraph(input=AgentPerCodeInputState, output=AgentPerCodeOutputState)
graph_per_code.add_node('get_doc_text_node', get_doc_text)
graph_per_code.add_node('graph_per_code_per_doc_node', graph_per_code_per_doc.compile())
graph_per_code.add_node('aggregate_all_results_per_doc_node', aggregate_all_results_per_doc)
graph_per_code.add_edge(START, 'get_doc_text_node')
graph_per_code.add_conditional_edge('get_doc_text_node', continue_invoke_code_prompt, 'graph_per_code_per_doc_node')
graph_per_code.add_edge('graph_per_code_per_doc_node', 'aggregate_all_results_per_doc_node')
graph_per_code.add_edge('aggregate_all_results_per_doc_node', END)

# Main graph
main_graph = StateGraph(input=CodingAgentInputState, output=CodingAgentOutputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('graph_per_code_node', graph_per_code.compile())
main_graph.add_node('aggregate_all_results_node', aggregate_all_results)
main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edge('fill_info_prompt_node', continue_to_invoke_prompt, 'graph_per_code_node')
main_graph.add_edge('graph_per_code_node', 'aggregate_all_results_node')
main_graph.add_edge('aggregate_all_results_node', END)

def fill_info_prompt(state: CodingAgentInputState) -> CodingAgentState:
    """
    This function takes the generic prompt and fills it with the charity and research specific information.
    """
    prompt_with_charity_research_information = coding_agent_prompt.format(
        project_description=state['project_description'],
        charity_overview=f"{state['charity_id']}: {state['charity_overview']}",
        research_question=state['research_question']
    )
    return {"prompt_for_project": prompt_with_charity_research_information}

def continue_to_invoke_prompt(state: CodingAgentState):
    """
    This function sends the generically filled prompt to the subgraph to invoke the prompt per code per doc.
    """
    prompt_with_charity_research_information = state['prompt_for_project']
    return [
        Send(
            "invoke_code_prompt_node",
            {
                "prompt_per_code": prompt_with_charity_research_information.format(code=c),
                "charity_directory": state['charity_directory']
            }
        )
        for c in state['code_list']
    ]

def get_doc_text(state: AgentPerCodeInputState) -> AgentPerCodeState:
    """
    This function reads each text from the files in the directory and appends them to a list.
    """
    doc_path_list = []
    doc_text_list = []

    for root, dirs, files in os.walk(state['charity_directory']):
        for file in files:
            if file.endswith('.md'):
                doc_path = os.path.join(root, file)
                doc_path_list.append(doc_path)
                doc_text = path_to_text(doc_path)
                doc_text_list.append(doc_text)

    return {'doc_text_list': doc_text_list}

def continue_invoke_code_prompt(state: AgentPerCodeState):
    """
    This function takes in the prompt filled with the charity and research specific information,
    iterates over the texts in `doc_text_list`, and uses Send to invoke one prompt per code per document.
    """
    return [
        Send(
            "invoke_one_code_prompt_per_doc_node",
            {
                "prompt_per_code": state["prompt_per_code"],
                "doc_text": d
            }
        )
        for d in state['doc_text_list']
    ]

def invoke_one_code_prompt_per_doc(state: AgentRunState):
    """
    This function takes in the full prompt and invokes the LLM for each document.
    """
    system_message = SystemMessage(content=state['prompt_per_code'])
    human_message = HumanMessage(content=text_to_code_prompt.format(text=state['doc_text']))

    result = llm.invoke([system_message, human_message])

    return {"output_per_code_per_doc": result}

def aggregate_all_results_per_doc(state: AgentPerCodeState) -> AgentPerCodeOutputState:
    """
    This function takes in the list of results from invoking the LLM with one code for each doc,
    and aggregates all the results per code.
    """
    output_per_code = ''.join(state['output_per_code_per_doc'])
    return {"output_per_code": output_per_code}

def aggregate_all_results(state: CodingAgentState) -> CodingAgentOutputState:
    """
    This function takes in the list of results for each code, and aggregates all the results for a final output.
    """
    output = ''.join(state['output_per_code'])
    return {"output": output}

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

    input_state = {
        'charity_id': charity_id,
        'charity_overview': charity_overview,
        'charity_directory': charity_directory,
        'research_question': research_question,
        'project_description': project_description,
        'prompt_for_project': '',  # Will be populated later
        'code_list': ['Code1', 'Code2']  # Replace with actual code list
    }

    # Run the main graph
    result = main_graph.run(input_state)

    # Save the output to a markdown file
    output_filepath = os.path.join('output_directory', 'final_output.md')  # Replace 'output_directory' with the desired path
    save_final_markdown(output_filepath, result['output'])

    # Visualize the graph
    visualize_graph(main_graph, "coding_graph")

if __name__ == "__main__":
    main()
