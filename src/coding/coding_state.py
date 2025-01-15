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
    list_output_per_code_per_doc: Annotated[list, operator.add]

class CodingAgentOutputState(TypedDict):
    list_output_per_code_per_doc: Annotated[list, operator.add]

class AgentPerCodeState(TypedDict):
    prompt_per_code: str
    charity_directory: str
    doc_text: str
