from typing import List, TypedDict
from pydantic import BaseModel, Field
import operator
from typing_extensions import Annotated
from langchain_core.tools import tool

class CodingAgentState(TypedDict):
    charity_id: str
    charity_overview: str
    charity_directory: str
    research_question: str
    prompt_for_project: str
    code_list: List[str]
    list_output_per_code_per_doc: Annotated[list, operator.add]

class CodingAgentOutputState(TypedDict):
    list_output_per_code_per_doc: Annotated[list, operator.add]

class AgentPerCodeState(TypedDict):
    prompt_per_code: str
    charity_directory: str
    doc_text: str


class StructuredOutputPerCode(BaseModel):
    code: str = Field(description="The code that was used to extract the information")
    quote: str = Field(description="The quote that was extracted from the document")
    reasoning: str = Field(description="The reasoning that was used to extract the information")