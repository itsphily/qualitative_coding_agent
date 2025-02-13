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
- [List of files that exist at start - what files exist at start?]

### Ending context  
- [List of files that will exist at end - what files will exist at end?]

## Low-Level Tasks
> Ordered from start to finish

1. [First task - what is the first task?]
```aider
What prompt would you run to complete this task?
What file do you want to CREATE or UPDATE?
What function do you want to CREATE or UPDATE?
What are details you want to add to drive the code changes?
```
2. [Second task - what is the second task?]
```aider
What prompt would you run to complete this task?
What file do you want to CREATE or UPDATE?
What function do you want to CREATE or UPDATE?
What are details you want to add to drive the code changes?
```
3. [Third task - what is the third task?]
```aider
What prompt would you run to complete this task?
What file do you want to CREATE or UPDATE?
What function do you want to CREATE or UPDATE?
What are details you want to add to drive the code changes?
```