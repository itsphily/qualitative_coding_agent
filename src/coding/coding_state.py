from typing import TypedDict, List, Dict, Optional, Annotated

class Code(TypedDict):
    code_description: str
    key_aspects: Optional[List[str]]

class CaseInfo(TypedDict):
    directory: str
    description: Optional[str]
    intervention: Optional[str]

class CodingState(TypedDict):
    research_question: str
    codes: Annotated[Optional[List[Code]], update_codes_list_reducer]
    cases_info: Dict[str, CaseInfo]
