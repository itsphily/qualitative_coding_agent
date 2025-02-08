# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Modify the code to handle a single structured output from the llm invokation (calling the LLM)

## Mid-Level Objective

- Modify CodingAgentState to include a new field called unprocessed_documents. 
- Modify the invoke_prompt function to handle a single structured output from the llm invokation (calling the LLM)
- Modify the generate_markdown function to handle the new data_list variable, and the unprocessed_documents variable
- Modify the output_to_markdown function to handle the new data_list variable

## Implementation Notes
- in langgraph the state is passed as an input to the function, the function will modify the state and return it. Make sure to follow this design pattern when updating the functions.
- Carefully review each low-level task for exact code changes
- Always make the necessary imports, add them to the requirements.txt file and keep all the imports at the top of the file.
- The directory where the files coding_prompt.py, coding_exec_new.py, coding_utils.py, coding_state_new.py are located is /Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/src/coding
- When creating/modifying a function for the graph, follow the convention shown in the example (node function example below).


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


## Context

### Beginning context
- coding_exec_new.py
- coding_state_new.py
- coding_utils.py
- coding_prompt.py (readonly)
- md_to_pdf.py
- requirements.txt

### Ending context  
- coding_exec_new.py
- coding_state_new.py 
- coding_utils.py
- coding_prompt.py (readonly)
- md_to_pdf.py
- requirements.txt

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
    If there is no error the result variable will look like this:
    <result variable>
    {
  "quote_reasoning_pairs": [
    {
      "quote": "quote extractr from doc text ...",
      "reasoning": "reasoning ...."
    },
    {
      "quote": "quote extractr from doc text ...",
      "reasoning": "reasoning ...."
    },
    {
      "quote": "quote extractr from doc text ...",
      "reasoning": "reasoning ...."
    }
  ],
  "document_importance": "important to read"
}
</result variable>

Each document will have a different number of quote_reasoning_pairs, and some might just have an empty array. You need to create a separate json object for each quote_reasoning_pair using the following format:
<format of each quote_reasoning_pair>
data = {
    "code": state['code'],
    "charity_id": state["charity_id"],
    "doc_name": state["doc_name"],
    "quote": extract one quote from the result variable,
    "reasoning": extract the matching reasoning from the result variable,
    "document_importance": extract the document importance from the result variable
}
</format of each quote_reasoning_pair>
the code, charity_id, doc_name, will be extracted from the state variable, and the quote,reasoning and document importance will be extracted from the result variable. Note that there can be multiple quote_reasoning_pairs in the result variable, and each data object will relate to one quote_reasoning_pair. Then append each data object to the data_list.

Modify all logging information to be relevan to the modified function.

lastly return {"prompt_per_code_results": data_list, "unprocessed_documents": unprocessed_documents}

```

3. in coding_state_new.py, modify the generate_markdown function to handle the new data_list variable, and the unprocessed_documents variable.
```aider
def generate_markdown(documents, unprocessed_documents):

Create a new markdown_doc variable that contain the following strings:
The first string will be a Markdown formatted string grouped by:
    1) code (top-level #)
    2) charity_id (##)
    3) doc_name  - document_importance (###)
    4) list of quote_reasoning_pairs

The second string will be a markdown formatted string grouped by:
    1) Important documents (top-level #) <-- fixed title
    2) document_importance (##)
    3) list of documents
Note in this case the document_importance will be "important to read" or "worth reading" or "not worth reading" and must appear in this order.

The third string will be a markdown formatted list of the unprocessed documents: 
    1) Unprocessed documents (top-level #) <-- fixed title
    2) list of unprocessed documents

Note that each document will have a different number of quote_reasoning_pairs, and some might just have an empty array.

append all three strings to the markdown_doc variable, between each string add a new line and a full line (----) to clearly separate each section.
  
return the markdown_doc variable
```


4. in coding_exec_new.py, modify the output_to_markdown function to handle the new data_list variable.
```aider
 Modify generate_markdown to take the prompt_per_code_results  and the unprocessed_documents markdown_doc = generate_markdown(state['prompt_per_code_results'], state['unprocessed_documents'])
```