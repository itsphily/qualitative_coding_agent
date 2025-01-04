# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

-  UPDATE main to take in a filepath as CLI argument, UPDATE the graph to add a save_final_markdown node, and connect it to the END node

## Mid-Level Objective

-  MODIFY def main() to take the filepath as a CLI argument
-  CREATE a function that will save the cleaned text stored in state.cleaned_text to a storage folder
-  UPDATE continue_qa_feedback_node to return qa_feedback_node (if state.feedback_application_counter is less than or equal to 2) and save_final_markdown_node otherwise. 
- ADD node save_final_markdown_node to the graph, MIRROR restructure_text_node
- ADD edge save_final_markdown_node, MIRROR restructure_text_node but instead of being connected to START, and qa_feedback_node, connect it to apply_qa_feedback_node, and END

## Implementation Notes
- When saving the final markdown file, save them in a folder called final_markdown_files, the files should be saved in subfolders named using the same structure as the filepath starting from nougat_extracted_text
-  when adding the nodes use .add('<node_name>', <node_function_name>) convention to Mirror the addition of other nodes that are already in the graph.
-  when adding the edges /drop convention to Mirror the addition of other edges that are already in the graph.

## Context

### Beginning context
- /src/PDF extract to md one prompt.py
- /src/utils.py
- /src/state.py

### Ending context  
- /src/PDF extract to md one prompt.py
- /src/utils.py
- /src/state.py

## Low-Level Tasks
> Ordered from start to finish

1. MODIFY def main() to take the filepath as a CLI argument
```aider
def main() should take the filepath as a CLI argument with the flag --filepath
```
2. CREATE a function that will save the cleaned text stored in state.cleaned_text to a storage folder
```aider
def save_final_markdown(filepath: str, cleaned_text: str):
    take the filepath from the CLI argument, to get the folder structure (start from nougat_extracted_text)
    use the folder structure to create if necessary the right folder in which to save the file
    Save the cleaned text stored in state.cleaned_text to a file in the right folder
    
```
3. UPDATE continue_qa_feedback_node
```aider
MODIFY continue_qa_feedback_node to return qa_feedback_node (if state.feedback_application_counter is less than or equal to 2) and save_final_markdown_node otherwise. 
```
4. ADD node save_final_markdown_node to the graph, MIRROR restructure_text_node
```aider
ADD node save_final_markdown_node to the graph, MIRROR restructure_text_node
```
5. ADD edge save_final_markdown_node, MIRROR restructure_text_node but instead of being connected to START, and qa_feedback_node, connect it to apply_qa_feedback_node, and END
```aider
ADD edge save_final_markdown_node, MIRROR restructure_text_node but instead of being connected to START, and qa_feedback_node, connect it to apply_qa_feedback_node, and END
```