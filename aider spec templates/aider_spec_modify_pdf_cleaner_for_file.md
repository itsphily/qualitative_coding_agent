# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.
## High-Level Objective

- Modify chunk_to_md.py to clean all the files in a directory rather than just one file

## Mid-Level Objective

- Modify the how the main function handles the arguments being passed to it. Right now we pass --filepath and --qa_loop_limit. in the current script filepath points to a file that contains the text to be cleaned, however we want to be able to pass a directory and have it clean all the files in the directory.
- Modify the states to be able to handle a directory being passed as filepath. 
- Modify the graph nodes, edges and functions to be able to handle a directory being passed as filepath rather than a single file.

## Implementation Notes
- Always properly comment the code you write, comment the function using proper docstrings using pep8 style.
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

<example of nested dictionary>
{
    "file_name_1": {
        "chunk_number_1": "chunk_text_1",
        "chunk_number_2": "chunk_text_2",
        "chunk_number_3": "chunk_text_3"
    },
    "file_name_2": {
        "chunk_number_1": "chunk_text_1",
        "chunk_number_2": "chunk_text_2",
        "chunk_number_3": "chunk_text_3"
    }
}
</example of nested dictionary>

## Context

### Beginning context
- /src/pdf_extraction/chunk_to_md.py
- /src/pdf_extraction/chunk_state.py
- /src/pdf_extraction/chunk_utils.py
- /src/prompt.py (readonly)
- requirements.txt

### Ending context  
- /src/pdf_extraction/chunk_to_md.py
- /src/pdf_extraction/chunk_state.py
- /src/pdf_extraction/chunk_utils.py
- /src/prompt.py (readonly)
- requirements.txt

## Low-Level Tasks
> Ordered from start to finish


1. Modify the class PDFToMarkdownInputState
```aider
in chunk_state.py, class PDFToMarkdownState(TypedDict):
    filepath: str 
    cleaned_text: Annotated[Dict, merge_dicts]
    chunks_dict: Dict[str, Dict[int, str]]
    cleaned_chunk_dict: Annotated[Dict[int, str], merge_dicts]
    qa_loop_limit: int
    files_dict: Dict[str, str]
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
Add  pdf_state = PDFToMarkdownInputState(
        filepath=filepath,
        qa_loop_limit=qa_loop_limit
    )
    The rest of the main function should be the same.
```

3. Create a new function that will take filepath argument form the PDFToMarkdownInputState and store the path and name of each file in a dictionary
```aider
in chunk_to_md.py, create function retrieve_files_in_directory(PDFToMarkdownState):

    - write a function that will look inside the directory at filepath, if there are subdirectories (search recursively) it will look inside all of them as well and retrieve all text files in the directory and its subdirectories. The text files usually have the .md extension.
    
    append the filepaths to the files_dict dictionary, using the name of the file as the key and the path to the file as the value.

    return the files_dict dictionary
```

4.  Modify chunk_file_node used to receive a filepath as an argument, but now it will receive files_dict {file_name: filepath}. Instead of using the filepath from the state, it will use the filepath from the files_dict stored in the state.
```aider
in chunk_to_md.py, modify the chunk_file_node(state: PDFToMarkdownState):
"""Itterate over the files_dict and chunk each of the files separately, stored the extracted text into a dictionary of chunks."""
loop over the files_dict and apply the chunk_file function to each of the files.
Note: chunk_file Returns a dictionary with: {Keys: Integer chunk numbers (starting from 1), Values: String chunks of text}

store returned dictionnary in state['chunks_dict'], and since we are processing multiple files, the keys of the dictionary should be the file_name and the values will be the dictionary returned by chunk_file. see example of nested dictionary for reference

 return {"chunks_dict": state['chunks_dict']}
```

5. Modify the send_to_clean_node function to be able to itterate over the chunks_dict.
```aider
in chunk_to_md.py, modify the send_to_clean_node(state: PDFToMarkdownState):

modify logger.info("Sending files to cleaner -- in progress")
remove """
    total_words = 0
    for chunk_number, chunk_text in state['chunks_dict'].items():
        word_count = len(chunk_text.split())
        total_words += word_count
        logger.info(f"Chunk {chunk_number}: {word_count} words")
    logger.info(f"Total words across all chunks: {total_words}")
"""
modify     return [
        Send(
            "clean_text",
            {
                "chunk_name": file_name,
                "chunk_number": chunk_number,
                "chunk_text": chunk_text,
                "qa_loop_limit": state['qa_loop_limit'],
                "chunk_feedback_application_counter": 0
            }
        )
        use a for loop to itterate through state['chunks_dict'], recall chunks_dict is a dictionary of dictionaries, the outer dictionary is the file name, and the inner dictionary is the chunk number and the chunk text.
        {
            "file_name_1": {
                "chunk_number_1": "chunk_text_1",
                "chunk_number_2": "chunk_text_2",
                "chunk_number_3": "chunk_text_3"
            },
            "file_name_2": {
                "chunk_number_1": "chunk_text_1",
                "chunk_number_2": "chunk_text_2",
                "chunk_number_3": "chunk_text_3"
            }
        }
        the for loop will itterate through the dictionnary to extract file_name, chunk_number and chunk_text.
]
```

6. modify ChunktoMarkdownInputState to be able to handle the new state.
```aider
class ChunktoMarkdownInputState(TypedDict):
    chunk_name: str
    chunk_number: int
    chunk_text: str
    qa_loop_limit: int
    chunk_feedback_application_counter: int
```

7. modify ChunktoMarkdownState to add a new attribute chunk_cleaned_text
```aider
class ChunktoMarkdownState(ChunktoMarkdownInputState, ChunktoMarkdownOutputState):
    chunk_qa_feedback: str
    chunk_cleaned_text: str
```

7. modify restructure_chunk_node to return a nested dictionary with the file name as the key and the chunk number and chunk text as the values.
```aider
in chunk_to_md.py, modify the restructure_chunk_node(state: ChunktoMarkdownInputState) ---> ChunktoMarkdownState:
the function itself will not change. 
change the logging statement to log the file name, chunk number and chunk text.
return {"chunk_cleaned_text": state["chunk_cleaned_text"]}

```

8. modify the get_qa_feedback function to be able to access the right chunk text since we changed the structure of the cleaned_chunk_dict.
```aider
in chunk_to_md.py, modify the get_qa_feedback function:
modify the variable cleaned_text = state["chunk_cleaned_text"]
everything else will remain the same.
```

9. modify the apply_qa_feedback function to access the state["chunk_cleaned_text"]
```aider
in chunk_to_md.py, modify the apply_qa_feedback function:
modify the variable current_cleaned = state["chunk_cleaned_text"]

re-apply the feedback to the chunk_cleaned_text
change  this: state["cleaned_chunk_dict"][state["chunk_number"]] = result.content, to that: state["chunk_cleaned_text"] = result.content

return {
    "chunk_cleaned_text": state["chunk_cleaned_text"],
    "chunk_feedback_application_counter": state["chunk_feedback_application_counter"]
}
```

10. 


What is chunks_dict ? 
it's the initial dictionary that contains the file name as the key and the chunk number and chunk text as the values.
        {
            "file_name_1": {
                "chunk_number_1": "chunk_text_1",
                "chunk_number_2": "chunk_text_2",
                "chunk_number_3": "chunk_text_3"
            },
            "file_name_2": {
                "chunk_number_1": "chunk_text_1",
                "chunk_number_2": "chunk_text_2",
                "chunk_number_3": "chunk_text_3"
            }
        }


change the return statement to return a nested dictionary with the file name as the key for the first tier, and the chunk number as the key for the second tier, and chunk text as the value as in the example of nested dictionary.