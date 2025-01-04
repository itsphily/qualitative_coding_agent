# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Add an evaluation node to the graph

## Mid-Level Objective

- CREATE class EvaluationResult in the state.py file to store the evaluation result
- CREATE def evaluate_restructured_output(state: PDFToMarkdownState) -> EvaluationResult that will evaluate the Restructured Output and return the EvaluationResult
- ADD the evaluation node (evaluate_restructured_output) to the graph below the #Add nodes section
- ADD the evaluation edge to the graph below the #Add edges section. The evaluation edge should appear after apply_qa_feedback_node (before the conditional edge)
- MODIFY src/PDF extract to md one prompt.py to print the EvaluationResult

## Implementation Notes
- when adding the edges /drop convention to Mirror the addition of other edges that are already in the graph.
- when adding the nodes and edges make sure they are added in the right part of the code using the comments to guide you.
- when creating evaluate_restructured_output, MIRROR the following example which takes an input schema and returns a result schema:
<multiple input and output schema >
class InputState(TypedDict):
    user_input: str

class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str

def node_1(state: InputState) -> OverallState:
    # Write to OverallState
    return {"foo": state["user_input"] + " name"}
</multiple input and output schema >

## Context

### Beginning context
- /src/PDF extract to md one prompt.py
- /src/state.py 
- /src/prompt.py (readonly)

### Ending context  
- /src/PDF extract to md one prompt.py
- /src/state.py
- /src/prompt.py (readonly)

## Low-Level Tasks
> Ordered from start to finish

1. CREATE class EvaluationResult in the state.py file to store the evaluation result
```aider
CREATE @dateclass class EvaluationResult to store: {
    "metrics": {
        "boilerplate_removal": {
            "score": 3
        },
        "sentence_reconstruction": {
            "score": 2
        },
        "content_preservation": {
            "score": 3
        },
        "formatting_accuracy": {
            "score": 1
        },
        "absence_commentary": {
            "score": 3
        }
    },
    "overall_quality_score": 73.33,
    "grade": "C"
} (the numbers in this example are arbitrary)
```

2. CREATE def evaluate_restructured_output(state: PDFToMarkdownState) -> EvaluationResult
```aider
CREATE def evaluate_restructured_output(state: PDFToMarkdownState) -> EvaluationResult
FORMAT the system_message to use the evaluate_cleaned_text_prompt
FORMAT the human_message to use the state.extracted_text for the raw_extracted_text and state.cleaned_text for the Restructured_Output
ADD and invoke of llm_json_mode to evaluate the restructured output and return the EvaluationResult
SAVE the result to the EvaluationResult (MIRROR the multiple input and output schema in the implementation notes)
each of the metrics (boilerplate_removal, sentence_reconstruction, content_preservation, formatting_accuracy, absence_commentary,overall_quality_score,grade) should be a key in the metrics dictionary with a score and max value
```

3. ADD the evaluation node (evaluate_restructured_output) to the graph below the #Add nodes section
```aider
in src/PDF extract to md one prompt.py ADD the evaluation node (evaluate_restructured_output) to the graph below the #Add nodes section
```

4. ADD the evaluation edge to the graph below the #Add edges section. The evaluation edge should appear after apply_qa_feedback_node (before the conditional edge)
```aider
in src/PDF extract to md one prompt.py ADD the evaluation edge to the graph below the #Add edges section. The evaluation edge should appear after apply_qa_feedback_node (before the conditional edge)
```

5. MODIFY src/PDF extract to md one prompt.py to print the EvaluationResult
```aider
MODIFY src/PDF extract to md one prompt.py to print the EvaluationResult
```