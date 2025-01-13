# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- The goal of the script is to take a generic prompt, populate it with the relevant information, invoke the LLM with the specific prompt (one prompt for each code) for each document in a specific folder, and save the output to a markdown file.

## Mid-Level Objective

- [List of mid-level objectives - what are the steps to achieve the high-level objective?]
- [Each objective should be concrete and measurable]
- [But not too detailed - save details for implementation notes]

## Implementation Notes
- See below for an example of how to use the send API. In that example, the send API is used to send each subject contained in the state["subjects"] list to the generate_joke node.
- to implement a subgraph, use the following convention:  <name of the current graph>.add_edge(<name of the node>, <name of the subgraph>.compile()). Also see subgraph example below.
- Always make the necessary imports, add them to the requirements.txt file and keep all the imports at the top of the file.
- Keep all the LLM initializations at the top of the file.
- Every function should be properly commented
- all the environment variables have been loaded in the .env file at this path: /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/.env
- The directory where the files coding_prompt.py, coding_exec.py, coding_utils.py, coding_state.py are located is /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/src/coding
- When the function uses an input schema such as AgentPerCodeInputState, or CodingAgentInputState always map the input schema to the overall state (in this case respectively AgentPerCodeState, or CodingAgentState). Use the convention shown in the multiple input and output schema example below.
- When creating a function for the graph, follow the convention shown in the example (node function example below).

<send API example>
def continue_to_jokes(state: OverallState):
    """
    We have this list in state. 
    We iterate through that list and for every subject in that list, we can use send to send it to a particular node.
    this will spawn a new generate_joke node for each subject, based on the size of the subjects list.
 
    The subject key is in the generate_joke state. 
    But the generate_joke state can contain whatever you want (it can have any state you want)
    """
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]
</send API example>

<subgraph example>
fa_builder = StateGraph(input=FailureAnalysisState,output=FailureAnalysisOutputState)
fa_builder.add_node("get_failures", get_failures)
fa_builder.add_node("generate_summary", generate_summary)
fa_builder.add_edge(START, "get_failures")
fa_builder.add_edge("get_failures", "generate_summary")
fa_builder.add_edge("generate_summary", END)

qs_builder = StateGraph(input=QuestionSummarizationState,output=QuestionSummarizationOutputState)
qs_builder.add_node("generate_summary", generate_summary)
qs_builder.add_node("send_to_slack", send_to_slack)
qs_builder.add_edge(START, "generate_summary")
qs_builder.add_edge("generate_summary", "send_to_slack")
qs_builder.add_edge("send_to_slack", END)

entry_builder = StateGraph(EntryGraphState)
entry_builder.add_node("clean_logs", clean_logs)
entry_builder.add_node("question_summarization", qs_builder.compile())
entry_builder.add_node("failure_analysis", fa_builder.compile())
graph = qs_builder.compile()
</subgraph example>

<multiple input and output schema >
class InputState(TypedDict):
    user_input: str

class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str

def node_1(state: InputState) -> OverallState:
    # Write to OverallState
    return {"foo": state["user_input"] + " name"}
</multiple input and output schema >

<node function example>
In this example, the node function is generate_joke. It takes the JokeState and returns an attribute(jokes) of the JokeState.
def generate_joke(state: JokeState):
    """
    Joke prompt that we format with the subject
    """
    prompt = joke_prompt.format(subject=state["subject"])
    response = model.with_structured_output(Joke).invoke(prompt)
    """
    return jokes, we are writing this to the jokes state in the overall state.
    We are passing it as a list so that it is appended to the jokes list.
    """
    return {"jokes": [response.joke]}
</node function example>

## Context

### Beginning context
- [List of files that exist at start - what files exist at start?]

### Ending context  
- [List of files that will exist at end - what files will exist at end?]

## Low-Level Tasks
> Ordered from start to finish

1. Create the files
```aider
CREATE coding_exec.py in src/coding directory
```
2. Create the files
```aider
Create coding_state.py in src/coding directory
```
3. Create the files
```aider
Create coding_utils.py in src/coding directory
```
4. Create the classes 
```aider
from typing import List
in coding_state.py CREATE class CodingAgentState(TypedDict):
charity_id: str
charity_overview:str
charity_directory: str
research_question:str
project_description:str
prompt_for_project: str
code_list: List
output_per_code: Annotated[list, operator.add]
```
5. Create the classes
```aider
from typing import List
in coding_state.py CREATE class CodingAgentOutputState(TypedDict):
output_per_code: Annotated[list, operator.add]
```
6. Create the classes
```aider
from typing import List
in coding_state.py CREATE class CodingAgentInputState(TypedDict):
charity_id: str
charity_overview: str
charity_directory: str
research_question: str
project_description: str
prompt_for_project: str
code_list: List
```
7. Create the classes
```aider
import operator
from typing import Annotated
in coding_state.py CREATE class AgentPerCodeState(TypedDict):
prompt_per_code: str
charity_directory:str
doc_text_list = List[str]
output_per_code: Annotated[list, operator.add]
output_per_code_per_doc: Annotated[list, operator.add]
```
8. Create the classes
```aider
in coding_state.py CREATE class AgentPerCodeInputState(TypedDict):
prompt_per_code: str
charity_directory:str
```
9. CREATE the main function
```aider
in coding_exec.py,  CREATE  a main function: 
def main(): 


if __name__ == "__main__"
main()

in coding_exec.py,  main harcode the CodingAgentInputState with:

charity_id = 'GiveDirectly'
charity_overview = Its social goal is 'Extreme poverty'. Its intervention is 'Distribution of wealth transfers'.
directory = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/storage/nougat_extracted_text/01_GiveDirectly"
research_question: "What operational processes enable charities to be cost effective?"

project_description: "In this research project, each case focuses on a charity known for its cost-effectiveness, i.e., its ability to pursue its social mission at a low cost.

Each case contains numerous data sources, including interview notes, third party assessments, webpages from a charity website and other data sources.

Each charity is seeking to address a social cause and it does so by implementing its intervention(s)."
```

10. CREATE the function to fill the prompt with the charity and the research specific information
```aider
from coding_prompt.py import coding_agent_prompt
from from langgraph.constants import Send

in coding_exec CREATE def fill_info_prompt(state: CodingAgentInputState) -> CodingAgentState:
Add and Complete the description of the function: "This function takes (...) and fills the prompt with the charity and the research specific information"

Use the information in CodingAgentState to Format the following field in the prompt:
- project_description with state.project_description 
- charity_overview with state.charity_ID + ": " + state.charity_overview
- research_question with state.research_question
Save the completed prompt to prompt_with_charity_research_information

return {"prompt_for_project" : prompt_with_charity_research_information}
```
11. CREATE the function to send the generically filled prompt to the subgraph to be filled with the code and the doc text
```aider
in coding_exec CREATE def continue_to_invoke_prompt(state: CodingAgentState):
Add and Complete the description of the function: "This function sends the generically filled prompt to the subgraph to invoke the prompt per code per doc"

prompt_with_charity_research_information = state['prompt_for_project']

return [Send ("invoke_code_prompt_node", { 
"prompt_per_code" : prompt_with_charity_research_information.format(code with c),
"charity_directory" : state[''charity_directory"]
} for c in state[''code_list"]
```

12. CREATE the function to get the text from the markdown file
```aider

in coding_utils CREATE def path_to_text(path):

Add and Complete the description of the function: "This function takes in a path and returns the content of the .md file"

CREATE a function that takes the path to a file and returns the full text from a .md document

return doc_text
```

13. CREATE the function to get the text from the markdown file
```aider

in coding_exec CREATE def get_doc_text(state: AgentPerCodeInputState) -> AgentPerCodeState:

Add and Complete the description of the function: "This function takes each texts from the files in the directory and appends them to a list "

CREATE a function to find all the paths of the files in state["charity_directory"], append the path to doc_path_list list
Use the function path_to_text(path) on each of the path in the list AND SAVE the results to a doc_text_list

return {'doc_text_list': doc_text_list}
```

14. CREATE the function to send the prompt per code per doc to the subgraph to invoke the prompt per code per doc
```aider
in coding_exec CREATE def continue_invoke_code_prompt(state: AgentPerCodeState):

Add and Complete the description of the function: "This function takes in the prompt filled with the charity and research specific information, iterates over the texts in  doc_text_list uses Send to invoke One prompt per code per file"

return [Send ("invoke_one_code_prompt_per_doc_node"), {
"prompt_per_code" = state["prompt_per_code"],
"doc_text" = d
} for d in state['doc_text_list']
]
```

15. CREATE the class
```aider
in coding_state.py CREATE class AgentRunState(TypedDict):
prompt_per_code: str
doc_text:str
```

16. CREATE the class
```aider
in coding_state.py CREATE class AgentRunOutputState(TypedDict):
output_per_code_per_doc: str
```

17. ADD the llm initialization to coding_exec.py
```aider
ADD the llm initialization to coding_exec.py

llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)

llm_json_mode = ChatOpenAI(
    model="deepseek-chat", 
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)

llm_json_mode.bind(response_format={"type": "json_object"})
```

18. CREATE the function to invoke the llm for each doc
```aider

in coding_exec CREATE def invoke_one_code_prompt_per_doc(state: AgentRunState):

Add and Complete the description of the function: "This function takes in the full prompt and invokes the llm for each doc"

system_message = [SystemMessage(content=state['prompt_per_code']), 
                  HumanMessage(content=text_to_code_prompt.format(text = state['doc_text'])]

result = llm.invoke(system_message)

return {"output_per_code_per_doc": result}

```
19. CREATE the function to visualize the graph
```aider

from langchain_core.runnables.graph import MermaidDrawMethod
in coding_utils CREATE def visualize_graph (graph, name):
def visualize_graph(graph, name):
    """Visualize the graph"""
    # visualize the graph
    try:
        png_data = graph.get_graph(xray = 1).draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        with open(f'{name}.png', 'wb') as f:
            f.write(png_data)
        print(f"Graph visualization saved to '{name}.png'")
    except Exception as e:
        print(f"Error saving graph visualization: {e}")
```

20. CREATE the subgraph to invoke the llm for each doc with the code prompt
```aider
from langgraph.graph import START, END, StateGraph

in coding_exec CREATE the graph graph_per_code_per_doc (MIRROR the subgraph example to add nodes and edges to the graph):
graph_per_code_per_doc = StateGraph(AgentRunState, output = AgentRunOutputState)
graph_per_code_per_doc.add_node('invoke_one_code_prompt_per_doc_node', invoke_one_code_prompt_per_doc)

graph_per_code_per_doc.add_edges(START, 'invoke_one_code_prompt_per_doc_node')
graph_per_code_per_doc.add_edge('invoke_one_code_prompt_per_doc_node', END)
```

21. CREATE the class
```aider
in coding_state.py CREATE class AgentPerCodeOutputState(TypedDict):
output_per_code_per_doc: str
```

22. CREATE the function to aggregate all the results per doc
```aider

in coding_exec CREATE def aggregate_all_results_per_doc(state: AgentPerCodeState) -> AgentPerCodeOutputState:

Add and Complete the description of the function: "This function takes in the list of results from invoking the LLM with one code for each doc, and aggregates all the results per code"

CREATE a function that takes the list of strings stored in state['output_per_code_per_doc'] and concatenate each item in a single string. Save the result to output_per_code

return {"output_per_code": output_per_code}

```
23. CREATE the graph to run the graph per code
```aider
MIRROR the subgraph example to add nodes and edges to the graph

in coding_exec CREATE the graph graph_per_code(MIRROR the subgraph example to add nodes and edges to the graph): 
graph_per_code = StateGraph(AgentPerCodeState, input = AgentPerCodeInputState,  output = AgentPerCodeOutputState)
graph_per_code.add_node('get_doc_text_node', get_doc_text)
graph_per_code.add_node('graph_per_code_per_doc_node', graph_per_code_per_doc.compile())
graph_per_code.add_node ('aggregate_all_results_per_doc_node', aggregate_all_results_per_doc)

graph_per_code.add_edge(START,  'get_doc_text_node' )
graph_per_code.add_conditional_edges('get_doc_text_node', continue_invoke_code_prompt, ['graph_per_code_per_doc'])
graph_per_code.add_edge('graph_per_code_per_doc', 'aggregate_all_results_per_doc_node')
graph_per_code.add_edge('aggregate_all_results_per_doc_node', END)

```

24. CREATE the function to aggregate all the results
```aider

in coding_exec CREATE def aggregate_all_results(state: CodingAgentState) -> CodingAgentOutputState:

Add and Complete the description of the function: "This function takes in the list of results for each code, and aggregates all the results for a final output"

CREATE a function that takes the list of strings stored in state['output_per_code'] and concatenate each item in a single string. Save the result to output

return {"output": output}

```
25. CREATE the graph to run the main graph
```aider
from langgraph.graph import START, END, StateGraph
MIRROR the subgraph example to add nodes and edges to the graph

in coding_exec CREATE the graph main_graph (MIRROR the subgraph example to add nodes and edges to the graph):
main_graph = StateGraph(CodingAgentState, input = CodingAgentInputState , output = CodingAgentOutputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('graph_per_code_node', graph_per_code.compile())
main_graph.add_node ('aggregate_all_results_node', aggregate_all_results)

main_graph. add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges('fill_info_prompt_node', continue_to_invoke_prompt, ['graph_per_code_node'])
main_graph.add_edge('graph_per_code_node', aggregate_all_results_node)
main_graph.add_edge(aggregate_all_results_node, END)
```

26. CREATE the function to save the final markdown file
```aider
import os
In coding_utils.py ADD def save_final_markdown(filepath: str, cleaned_text: str):

 CREATE a function that will take the cleaned_text and the filepath as arguments and will SAVE the cleaned_text to a .md file in the filepath
)
```

27. RUN the main graph, Save the output to a markdown file, and visualize the graph
```aider
in coding_exec.py,def main(): 

if __name__ == "__main__"
main()

RUN the main graph
ADD visualize_graph (main_graph, "coding_graph")
Use save_final_markdown to save the output of the main graph to a markdown file
```
