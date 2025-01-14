from typing import List, TypedDict
import operator
from typing_extensions import Annotated

class CodingAgentState(TypedDict):
    charity_id: str
    charity_overview: str
    charity_directory: str
    research_question: str
    project_description: str
    prompt_for_project: str
    code_list: List[str]
    list_output_per_code: Annotated[List[str], operator.add]

class CodingAgentOutputState(TypedDict):
    list_output_per_code: Annotated[List[str], operator.add]

class CodingAgentInputState(TypedDict):
    charity_id: str
    charity_overview: str
    charity_directory: str
    research_question: str
    project_description: str
    prompt_for_project: str
    code_list: List[str]

class AgentPerCodeState(TypedDict):
    prompt_per_code: str
    charity_directory: str
    doc_text_list: List[str]
    list_output_per_code: Annotated[List[str], operator.add]
    list_output_per_code_per_doc: Annotated[List[str], operator.add]

class AgentPerCodeInputState(TypedDict):
    prompt_per_code: str
    charity_directory: str

class AgentRunState(TypedDict):
    prompt_per_code: str
    doc_text: str

class AgentRunOutputState(TypedDict):
    output_per_code_per_doc: str

class AgentPerCodeOutputState(TypedDict):
    output_per_code: str
