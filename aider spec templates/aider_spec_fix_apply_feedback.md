# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Update the graph functions to properly extract the text from the PDF

## Mid-Level Objective

- Mirror  def restructure_text(state: PDFToMarkdownState) to Update def qa_feedback_prompt(state: PDFToMarkdownState) to compare the cleaned text stored in state.cleaned_text to the original text stored in state.extracted_text and return the QA feedback stored in state.qa_feedback.
- Mirror  def restructure_text(state: PDFToMarkdownState) to Update def apply_qa_feedback(state: PDFToMarkdownState) to apply the QA feedback stored in state.qa_feedback to the cleaned text stored in state.cleaned_text and return the updated cleaned text in state.cleaned_text.

## Implementation Notes
- No need to significantly change the code, just update the graph functions (def restructure_text(state: PDFToMarkdownState), def apply_qa_feedback(state: PDFToMarkdownState), def qa_feedback_prompt(state: PDFToMarkdownState))
- in langgraph the state is passed as an input to the function, the function will modify the state and return it. Make sure to follow this design pattern when updating the functions.
- Carefully review each low-level task for exact code changes

## Context

### Beginning context
-  /src/PDF extract to md one prompt.py
- /src/utils.py
- /src/prompt.py (readonly)

### Ending context  
- /src/PDF extract to md one prompt.py
- /src/utils.py
- /src/prompt.py (readonly)

## Low-Level Tasks
> Ordered from start to finish

1. Update def qa_feedback_prompt
```aider
UPDATE def qa_feedback_prompt(state: PDFToMarkdownState): 
    MIRROR the llm.invoke code from def restructure_text to pass the qa_feedback_prompt and the extracted_text to the llm.invoke function as SystemMessage. The extracted_text should be passed between xml tags (<Original Text > and </Original Text >). 
    Update the human message to Compare the Original Text against the Restructured Output produced. insert both text between xml tags (<Original Text > and </Original Text >) and (<Restructured Output > and </Restructured Output >).
    USE save_cleaned_text to save the original text, the restructured output and the qa_feedback in the same file (in that order).
```

2. Update def apply_qa_feedback
```aider
UPDATE def apply_qa_feedback(state: PDFToMarkdownState):
    MIRROR the llm.invoke code from def restructure_text to pass the apply_qa_feedback_prompt as system message. Create and Add the human message as "Apply the QA feedback to the cleaned text using the original text as the authoritative reference" ADD the qa_feedback (between xml tags <QA Feedback > and </QA Feedback >), the cleaned text between xml tags (<Cleaned Text > and </Cleaned Text >), and the original text (between xml tags <Original Text > and </Original Text >). 
    USE save_cleaned_text to save the original text, the restructured output (in that order), set the include_feedback to True.
```
