# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Modify the code to handle a single structured output from the llm invokation (calling the LLM)

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
- coding_exec_new.py
- coding_state_new.py
- coding_utils.py
- coding_prompt.py
- md_to_pdf.py

### Ending context  
- coding_exec_new.py
- coding_state_new.py
- coding_utils.py
- coding_prompt.py
- md_to_pdf.py

## Low-Level Tasks
> Ordered from start to finish

1. modify CodingAgentState to include a new field called unprocessed_documents. 
```aider
ADD the field unprocessed_documents to the CodingAgentState type.
unprocessed_documents: Annotated[list, merge_lists]
```

2. in coding_exec_new.py, modify the invoke_prompt function to handle a single structured output from the llm invokation (calling the LLM)
```aider
def invoke_prompt(state:InvokePromptPerCodeState):
    """
    This function invokes the LLM with the prepared prompt for each document.
    """
    system_message = SystemMessage(content=state['prompt_per_code'])
    human_message = HumanMessage(content=text_to_code_prompt.format(text=state['doc_text']))
    data_list = []
    unprocessed_documents = []

    enclose this result = llm_o3_with_structured_output.invoke([system_message, human_message]) in a try/except block. if there is an error, append the document to the unprocessed_documents list.


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