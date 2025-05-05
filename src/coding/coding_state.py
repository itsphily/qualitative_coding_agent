from typing import TypedDict, List, Dict, Optional, Annotated, Any, Union
import logging

class Code(TypedDict):
    code_description: str
    key_aspects: Optional[List[str]]

def merge_aspects(
    current: Optional[Dict[str, Optional[List[str]]]],
    new: Optional[Dict[str, List[str]] | List[Dict[str, List[str]]]],
) -> Dict[str, Optional[List[str]]]:
    if current is None:
        current = {}
    if new is None:
        return current
    if not isinstance(new, list):
        new = [new]
    for update in new:
        if isinstance(update, dict):
            current.update(update)        # dict.update is associative
    return current

class CaseInfo(TypedDict):
    directory: str
    description: Optional[str]
    intervention: Optional[str]

class CodingState(TypedDict):
    research_question: str
    codes: Annotated[Dict[str, Optional[List[str]]], merge_aspects]
    cases_info: Dict[str, CaseInfo]
