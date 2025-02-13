# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Add a synthesis layer to the coding agent.

## Mid-Level Objective

-  To add the synthesis layer, we will modify the last two nodes of the current graph (invert the order to the output_to_markdown node, and qa_quote_reasoning_pairs node)
- Modify the output of the qa_quote_reasoning_pairs node to overwrite the prompt_per_code_results. 
- Modify the output_to_markdown node functions: generate_markdown (uses the prompt_per_code_results as input) and save_final_markdown to respectively generate the markdown of each quote reasoning pair per directory (charity id) and save the markdown to a file. 
- Add a synthesis layer to the coding agent. To add the synthesis layer we willl need to create several new nodes and edges to the graph. This layer will have 4 parts:
    - Layer 1: first, create a node to do per charity per code synthesis. Create a new node that will use the layer_1_synthesis_prompt to generate a synthesis for each charity per code. This node will use the send API to send each quote reasoning pairs grouped by charity and code to the layer_1_synthesis node.
    - Layer 2 (per charity synthesis): second, create a node to do per charity synthesis. Create a new node that will use the layer_2_charity_synthesis_prompt to generate a synthesis for all codes for each charity. This node will use the output from the previous layer (per charity per code synthesis), aggregate the results per charity (aggregate the results for each code per charity) and then use the send API to send the aggregated results to the layer_2_charity_synthesis node, this will be done in parallel for each charity.
    - Layer 2 (per code synthesis): third, create a node to do per code synthesis. Create a new node that will use the layer_2_code_synthesis_prompt to generate a synthesis for all charities for each code. This node will use the output from the previous layer (per charity per code synthesis), aggregate the results per code (aggregate the results for each charity per code) and then use the send API to send the aggregated results to the layer_2_code_synthesis node, this will be done in parallel for each code.
    - Final layer: fourth, create a node to do final synthesis. Create a new node that will use the final_layer_research_question_prompt to generate a comprehensive answer to the research question based on the aggregation from the previous layer (layer 2). This node will use the output from the previous layer (per charity synthesis and per code synthesis), as well as the final_layer_research_question_prompt to invoke an LLM call to generate the final output.


## Implementation Notes

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
- The directory where the files coding_prompt.py, coding_exec_new.py, coding_utils.py, coding_state_new.py are located is /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/src/coding
- Carefully review each low-level task for exact code changes

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
The function will take a state['prompt_per_code_results'] which is a dictionary with the following keys: data type:
prompt_per_code_results:{
    - charity_id: str
    - code: str
    - doc_name: str
    - quote: str
    - reasoning: str
    - document_importance: Literal["important to read", "worth reading", "not worth reading"]
}

Modify the function generate_markdown to generate a markdown string for each charity id, and store these strings in a dictionary named markdown_output with the charity_id as the key and the markdown string as the value.

The markdown string will be generated using the markdown string format (between parenthesis are the values of the dictionary to be used in the markdown string):
<markdown string format>
# Charity Id (charity_id)

# Document Importance
### Important to read
(list of all the doc_name that have document_importance set to "important to read")
### Worth reading
(list of all the doc_name that have document_importance set to "worth reading")
### Not worth reading
(list of all the doc_name that have document_importance set to "not worth reading")

## Code (code)
### Doc Name (doc_name)
- **Quote:** Quote (quote)
- **Reasoning:** Reasoning (reasoning)
(repeat for each quote reasoning pair)
(repeat this section for each code)
</markdown string format>
```

4. in coding_utils.py, modify the save_final_markdown. so that it takes the markdown_output dictionnary as input and saves each value in a separate file 
```aider

Modify save_final_markdown(markdown_output): 
    for charity_id, markdown_content in markdown_output.items():
        filename = f'Coding_output_for_{charity_id}.md'
        save_final_markdown(filename, markdown_content)

All the files will be saved in the coding_output folder.
```


5. in coding_exec.py, modify the output_to_markdown function to use the generate_markdown function to generate the markdown_output dictionary, and the save_final_markdown function to save the markdown_output dictionary to a separate file for each charity id.
```aider
def output_to_markdown(state: CodingAgentState):
    """
    This function generates the markdown output from the collected results and saves separate files for each charity id.
    """
    markdown_output = generate_markdown(state['prompt_per_code_results'], state['unprocessed_documents'])
    
    save_final_markdown(filename, markdown_content)
    
    return {"markdown_output": markdown_output}

```

6. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```

4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
4. in coding_utils.py, modify the generate_markdown function.
```aider
```
