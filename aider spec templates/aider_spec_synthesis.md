# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Add a synthesis layer to the coding agent.

## Mid-Level Objective

1) Reorder and Update Existing Nodes
- Graph Reordering: In the main graph, invert the order of the last two nodes so that the qa_quote_reasoning_pairs node precedes the output_to_markdown node. Update the edge definitions accordingly.
- QA Results Update: Modify the qa_quote_reasoning_pairs function so that its output overwrites the existing prompt_per_code_results state key with the QA-evaluated results.

2) Enhance Markdown Generation and Saving
- Generate Markdown per Charity: Update the generate_markdown function to process the prompt_per_code_results data by grouping quote–reasoning pairs by charity (using charity_id) and further organizing them by document importance and code.
- Save Files per Charity: Modify the save_final_markdown function so that for each charity, the generated markdown string is saved as a separate file (e.g., Coding_output_for_{charity_id}.md) in the designated output folder (e.g., coding_output).

3) Implement a Multi-Layer Synthesis Process
To provide a comprehensive synthesis that addresses both per-code and per-charity perspectives—and ultimately answers the research question—introduce the following synthesis layers:

- Synthesis Layer 1 – Per Charity Per Code Synthesis:
Create a new node (synthesis_layer_1) that groups all quote–reasoning pairs for each unique combination of charity and code.
Use the layer_1_synthesis_prompt to generate a synthesis for each group.
Utilize the send API to dispatch each grouped (and JSON-formatted) payload to the synthesis_layer_1 node.

- Synthesis Layer 2 – Aggregation:
Implement two parallel aggregation nodes:
Per Charity Aggregation:
Create a node (synthesis_layer_2_per_charity) that aggregates all synthesis results from Layer 1 for each charity (i.e., combining results across all codes for a given charity).
This node uses the layer_2_charity_synthesis_prompt and sends the aggregated results via the send API.
Per Code Aggregation:
Create a node (synthesis_layer_2_per_code) that aggregates all synthesis results from Layer 1 for each code (i.e., combining results across all charities for a given code).
This node uses the layer_2_code_synthesis_prompt and also employs the send API.
Final Synthesis – Comprehensive Report Generation:

- Create a final synthesis node (final_report) that takes as input both the per-charity and per-code aggregated results.
- Use the final_layer_research_question_prompt to generate a comprehensive answer to the research question.
- This node should produce a final markdown report (via an LLM call) that is then saved to the output folder.

4) Update State and Utility Integrations
- State Updates:
Modify CodingAgentState to add new attributes for synthesis data, including (but not limited to) synthesis_layer_1, synthesis_layer_2_per_code, synthesis_layer_2_per_charity, synthesis_output_per_charity, and synthesis_output_per_code.
- Define corresponding TypedDict types (e.g., SynthesisLayer1State, SynthesisLayer2PerCodeState, etc.) to enforce proper data structures.
- Utility Imports:
Ensure that all necessary helper functions (such as merge_dicts) are imported and used consistently to merge state data as required.


## Implementation Notes

- All the functions that are added to the file must be added before the if main == "__main__": block.
- When adding nodes and edges to the graph make sure they are in the appropriate section (there is one section for the nodes and one for the edges). Also make sure to place them in order.
- Here are mandatory urls you need to consult before starting to code this project:
    - https://langchain-ai.github.io/langgraph/how-tos/
    - https://langchain-ai.github.io/langgraph/concepts/#langgraph-platform
    - https://langchain-ai.github.io/langgraph/how-tos/map-reduce/
    - https://langchain-ai.github.io/langgraph/how-tos/branching/
    - https://langchain-ai.github.io/langgraph/how-tos/state-reducers/
    - https://langchain-ai.github.io/langgraph/how-tos/state-model/
    - https://langchain-ai.github.io/langgraph/how-tos/input_output_schema/
    - https://langchain-ai.github.io/langgraph/how-tos/subgraph/
- Always make the necessary imports, add them to the requirements.txt file and keep all the imports at the top of the file.
- Every function should be properly commented, see proper commenting example below.
- Keep all the LLM initializations at the top of the file.
- See below for an example of how to use the send API. In that example, the send API is used to send each subject contained in the state["subjects"] list to the generate_joke node.
- all the environment variables have been loaded in the .env file at this path: /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/.env
- in langgraph the state is passed as an input to the function, the function will modify the state and return it. Make sure to follow this design pattern when updating the functions.
- When creating a function for the graph, follow the convention shown in the example (node function example below).
- Make sure you implement the changes to all the files as stated in the low-level tasks.
- The directory where the files coding_prompt.py, coding_exec.py, coding_utils.py, coding_state.py are located is /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/src/coding
- Always make sure you have all the necessary imports. Put all the imports at the top of the file.
- Carefully review each low-level task for exact code changes
- Pay special attention to the return type of the functions. Make sure to return the correct type as specified in the function signature.

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

<proper commenting example>
def test_function(p1, p2, p3):
    """
    test_function does blah blah blah.

    :param p1: describe about parameter p1
    :param p2: describe about parameter p2
    :param p3: describe about parameter p3
    :return: describe what it returns
    """ 
    pass
</proper commenting example>

### Beginning context
- requirements.txt
- .env (readonly)
- coding_prompt.py (readonly)
- coding_exec.py
- coding_utils.py
- coding_state.py

### Ending context  
- requirements.txt
- .env (readonly)
- coding_prompt.py (readonly)
- coding_exec.py
- coding_utils.py
- coding_state.py
- coding_reducer.py

## Low-Level Tasks
> Ordered from start to finish

1. In coding_exec.py, modify the main graph to switch the order of the output_to_markdown and qa_quote_reasoning_pairs nodes.
```aider
Modify the main graph to:
# Define the main graph
main_graph = StateGraph(CodingAgentState, input = CodingAgentInputState, output=CodingAgentOutputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_subgraph_node', invoke_subgraph.compile())
main_graph.add_node('output_to_markdown_node', output_to_markdown)
main_graph.add_node('qa_quote_reasoning_pairs_node', qa_quote_reasoning_pairs)
main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges(
    'fill_info_prompt_node',
    continue_to_invoke_subgraph_research_question,
    ['invoke_subgraph_node']
)
main_graph.add_edge('invoke_subgraph_node', 'qa_quote_reasoning_pairs_node')
main_graph.add_edge('qa_quote_reasoning_pairs_node', 'output_to_markdown_node')
main_graph.add_edge('output_to_markdown_node', END)

checkpointer = MemorySaver()
main_graph = main_graph.compile(checkpointer=checkpointer)

```
2. in coding_exec.py, modify the qa_quote_reasoning_pairs function to overwrite the prompt_per_code_results with the qa_results.
```aider
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
```


3. in coding_utils.py, modify the generate_markdown function.
```aider
The function will take a state['prompt_per_code_results'] which is a nested dictionary with an int as the key and a dictionary as the value with the following structure:
prompt_per_code_results: {int {
    - charity_id: str
    - code: str
    - doc_name: str
    - quote: str
    - reasoning: str
    - document_importance: Literal["important to read", "worth reading", "not worth reading"]
}}

Modify the function generate_markdown to generate a markdown string for each charity id, and store these strings in a dictionary named markdown_output with the charity_id as the key and the markdown string as the value.

Markdown Generation Clarification:

For each charity (identified by charity_id), generate a separate markdown string (and file) that is organized as follows:
- Charity Header: The top of the markdown should display the charity's ID.
- Document Importance Section: Under a "Document Importance" header, list the names of all documents (using their doc_name) grouped into three sub-sections: Important to read, Worth reading, Not worth reading

- Code-Specific Sections: For each code associated with that charity, create a separate section that includes:
A header with the code. For each document under that code, a sub-header with the document name, followed by a list of all quote–reasoning pairs extracted from that document.

The markdown string will be generated using the markdown string format (between parenthesis are the values of the dictionary to be used in the markdown string):

<markdown string format>
# Charity Id: <charity_id>

# Document Importance
### Important to read
(list of all doc_name with document_importance = "important to read")
### Worth reading
(list of all doc_name with document_importance = "worth reading")
### Not worth reading
(list of all doc_name with document_importance = "not worth reading")

## Code: <code>
### Doc Name: <doc_name>
- **Quote:** <quote>
- **Reasoning:** <reasoning>
(repeat for each quote–reasoning pair)
(repeat the "Doc Name" section for each document under the code)
(repeat the "Code" section for each code)
</markdown string format>
```

4. in coding_utils.py, modify the save_final_markdown. so that it takes the markdown_output dictionnary as input and saves each value in a separate file 
```aider

Task Description:
Modify the save_final_markdown function so that it:
Accepts a dictionary (markdown_output) where each key is a charity_id and each value is the corresponding markdown string.
Explicitly defines the output folder as "coding_output".
Checks if the coding_output folder exists; if not, it creates the folder.
Iterates over the markdown_output dictionary, and for each charity:
Constructs a filename in the format Coding_output_for_<charity_id>.md.
Saves the markdown content to that file within the coding_output folder using os.path.join().

def save_final_markdown(markdown_output: dict):
    """
    This function takes a dictionary where each key is a charity_id and each value is the corresponding markdown string.
    It saves each markdown string into a separate file named 'Coding_output_for_<charity_id>.md' in the 'coding_output' folder.
    
    :param markdown_output: Dictionary with charity_id as keys and markdown content as values.
    """
    import os

    # Define the output folder
    output_folder = "coding_output"
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over the dictionary and save each markdown string to a file in the output folder
    for charity_id, markdown_content in markdown_output.items():
        filename = f'Coding_output_for_{charity_id}.md'
        filepath = os.path.join(output_folder, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

```


5. in coding_exec.py, modify the output_to_markdown function to use the generate_markdown function to generate the markdown_output dictionary, and the save_final_markdown function to save the markdown_output dictionary to a separate file for each charity id.
```aider

Task Description:
Modify the output_to_markdown function so that it:
Uses the generate_markdown function to create the markdown_output dictionary from the state.
Directly calls the updated save_final_markdown function with the markdown_output dictionary, ensuring that each markdown file is saved in the coding_output folder.
Returns the updated state including the markdown_output dictionary.


def output_to_markdown(state: CodingAgentState):
    """
    This function generates the markdown output from the collected results and saves separate files for each charity id
    in the 'coding_output' folder.
    """
    # Generate the markdown output dictionary by grouping results per charity
    markdown_output = generate_markdown(state['prompt_per_code_results'], state['unprocessed_documents'])
    
    # Save the markdown files in the 'coding_output' folder
    save_final_markdown(markdown_output)
    
    # Return the updated state with the markdown output
    return {"markdown_output": markdown_output}

```

6. import the merge_dicts function from coding_reducer.py
```aider
in coding_state.py, import the merge_dicts function from coding_reducer.py 

```

7. Create a new file called coding_reducer.py and add the following function:
```aider
def merge_dicts(dict_a: dict, dict_b: dict) -> dict:
    """
    Merge dict_b into dict_a. 
    Returns a new dict, leaving the original dicts unchanged.
    """
    merged = dict_a.copy()
    merged.update(dict_b)
    return merged
```

8. add a synthesis function to the coding agent (per code per charity synthesis)
```
in coding_exec.py, add a new function continue_to_synthesis_layer_1(state: CodingAgentState):

Mirror the send API example above to iterate over the state['prompt_per_code_results'] and send all the quote reasoning pairs for each code for each charity to the synthesis_layer_1 node.
Note: I want to group all entries with the same charity_id and code into one dictionary, then convert that group to JSON formatted string and send it to the synthesis_layer_1 node. in other words, the synthesis_layer_1 node will receive a subset of dictionnary stored in state['prompt_per_code_results'] that will be formatted as a JSON formated string, each subset will contain the quote reasoning pairs for a specific code for a specific charity.

This is the format of the dictionnary stored in state['prompt_per_code_results']:
prompt_per_code_results:{
    - charity_id: str
    - code: str
    - doc_name: str
    - quote: str
    - reasoning: str
    - document_importance: Literal["important to read", "worth reading", "not worth reading"]
}



return [Send("synthesis_layer_1", {"synthesis_layer_1_text": s,
                                    "synthesis_layer_1_charity_id": s['charity_id'],
                                    "synthesis_layer_1_code": s['code']
}) to get s iterate over each code and charity in the state['prompt_per_code_results'] , s['charity_id'], s['code']]

note: s is a subset of the dictionnary stored in state['prompt_per_code_results'] for a specific code for a specific charity turned into a JSON formated string.

```


9. Create a synthesis_layer_1 state
```aider
in coding_state.py, add a new class called SynthesisLayer1State.
class SynthesisLayer1State(TypedDict):
    synthesis_layer_1_text: str
    synthesis_layer_1_charity_id: str
    synthesis_layer_1_code: str

```

10. Modify CodingAgentState to add a new attribute called synthesis_layer_1.
```aider
in coding_state.py Modify CodingAgentStateCodingAgentState(TypedDict):
    markdown_output: dict[str, str]
    prompt_per_code_results: Annotated[list, merge_lists]
    unprocessed_documents: Annotated[list, merge_lists] 
    synthesis_layer_1: Annotated[Dict[str, str], merge_dicts]
```


11. in coding_exec.py, add a new function synthesis_layer_1(state: SynthesisLayer1State, config):
```aider

in coding_exec.py, add a new function synthesis_layer_1(state: CodingAgentState, config):
system_message = SystemMessage(layer_1_synthesis_prompt.format(research_question=config["configurable"].get("research_question")))

human_message = HumanMessage(content=text_to_synthesis_prompt.format(text=state['synthesis_layer_1_text']))

result = llm_o3.invoke([system_message, human_message])

return {synthesis_layer_1:{"synthesis_layer_1_result": result,
        "synthesis_layer_1_charity_id": state['synthesis_layer_1_charity_id'],
        "synthesis_layer_1_code": state['synthesis_layer_1_code']}}

```

12. add a conditional edge to the main graph to continue_to_synthesis_layer_1 node.
```aider
main_graph = StateGraph(CodingAgentState, input = CodingAgentInputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_subgraph_node', invoke_subgraph.compile())
main_graph.add_node('output_to_markdown_node', output_to_markdown)
main_graph.add_node('qa_quote_reasoning_pairs_node', qa_quote_reasoning_pairs)
main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges(
    'fill_info_prompt_node',
    continue_to_invoke_subgraph_research_question,
    ['invoke_subgraph_node']
)
main_graph.add_edge('invoke_subgraph_node', 'output_to_markdown_node')
main_graph.add_edge('output_to_markdown_node', 'qa_quote_reasoning_pairs_node')
main_graph.add_edge('qa_quote_reasoning_pairs_node', continue_to_synthesis_layer_1, [synthesis_layer_1_node])
main_graph.add_edge('synthesis_layer_1_node', END)
```

13. add a the node and edge to the main graph for the synthesis_layer_1_node.
```aider
main_graph = StateGraph(CodingAgentState, input = CodingAgentInputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_subgraph_node', invoke_subgraph.compile())
main_graph.add_node('output_to_markdown_node', output_to_markdown)
main_graph.add_node('qa_quote_reasoning_pairs_node', qa_quote_reasoning_pairs)
main_graph.add_node('synthesis_layer_1_node', synthesis_layer_1)

main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges(
    'fill_info_prompt_node',
    continue_to_invoke_subgraph_research_question,
    ['invoke_subgraph_node']
)
main_graph.add_edge('invoke_subgraph_node', 'output_to_markdown_node')
main_graph.add_edge('output_to_markdown_node', 'qa_quote_reasoning_pairs_node')
main_graph.add_edge('qa_quote_reasoning_pairs_node', continue_to_synthesis_layer_1_node, [synthesis_layer_1_node])
main_graph.add_edge('synthesis_layer_1_node', END)
```

14. add a synthesis function that will aggregate the results from the synthesis_layer_1 node for a code of all charities. 
```aider
in coding_exec.py, add a new function continue_to_synthesis_layer_2_per_code(state: CodingAgentState):

Mirror the send API example above to iterate over the state['synthesis_layer_1'] for all charities and send all the results for a specific code to the synthesis_layer_2_per_charity node. The objective is to aggregate the results for a specific code for all charities.

state['synthesis_layer_1'] is a dictionnary with the following keys:
synthesis_layer_1:{
    - synthesis_layer_1_result: str
    - synthesis_layer_1_charity_id: str
    - synthesis_layer_1_code: str
}

return [Send("synthesis_layer_2_per_charity", { "synthesis_layer_2_all_charity_text": s,
                                                "synthesis_layer_2_code": s['synthesis_layer_1_code']
}) for iterate over each charity for a specific code (repeat for all codes) in the state['synthesis_layer_1']]

note: s is a subset of the dictionnary stored in state['synthesis_layer_1'] for a specific code of all charities turned into a JSON formated string. Each relevant dictionnary values will have to be aggregated for each code of all charities to get s. 
```

15. Create a synthesis_layer_2_per_code state
```aider
in coding_state.py, add a new class called SynthesisLayer2PerCodeState.
class SynthesisLayer2PerCodeState(TypedDict):
    synthesis_layer_2_all_charity_text: str
    synthesis_layer_2_code: str
```

16. 
```aider
in coding_exec.py, add a new function synthesis_layer_2_per_code(state: SynthesisLayer2PerCodeState, config):

system_message = SystemMessage(layer_2_per_code_synthesis_prompt.format(research_question=config["configurable"].get("research_question")))

human_message = HumanMessage(content=text_to_synthesis_layer_2_prompt.format(text=state['synthesis_layer_2_all_charity_text']))

result = llm_o3.invoke([system_message, human_message])

return {synthesis_layer_2_per_code:{"synthesis_layer_2_per_code_result": result,
        "synthesis_layer_2_per_code_charity_id": state['synthesis_layer_2_code']}}

```

17. Modify CodingAgentState to add a new attribute called synthesis_layer_2_per_code and synthesis_layer_2_per_charity.
```aider
in coding_state.py Modify CodingAgentStateCodingAgentState(TypedDict):
    markdown_output: dict[str, str]
    prompt_per_code_results: Annotated[list, merge_lists]
    unprocessed_documents: Annotated[list, merge_lists] 
    synthesis_layer_1: Annotated[Dict[str, str], merge_dicts]
    synthesis_layer_2_per_code: Annotated[Dict[str, str], merge_dicts]
    synthesis_layer_2_per_charity: Annotated[Dict[str, str], merge_dicts]
```


18. add a synthesis function that will aggregate the results from the synthesis_layer_1 node for a charity of all codes. 
```aider
in coding_exec.py, add a new function continue_to_synthesis_layer_2_per_charity(state: CodingAgentState):

Mirror the send API example above to iterate over the state['synthesis_layer_1'] for all codes and send all the results for a specific charity to the synthesis_layer_2_per_code node. The objective is to aggregate the results for a specific charity of all codes.

state['synthesis_layer_1'] is a dictionnary with the following keys:
synthesis_layer_1:{
    - synthesis_layer_1_result: str
    - synthesis_layer_1_charity_id: str
    - synthesis_layer_1_code: str
}

return [Send("synthesis_layer_2_per_code", {    "synthesis_layer_2_all_code_text": s,
                                                "synthesis_layer_2_charity_id": s['synthesis_layer_1_charity_id']
}) for iterate over each code for a specific charity (repeat for all charities) in the state['synthesis_layer_1']]

note: s is a subset of the dictionnary stored in state['synthesis_layer_1'] for a specific charity of all codes turned into a JSON formated string. Each relevant dictionnary values will have to be aggregated for each charity of all codes to get s. 
```

19. Create a synthesis_layer_2_per_charity state
```aider
in coding_state.py, add a new class called SynthesisLayer2PerCharityState.
class SynthesisLayer2PerCharityState(TypedDict):
    synthesis_layer_2_all_code_text: str
    synthesis_layer_2_charity_id: str
```

20. 
```aider
in coding_exec.py, add a new function synthesis_layer_2_per_charity(state: SynthesisLayer2PerCharityState, config):

system_message = SystemMessage(layer_2_per_charity_synthesis_prompt.format(research_question=config["configurable"].get("research_question")))

human_message = HumanMessage(content=text_to_synthesis_layer_2_prompt.format(text=state['synthesis_layer_2_all_code_text']))

result = llm_o3.invoke([system_message, human_message])

return {synthesis_layer_2_per_charity:{"synthesis_layer_2_per_charity_result": result,
        "synthesis_layer_2_per_charity_code": state['synthesis_layer_2_charity_id']}}

```

21. Add the synthesis output to markdown function to the main graph. This function will take the state[synthesis_layer_2_per_code] and state[synthesis_layer_2_per_charity] from the codingagentstate and structure the texts as markdown and save them to a file (.md extension) in the coding_output folder.
```aider
in coding_utils.py, add a new function synthesis_output_to_markdown(state: CodingAgentState):

This function will take the state['synthesis_layer_2_per_charity'] and state['synthesis_layer_2_per_code']and structure the output as markdown and save them to a separate file for each charity and code.


    synthesis_layer_2_per_code: Annotated[Dict[str, str], merge_dicts]
    synthesis_layer_2_per_charity: Annotated[Dict[str, str], merge_dicts]
```

22. Create a new function called generate_synthesis_markdown to structure the synthesis output as markdown and save it to a file.
```aider

in coding_utils.py, add a new function generate_synthesis_markdown(markdown_text, name, output_folder):

This function will take a markdown_text, it will save the output as a markdown file in the output_folder folder with the name name.md.

return the markdown string.

```

23. modify the codingagentstate to add a new attribute called synthesis_output_per_charity and synthesis_output_per_code.
```aider
in coding_state.py Modify CodingAgentStateCodingAgentState(TypedDict):
    markdown_output: dict[str, str]
    prompt_per_code_results: Annotated[list, merge_lists]
    unprocessed_documents: Annotated[list, merge_lists] 
    synthesis_layer_1: Annotated[Dict[str, str], merge_dicts]
    synthesis_layer_2_per_code: Annotated[Dict[str, str], merge_dicts]
    synthesis_layer_2_per_charity: Annotated[Dict[str, str], merge_dicts]
    synthesis_output_per_charity: str
    synthesis_output_per_code: str
```

24. Create a new function called synthesis_output_to_markdown(state: CodingAgentState):
```aider

Note: make sure to import the generate_synthesis_markdown function from coding_utils.py.
in coding_exec.py, add a new function generate_synthesis_markdown(state: CodingAgentState):

synthesis_per_charity = Aggregate all the values from state['synthesis_layer_2_per_charity'] using the keys as section titles in a markdown formatted file. 

synthesis_output_per_charity = generate_synthesis_markdown(synthesis_per_charity, 'synthesis_output_per_charity.md', 'coding_output')

synthesis_per_code = Aggregate all the values from state['synthesis_layer_2_per_code'] using the keys as section titles in a markdown formatted file. 

synthesis_output_per_code = generate_synthesis_markdown(synthesis_per_code, 'synthesis_output_per_code.md', 'coding_output')

return {"synthesis_output_per_charity": synthesis_output_per_charity,
        "synthesis_output_per_code": synthesis_output_per_code}
```

25. add nodes and edges to the main graph for the synthesis_layer_2_per_code, synthesis_layer_2_per_charity, and the synthesis_output_to_markdown node.
```aider
main_graph = StateGraph(CodingAgentState, input = CodingAgentInputState)
main_graph.add_node('fill_info_prompt_node', fill_info_prompt)
main_graph.add_node('invoke_subgraph_node', invoke_subgraph.compile())
main_graph.add_node('output_to_markdown_node', output_to_markdown)
main_graph.add_node('qa_quote_reasoning_pairs_node', qa_quote_reasoning_pairs)
main_graph.add_node('synthesis_layer_1_node', synthesis_layer_1)
main_graph.add_node('synthesis_layer_2_per_code_node', synthesis_layer_2_per_code)
main_graph.add_node('synthesis_layer_2_per_charity_node', synthesis_layer_2_per_charity)
main_graph.add_node('synthesis_output_to_markdown_node', synthesis_output_to_markdown)

main_graph.add_edge(START, 'fill_info_prompt_node')
main_graph.add_conditional_edges(
    'fill_info_prompt_node',
    continue_to_invoke_subgraph_research_question,
    ['invoke_subgraph_node']
)
main_graph.add_edge('invoke_subgraph_node', 'output_to_markdown_node')
main_graph.add_edge('output_to_markdown_node', 'qa_quote_reasoning_pairs_node')
main_graph.add_edge('qa_quote_reasoning_pairs_node', continue_to_synthesis_layer_1_node, [synthesis_layer_1_node])
main_graph.add_edge('synthesis_layer_1_node', 'synthesis_layer_2_per_code_node')
main_graph.add_edge('synthesis_layer_2_per_code_node', 'synthesis_layer_2_per_charity_node')
main_graph.add_edge('synthesis_layer_2_per_charity_node', 'synthesis_output_to_markdown_node')
main_graph.add_edge('synthesis_output_to_markdown_node', END)
```

26. Add the final report synthesis function to the main graph.
```aider

in coding_exec.py, add a new function final_report(state: CodingAgentState, config):

system_message = SystemMessage(final_layer_research_question_prompt.format(research_question=config["configurable"].get("research_question")))

human_message = HumanMessage(content=text_to_synthesis_layer_2_prompt.format(per_charity_aggregated_outputs=state['synthesis_output_per_charity'], 
per_code_aggregated_outputs=state['synthesis_output_per_code']))

result = llm_o3.invoke([system_message, human_message])

final_report_result = generate_synthesis_markdown(result, 'final_report.md', 'coding_output')

return {"final_report_result": final_report_result}

```
