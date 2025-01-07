# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- CREATE 3 new files (src/chunk_to_md.py, src/chunk_state.py, src/chunk_utils.py) based on the existing files (src/PDF extract to md one prompt.py, src/state.py, src/utils.py) that will instead implement a chunking graph(chunks up and combines the chunks when cleaned), and a cleaning graph(clean the chunks and returns a cleaned chunk dictionary).

## Mid-Level Objective

- CREATE file src/chunk_to_md.py 
- CREATE file src/chunk_state.py
- CREATE file src/chunk_utils.py
- In src/chunk_state.py, CREATE PDFToMarkdownState, PDFToMarkdownInputState, PDFToMarkdownOutputState, ChunktoMarkdownState, ChunktoMarkdownInputState, ChunktoMarkdownOutputState
- Mirror the main function in src/PDF extract to md one prompt.py, import statements, and llm initialization (remove all llm initialization except the deepseek one)
- In src/chunk_utils.py, CREATE a function that will take a markdown file and return a dictionnary of chunks, and the chunk number which will be used to sort the chunks by chunk number in the correct order (the key will be the chunk number).
- In src/chunk_to_md.py, CREATE a graph that will that will first take the markdown file associated to the filepath specified in the args and return a list of chunks and the chunk number. return the chunk number as a key in the dictionnary, and the chunk text as the value. second, use the send API to send each chunk to the chunk_cleaner subgraph. third, receive the cleaned chunks dict which will be re-combined in order into a final markdown file.
- In src/chunk_to_md.py, CREATE a graph (the cleaning subgraph) that will take the chunks dict and return a cleaned chunk dictionary. The state of the graph will be ChunktoMarkdownState, with the input state being ChunktoMarkdownInputState, and the output state being ChunktoMarkdownOutputState. This subgraph will be similar to the one in src/PDF extract to md one prompt.py. MODIFY the graph in src/PDF extract to md one prompt.py to use the following nodes only: restructure_chunk_node, qa_feedback_node, apply_qa_feedback_node, save_to_cleaned_chunks_dict_node.
- MODIFY the save_final_markdown_node to save the cleaned chunks to a dict (the cleaned chunks is the value, and the chunk number is the key)


- CREATE a dataclass that will store the chunk number, chunk text
- ADD from typing import Annotated
- CREATE a function using Langgraph's send API to run the graph for each chunk.

## Implementation Notes
- Each chunk should be roughly 2000 words, however the chunks should be truncated only at the end of a sentence.
- See below for an example of sorting reducer and how to use it in the state.
- See below for an example of how to use the send API. In that example, the send API is used to send each subject contained in the state["subjects"] list to the generate_joke node.
- When saving the final markdown file, save them in a folder called final_markdown_files, the files should be saved in subfolders named using the same structure as the filepath starting from nougat_extracted_text
-  when adding the nodes use .add('<node_name>', <node_function_name>) convention to Mirror the addition of other nodes that are already in the graph.
-  when adding the edges /drop convention to Mirror the addition of other edges that are already in the graph.
- to implement a subgraph, use the following convention:  <name of the current graph>.add_edge(<name of the node>, <name of the subgraph>.compile()). Also see subgraph example below.
- (IMPORTANT) Langgraph uses a stateful approach, the functions that are used to create the graph must take the state as an argument, and will return a value that will be used to update an attribute in the state.
- MODIFY the imports from src/chunk_to_md.py to import the functions from src/chunk_state.py and src/chunk_utils.py
- USE prompt.py to create the prompt for the nodes. MIRROR the use of prompt.py in src/PDF extract to md one prompt.py
- CREATE a main function that will take the filepath and qa_loop_limit as a CLI argument, and run the graph

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

## Context

### Beginning context
- src/PDF extract to md one prompt.py (read only)
- src/state.py (read only)
- src/utils.py (read only)
- src/prompt.py (read only)

### Ending context  
- src/PDF extract to md one prompt.py (read only)
- src/state.py (read only)
- src/utils.py (read only)
- src/chunk_to_md.py
- src/chunk_state.py
- src/chunk_utils.py
- src/prompt.py (read only)

## Low-Level Tasks
> Ordered from start to finish

1. CREATE file src/chunk_to_md.py 
```aider
CREATE file src/chunk_to_md.py, MIRROR the imports from src/PDF extract to md one prompt.py
```
2. CREATE file src/chunk_state.py
```aider
CREATE file src/chunk_state.py, MIRROR the imports from src/state.py
```
3. CREATE file src/chunk_utils.py
```aider
CREATE file src/chunk_utils.py, MIRROR the imports from src/utils.py
```
4. CREATE PDFToMarkdownState
```aider
add extracted_text: str
add filepath: str
add cleaned_text: str
add chunks_dict: dict
add cleaned_chunks_dict: dict
```
5. CREATE PDFToMarkdownInputState
```aider
add extracted_text: str
add filepath: str
add qa_loop_limit: int
```
6. CREATE PDFToMarkdownOutputState
```aider
add cleaned_text: str
```
7. CREATE ChunktoMarkdownState
```aider
add chunk_dict: dict
add chunk_text: str
add cleaned_chunk_text: str
add chunk_qa_feedback: str
add chunk_feedback_application_counter: int
add cleaned_chunk_dict: dict
add qa_loop_limit: int
```
8. CREATE ChunktoMarkdownInputState
```aider
add chunk_dict: dict
add qa_loop_limit: int
```
9. CREATE ChunktoMarkdownOutputState
```aider
add cleaned_chunk_dict: dict
```

10. ADD the llm initialization to src/chunk_to_md.py
```aider
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

11. in src/chunk_utils.py, CREATE def chunk_file that will take a markdown file and return a dict of chunks with the ordered chunk number as the key and the chunk text as the value
```aider
CREATE a function that will take the markdown file specified in the args and return a dict of chunks and the chunk number. 
The chunk number must be an int that is linked to the position of the chunk in the list (the chunk number must allow us to sort the chunks by chunk number in the correct order).
The chunks should only be truncated at the end of a sentence, and roughly 2000 words.
```

12. in src/chunk_to_md.py, CREATE a graph (the cleaning subgraph) that Mirrors the graph in src/PDF extract to md one prompt.py, but instead of using the nodes restructure_text_node, qa_feedback_node, apply_qa_feedback_node, save_final_markdown_node, use the nodes chunk_file_node, send_to_clean_node, save_to_cleaned_chunks_dict_node
```aider
chunk_cleaner = StateGraph(ChunktoMarkdownState, input = ChunktoMarkdownInputState, output = ChunktoMarkdownOutputState)
chunk_cleaner.add_node('restructure_chunk_node', restructure_chunk_node)
chunk_cleaner.add_node('qa_feedback_node', get_qa_feedback)
chunk_cleaner.add_node('apply_qa_feedback_node', apply_qa_feedback)
chunk_cleaner_builder.add_node('save_to_cleaned_chunks_dict_node', save_to_cleaned_chunks_dict)

chunk_cleaner.add_edge(START, 'restructure_chunk_node')
chunk_cleaner.add_edge('restructure_chunk_node', 'qa_feedback_node')
chunk_cleaner.add_edge('qa_feedback_node', 'apply_qa_feedback_node')
chunk_cleaner.add_edge('apply_qa_feedback_node', continue_qa_feedback_node)
chunk_cleaner.add_edge('save_to_cleaned_chunks_dict_node', END)


graph = builder.compile()
```

13. Create def restructure_chunk_node
```aider
CREATE a function that will take the ChunktoMarkdownState and return a restructured chunk text and the add qa_loop_limit inherited from the PDFToMarkdownState. MIRROR the restructure_text_node function in src/PDF extract to md one prompt.py
```

14. Create def get_qa_feedback
```aider
CREATE a function that will take the ChunktoMarkdownState and return a qa feedback. MIRROR the get_qa_feedback function in src/PDF extract to md one prompt.py
```

15. Create def apply_qa_feedback
```aider
CREATE a function that will take the ChunktoMarkdownState and return a chunk text with the qa feedback applied. MIRROR the apply_qa_feedback function in src/PDF extract to md one prompt.py
```

16. Create def continue_qa_feedback_node
```aider
MIRROR the continue_qa_feedback_node function in src/PDF extract to md one prompt.py, UPDATE the function to use chunk_feedback_application_counter
MODIFY the if statement to use a qa_loop_limit (see step 21 for more details) instead of a hardcoded value. 
return qa_feedback_node if chunk_feedback_application_counter is less than or equal to 2, otherwise return save_to_cleaned_chunks_dict_node
```

17. Create def save_to_cleaned_chunks_dict
```aider
CREATE a function that will take the ChunktoMarkdownState, use the state.cleaned_chunk_text to save the cleaned chunk text to a dict. MIRROR the save_final_markdown function in src/PDF extract to md one prompt.py but instead of saving the cleaned text to a file, save it to a dict.
return the cleaned_chunk_dict
```

18. in src/chunk_to_md.py, CREATE the main graph
```aider
main_graph = StateGraph(PDFToMarkdownState, input = PDFToMarkdownInputState, output = PDFToMarkdownOutputState)
main_graph.add_node('chunk_file_node', chunk_file)
main_graph.add_node('clean_text', chunk_cleaner.compile())
main_graph.add_node('compile_clean_text', compile_clean_text)
main_graph.add_node('save_final_markdown', save_final_markdown)

main_graph.add_edge(START, 'chunk_file_node')
main_graph.add_edge('chunk_file_node', 'clean_text')
main_graph.add_edge('clean_text', 'compile_clean_text')
main_graph.add_edge('compile_clean_text', 'save_final_markdown')
main_graph.add_edge('save_final_markdown', END)

graph = builder.compile()
```

19. CREATE def compile_clean_text
```aider
CREATE a function that will take the PDFToMarkdownState, use the state.cleaned_chunks_dict to combine in order using the chunk number as the key, the cleaned chunk text as the value, and return the cleaned_text. 
```

20. CREATE def save_final_markdown a function that will take the cleaned text stored in state.cleaned_text, save the content to a markdown file, and store it in the appropriate folder
```aider
def save_final_markdown(filepath: str, cleaned_text: str):
    take the filepath from the CLI argument, to get the folder structure (start from nougat_extracted_text)
    use the folder structure to create if necessary the right folder in which to save the file
    Save the cleaned text stored in state.cleaned_text to a file in the right folder
```

21. CREATE a main function that will take the filepath as a CLI argument, and run the graph
```aider
MIRROR the main function in src/PDF extract to md one prompt.py, but instead of using the graph in src/PDF extract to md one prompt.py, use the main_graph in src/chunk_to_md.py
ADD qa_loop_limit (default should be 1)as an argument that could be passed as a CLI argument. 
```
