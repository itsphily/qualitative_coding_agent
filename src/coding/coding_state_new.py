from typing import List, TypedDict
from pydantic import BaseModel, Field
import operator
from typing_extensions import Annotated
from langchain_core.tools import tool
from coding_utils import merge_lists

class CodingAgentState(TypedDict):
    charity_id: str
    charity_directory: str
    research_question: str
    code_list: List[str]
    code_and_research_question_prompt_variable: str
    prompt_per_code_results: Annotated[list, merge_lists]

class CodingAgentOutputState(TypedDict):
    markdown_output: str

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

class InvokePromptPerCodeState(TypedDict):
    prompt_per_code:str
    code:str
    charity_id:str
    doc_name:str
    doc_text:str
    invoke_results: Annotated[any, operator.add]

class InvokePromptOutputState(TypedDict):
    code: str
    charity_id: str
    quote: str
    reasoning: str

class StructuredOutputPerCode(BaseModel):
    code: str = Field(description="The code that was used to extract the information")
    charity_id: str = Field(description="The ID of the charity")
    doc_name: str = Field(description="The name of the document")
    quote: str = Field(description="The quote that was extracted from the document")
    reasoning: str = Field(description="The reasoning that was used to extract the information")
