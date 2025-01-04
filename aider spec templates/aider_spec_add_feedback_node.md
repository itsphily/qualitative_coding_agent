# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- MODIFY the graph to add a loop that will run the graph until the cleaned text is satisfactory (max of 2 iterations)

## Mid-Level Objective

- ADD a feedback_application_counter to PDFToMarkdownState, initialize it to 0
- CREATE a conditional node that will return the name of the node to run next based on the feedback_application_counter (if it is greater or equal to 2, return END, otherwise return apply_qa_feedback)
- Update the graph to add the conditional node 
- Update the graph to ADD the conditional edge between qa_feedback_node and apply_qa_feedback_node


## Implementation Notes
- The conditional node must take the feedback_application_counter as an input, itterate, and return it.
-  when adding the nodes use .add('<node_name>', <node_function>) convention to Mirror the addition of other nodes that are already in the graph.
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

1. ADD a feedback_application_counter to PDFToMarkdownState
```aider
ADD a feedback_application_counter to PDFToMarkdownState, initialize it to 0
```
2. CREATE a conditional node 
```aider
CREATE a continue_qa_feedback_node that will return the name of the node to run next based on the feedback_application_counter (if it is greater or equal to 2, return END, otherwise return apply_qa_feedback)
```
3. Update the graph to add the conditional node 
```aider
Update the graph to add the conditional node 
Mirror the addition of other nodes that are already in the graph.
```

4. Update the graph to ADD the conditional edge between qa_feedback_node and apply_qa_feedback_node
```aider
Update the graph to ADD the conditional edge between qa_feedback_node and apply_qa_feedback_node
Mirror the addition of other edges, use .add_conditional_edges('<node_name>', <node_function>)
```