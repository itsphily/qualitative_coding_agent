# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Build a coding agent that combines a research question with a code into a more specific research question. Build the functions to invoke an LLM to find evidence in the documents that would answer the research question, and then outputs a structured summary (in Markdown).

## Mid-Level Objective

- Load environment variables and configure all required LLMs and tools.
- Build the functions to combine a research question with a code into a more specific research question.
- Build the functions to invoke an LLM within the subgraph with each document.  
- The invokation of the LLM should find evidence in the documents that would answer the research question. The evidence will give us a quote and a reasoning.
- The output of the subgraph shtould be a list of dictionaries wih the following keys: code, charity_id, doc_name, quote, reasoning.
- The output of the main graph should be a markdown file with the following structure:
    - # code
    - ## charity_id
    - ### doc_name
        - Quote: quote
        - Reasoning: reasoning

## Implementation Notes
- See below for an example of how to use the send API. In that example, the send API is used to send each subject contained in the state["subjects"] list to the generate_joke node.
- to implement a subgraph, use the following convention:  <name of the current graph>.add_edge(<name of the node>, <name of the subgraph>.compile()). Also see subgraph example below.
- Always make the necessary imports, add them to the requirements.txt file and keep all the imports at the top of the file.
- Keep all the LLM initializations at the top of the file.
- Every function should be properly commented
- all the environment variables have been loaded in the .env file at this path: /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/.env
- When creating a function for the graph, follow the convention shown in the example (node function example below).
- Make sure you implement the changes to all the files as stated in the low-level tasks.
- The directory where the files coding_prompt.py, coding_exec_new.py, coding_utils.py, coding_state_new.py are located is /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/src/coding
- When the function uses an input schema such as InvokePromptInputState always map the input schema to the overall state (in this case InvokePromptState). Use the convention shown in the multiple input and output schema example below.
- Here are mandatory urls you need to consult before starting to code this project:
    - https://langchain-ai.github.io/langgraph/how-tos/
    - https://langchain-ai.github.io/langgraph/concepts/#langgraph-platform
    - https://langchain-ai.github.io/langgraph/how-tos/map-reduce/
    - https://langchain-ai.github.io/langgraph/how-tos/branching/

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
- /src/coding/coding_exec.py (readonly)
- /src/coding/coding_exec_new.py
- /src/coding/coding_prompt.py (readonly)
- /src/coding/coding_state.py (readonly)
- /src/coding/coding_state_new.py
- /src/coding/coding_utils.py

### Ending context  
- /src/coding/coding_exec.py (readonly)
- /src/coding/coding_exec_new.py
- /src/coding/coding_prompt.py (readonly)
- /src/coding/coding_state.py (readonly)
- /src/coding/coding_state_new.py
- /src/coding/coding_utils.py

## Low-Level Tasks
> Ordered from start to finish

1. MIRROR the imports and the llm initialization in coding_exec.py to coding_exec_new.py
```aider
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
```

2. Create fill_info_prompt function in coding_exec_new.py
```aider
In coding_exec_new.py, Create def fill_info_prompt (state: CodingAgentState):
    """
    This function takes the generic prompt header and fills it with the charity and research specific information.
    """
    code_and_research_question_prompt = combine_code_and_research_question_prompt.format(
        research_question=state['research_question']
    )
    # Store the formatted header in the state
    return {"code_and_research_question_prompt": code_and_research_question_prompt}
```
3. Create continue_to_invoke_subgraph_research_question function in coding_exec_new.py
```aider
def continue_to_invoke_subgraph_research_question(state: CodingAgentState):
    """
    This function sends the formatted prompt to the subgraph to first combine the code and research question and then invoke that prompt per code per document.
    """
    combine_code_and_research_question = state['combine_code_and_research_question']

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
```
4. Create a new class in src/coding/coding_state_new.py
```aider
class InvokePromptInputState(TypedDict):
    combine_code_and_research_question_prompt: str
    charity_id: str
    charity_directory: str
    code: str
```
5. Create a new class in src/coding/coding_state_new.py
```aider
class InvokePromptState(TypedDict):
    combine_code_and_research_question_prompt: str
    charity_id: str
    charity_directory: str
    code: str
    research_question_with_code: str
    quote: str
    reasoning: str

```

6. Create a new class in src/coding/coding_state_new.py
```aider
class InvokePromptOutputState(TypedDict):
    code: str
    charity_id: str
    quote: str
    reasoning: str
```

7. Create a new function in src/coding/coding_exec_new.py
```aider
def combine_code_and_research_question_prompt(state: InvokePromptInputState)->InvokePromptState:
    """
    This function takes the input state and combines the code and research question prompt.
    """

    human_message = HumanMessage(content=state['combine_code_and_research_question_prompt'])

    # Make the LLM call using the model bound with the StructuredOutputPerCode tool
    result = llm.invoke([human_message])
    return {"research_question": result.content}
```

8. Create a new function to extract the document name from the path in src/coding/coding_utils.py
```aider
def path_to_doc_name(path: str)->str:
    """
    This function takes the path to a document and returns the document name.
    """
    CREATE a function that takes the path to a document and returns the document name. the document name is the last part of the path.
```

9. Create a new function in src/coding/coding_exec_new.py
```aider
def continue_invoke_research_question(state: InvokePromptState)->InvokePromptOutputState:
    """
    This function sends the formatted prompt to invoke the prompt per code per document.
    """

    prompt = coding_agent_prompt_header_specific.format(
        research_question=state['research_question']
    )
    
    doc_path_list = []

    for root, dirs, files in os.walk(state['charity_directory']):
        for file in files:
            if file.endswith('.md'):
                doc_path = os.path.join(root, file)
                doc_path_list.append(doc_path)

    return [
        Send (
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
```
10. Create a new function in src/coding/coding_exec_new.py
```aider
def invoke_prompt(state: InvokePromptPerCodeState):
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

	data = {
	"code": state['code'],            
	"charity_id": state["charity_id"],
        "doc_name": state["doc_name"],
	"quote": result.tool_calls[0]['args']['quote']
	"reasoning": result.tool_calls[0]['args']['quote']
	}

        # Return the structured JSON string so it can be aggregated
        return {"prompt_per_code_results": [data]}
    
else:
        # If no tool call was made, fallback
        print("No tool call was made")
	    print("error: no tool call was made")

```

11. Create a new function in src/coding/coding_utils.py
```aider
def merge_lists(list_a: list, list_b: list) -> list:    
"""
    Merge list_b into list_a. 
    Returns a new list, leaving the original list unchanged.
"""
merged = list_a.copy()
merged.extend(list_b)
return merged
```

12. Create a new function in src/coding/coding_utils.py
```aider
from collections import defaultdict

def generate_markdown(documents):
    """
    Generate a Markdown string grouped by:
      1) code (top-level #)
      2) charity_id (##)
      3) doc_name (###)
    For each document, include lines for "Quote" and "Reasoning".
    """
    # Group data in a nested structure: code -> charity_id -> doc_name -> list of (quote, reasoning)
    grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for doc in documents:
        code = doc["code"]
        charity_id = doc["charity_id"]
        doc_name = doc["doc_name"]
        quote = doc["quote"]
        reasoning = doc["reasoning"]
        
        # Append to our nested data structure
        grouped_data[code][charity_id][doc_name].append((quote, reasoning))

    # Build the Markdown output
    markdown_lines = []
    for code, charities in grouped_data.items():
        # Top-level heading for code
        markdown_lines.append(f"# {code}")
        
        for charity_id, doc_names in charities.items():
            # Heading for charity_id
            markdown_lines.append(f"## {charity_id}")
            
            for doc_name, entries in doc_names.items():
                # Sub-heading for doc_name
                for (quote, reasoning) in entries:
                    markdown_lines.append(f"### {doc_name}")
                    markdown_lines.append(f"Quote: {quote}")
                    markdown_lines.append(f"Reasoning: {reasoning}")
                    
                    # Optional blank line for spacing
                    markdown_lines.append("")
    
    # Join everything with newlines
    return "\n".join(markdown_lines)
```

13. Create a new function in src/coding/coding_exec.py
```aider
def output_to_markdown(state: CodingAgentState)->CodingAgentOutputState:  
"""
Write a description of the function
"""
markdowndoc = generate_markdown(state['prompt_per_code_results'])
return {"markdown_output": markdowndoc}
```

14. Create a new class in src/coding/coding_state_new.py
```aider
class CodingAgentOutputState(TypedDict):
    markdown_output: str
```

15. Create a new subgraph in src/coding/coding_exec_new.py
```aider
from langgraph.graph import START, END, StateGraph
MIRROR the subgraph example to add nodes and edges to the graph

invoke_subgraph = StateGraph(InvokePromptState, input=InvokePromptInputState)
invoke_subgraph.add_node("combine_code_and_research_question_prompt_node", combine_code_and_research_question_prompt)
invoke_subgraph.add_node('invoke_prompt_node', invoke_prompt)

invoke_subgraph.add_edge(START, "combine_code_and_research_question_prompt_node")
invoke_subgraph.add_conditional_edges("combine_code_and_research_question_prompt_node", continue_invoke_research_question, ['invoke_prompt_node']) 
invoke_subgraph.add_edge('invoke_prompt', END)
```

16. Create main graph in src/coding/coding_exec_new.py
```aider
from langgraph.graph import START, END, StateGraph
MIRROR the subgraph example to add nodes and edges to the graph

in coding_exec CREATE the graph main_graph (MIRROR the subgraph example to add nodes and edges to the graph):
main_graph = StateGraph(CodingAgentState, input = CodingAgentInputState , output = CodingAgentOutputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_subgraph_node', invoke_subgraph.compile())
main_graph.add_node('output_to_markdown_node', output_to_markdown)

main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges('fill_info_prompt_node', continue_to_invoke_subgraph_research_question, ['invoke_subgraph_node']
main_graph.add_edge('invoke_subgraph_node', 'output_to_markdown_node')
main_graph. add_edge('output_to_markdown_node', END)
```

17. RUN the main graph, print the output to a markdown file, and visualize the graph
```aider
in coding_exec.py,def main(): 

if __name__ == "__main__"
main()

RUN the main graph
ADD visualize_graph (main_graph, "coding_graph_new")
from coding_utils import save_final_markdown
Use save_final_markdown to save the output of the main graph to a markdown file
```