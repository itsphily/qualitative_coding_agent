from typing import List, TypedDict
from pydantic import BaseModel, Field
import operator
from typing_extensions import Annotated
from langchain_core.tools import tool
from coding_utils import merge_lists

class CodingAgentInputState(TypedDict):
    charity_id: str
    charity_directory: str
    research_question: str
    code_list: List[str]
    prompt_per_code_results: Annotated[list, merge_lists]
    unprocessed_documents: Annotated[list, merge_lists] 

class CodingAgentState(TypedDict):
    markdown_output: dict[str, str]
    prompt_per_code_results: Annotated[list, merge_lists]
    unprocessed_documents: Annotated[list, merge_lists] 

class CodingAgentOutputState(TypedDict):
    markdown_output: dict[str, str]
    prompt_per_code_results: Annotated[list, merge_lists]
    unprocessed_documents: Annotated[list, merge_lists] 

class InvokePromptInputState(TypedDict):
    code_and_research_question_prompt_variable: str
    charity_id: str
    charity_directory: str
    code: str

class InvokePromptState(TypedDict):
    code_and_research_question_prompt_variable: str
    charity_id: str
    charity_directory: str
    code: str
    research_question_with_code: str
    prompt_per_code_results: Annotated[list, merge_lists]

class InvokePromptOutputState(TypedDict):
    prompt_per_code_results: Annotated[list, merge_lists]

class InvokePromptPerCodeState(TypedDict):
    prompt_per_code:str
    code:str
    charity_id:str
    doc_name:str
    doc_path:str
    doc_text:str
    invoke_results: Annotated[any, operator.add]

class QuoteReasoningPair(BaseModel):
    quote: str = Field(..., description="The quote that was extracted from the document")
    reasoning: str = Field(..., description="The reasoning that was used to extract the information")

class StructuredOutputPerCode(BaseModel):
    quote_reasoning_pairs: List[QuoteReasoningPair] = Field(
        ...,
        description=(
            "A list of quote–reasoning pairs. "
            "If the AI finds one pair, this list will have one element: [(Quote, reasoning)]. "
            "If it finds three pairs, the list will have three elements: "
            "[(Quote#1, reasoning#1), (Quote#2, reasoning#2), (Quote#3, reasoning#3)]."
        )
    )
    document_importance: str = Field(
        ...,
        description="The importance of the document to the research question, either 'important to read', 'worth reading', or 'not worth reading'"
    )
