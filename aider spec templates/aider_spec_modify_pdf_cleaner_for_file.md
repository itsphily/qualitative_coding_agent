# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.
## High-Level Objective

- Modify chunk_to_md.py to clean all the files in a directory rather than just one file

## Mid-Level Objective

- Modify the how the main function handles the arguments being passed to it. Right now we pass --filepath and --qa_loop_limit. in the current script filepath points to a file that contains the text to be cleaned, however we want to be able to pass a directory and have it clean all the files in the directory.
- Modify the states to be able to handle a directory being passed as filepath. 
- Modify the graph nodes, edges and functions to be able to handle a directory being passed as filepath rather than a single file.

## Implementation Notes
- in langgraph the state is passed as an input to the function, the function will modify the state and return it. Make sure to follow this design pattern when updating the functions.
- See below for an example of how to use the send API. In that example, the send API is used to send each subject contained in the state["subjects"] list to the generate_joke node.
- Carefully review each low-level task for exact code changes
- When creating or modifying a function for the graph, follow the convention shown in the example (node function example below).
- always update the requirements.txt file when you update the dependencies
- Here are mandatory urls you need to consult before starting to code this project:
    - https://langchain-ai.github.io/langgraph/how-tos/
    - https://langchain-ai.github.io/langgraph/concepts/#langgraph-platform
    - https://langchain-ai.github.io/langgraph/how-tos/map-reduce/
    - https://langchain-ai.github.io/langgraph/how-tos/branching/

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

## Context

### Beginning context
- /src/pdf_extraction/chunk_to_md.py
- /src/utils.py
- /src/prompt.py (readonly)
- requirements.txt

### Ending context  
- /src/pdf_extraction/chunk_to_md.py
- /src/utils.py
- /src/prompt.py (readonly)
- requirements.txt

## Low-Level Tasks
> Ordered from start to finish


1. Modify the class PDFToMarkdownInputState
```aider
in chunk_state.py, class PDFToMarkdownState(TypedDict):
    filepath: str 
    cleaned_text: Annotated[Dict[int, str], merge_dicts]
    chunks_dict: Dict
    cleaned_chunk_dict: Annotated[Dict[int, str], merge_dicts]
    qa_loop_limit: int
"""


2. Modify the main function to be able to handle a directory being passed as filepath.
```aider
in chunk_to_md.py, modify the def main():
Remove
""" 
    logger.info(f"Starting processing of file: {filepath}")
    logger.info(f"QA loop limit set to: {qa_loop_limit}")

    with open(filepath, "r", encoding="utf-8") as f:
        extracted_text = f.read()

    pdf_state = PDFToMarkdownInputState(
        extracted_text=extracted_text,
        filepath=filepath,
        qa_loop_limit=qa_loop_limit
    )
"""


```



1. Create a new function that will take the directory as the --filepath argument passed in the CLI and use the send api to send each file in the directory to the chunk_file_node
```aider
in chunk_to_md.py, create function retrieve_files_in_directory(PDFToMarkdownState):

    - use the send api to send each file in the directory to the chunk_file_node
    
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