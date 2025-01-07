# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- [High level goal goes here - what do you want to build?]

## Mid-Level Objective

- [List of mid-level objectives - what are the steps to achieve the high-level objective?]
- [Each objective should be concrete and measurable]
- [But not too detailed - save details for implementation notes]

## Implementation Notes
- [Important technical details - what are the important technical details?]
- [Dependencies and requirements - what are the dependencies and requirements?]
- [Coding standards to follow - what are the coding standards to follow?]
- [Other technical guidance - what are other technical guidance?]

## Context

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
## Mid-Level Objective



- In src/chunk_to_md.py, CREATE a graph (the cleaning subgraph) that will take the chunks dict and return a cleaned chunk dictionary. The state of the graph will be ChunktoMarkdownState, with the input state being ChunktoMarkdownInputState, and the output state being ChunktoMarkdownOutputState. This subgraph will be similar to the one in src/PDF extract to md one prompt.py. MODIFY the graph in src/PDF extract to md one prompt.py to use the following nodes only: restructure_chunk_node, qa_feedback_node, apply_qa_feedback_node, save_to_cleaned_chunks_dict_node.


- MODIFY the save_final_markdown_node to save the cleaned chunks to a dict (the cleaned chunks is the value, and the chunk number is the key)