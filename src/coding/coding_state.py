from typing import TypedDict, List, Dict, Optional, Annotated, Any, Union
import logging

def merge_aspects(
    current: Optional[Dict[str, Optional[List[str]]]],
    new: Optional[Dict[str, List[str]]],
) -> Dict[str, Optional[List[str]]]:
    """
    Merges new code aspects into the current state.
    current: Dictionary mapping code descriptions to their aspects
    new: Dictionary containing updates of code descriptions to their aspects
    """
    if current is None:
        current = {}
    if new is None:
        return current
    
    # Simply update the dictionary with the new aspects
    current.update(new)
    return current

class CaseInfo(TypedDict):
    directory: str
    description: Optional[str]
    intervention: Optional[str]

class CodingState(TypedDict):
    research_question: str
    # Dictionary where code_description (string) is the key and value is a list of key aspects
    codes: Annotated[Dict[str, Optional[List[str]]], merge_aspects]
    cases_info: Dict[str, CaseInfo]
