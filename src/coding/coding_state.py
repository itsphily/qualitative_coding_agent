from typing import List, TypedDict
from pydantic import BaseModel, Field
import operator
from typing_extensions import Annotated
from langchain_core.tools import tool

class CodingAgentState(TypedDict):
    charity_id: str
    charity_directory: str
    research_question: str
    prompt_for_project: str
    code_list: List[str]
    code_and_research_question_prompt: str
    list_output_per_code_per_doc: Annotated[list, operator.add]

class CodingAgentOutputState(TypedDict):
    list_output_per_code_per_doc: Annotated[list, operator.add]

class CodeOutput(TypedDict):
    charity_id: str
    code: str
    quote: str
    reasoning: str

class AgentPerCodeState(TypedDict):
    prompt_per_code: str
    charity_id: str
    charity_directory: str
    code: str
    doc_text: str

class AgentPerCodeState(TypedDict):
    charity_id: str
    code: str
    quote: str
    reasoning: str


class StructuredOutputPerCode(BaseModel):
    quote: str = Field(description="The quote that was extracted from the document")
    reasoning: str = Field(description="The reasoning that was used to extract the information")