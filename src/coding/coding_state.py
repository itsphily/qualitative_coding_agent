from typing import TypedDict, List, Dict, Optional, Annotated, Any
from langgraph.graph import MessagesState

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

    current.update(new)
    return current

def merge_case_info(
    current: Optional[Dict[str, Dict[str, Any]]],
    new: Optional[Dict[str, Dict[str, Any]]],
) -> Dict[str, Dict[str, Any]]:
    """
    Merges new case info into the current state.
    
    Args:
        current: Dictionary mapping case ids to CaseInfo objects
        new: Dictionary containing updates of case ids to CaseInfo objects
    
    Returns:
        Updated dictionary with merged case info
    """
    if current is None:
        current = {}
    if new is None:
        return current
    
    # For each case_id in the new dictionary
    for case_id, new_info in new.items():
        if case_id in current:
            # If the case_id exists in current, update its fields with new values
            current[case_id].update(new_info)
        else:
            # If the case_id doesn't exist, add it
            current[case_id] = new_info
    
    return current

def merge_evidence_list(
    current: Optional[Dict[str, List[Dict[str, Any]]]],
    new: Optional[Dict[str, List[Dict[str, Any]]]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Merges new evidence into the current state based on case descriptions.
    
    Args:
        current: Dictionary mapping case descriptions to their evidence lists
        new: Dictionary containing updates of case descriptions to evidence lists
    
    Returns:
        Updated dictionary with merged evidence lists
    """
    if current is None:
        current = {}
    if new is None:
        return current
    
    # For each case_description in the new dictionary
    for case_description, new_evidence_list in new.items():
        if case_description in current:
            # If the case_description exists in current, extend its evidence list
            current[case_description].extend(new_evidence_list)
        else:
            # If the case_description doesn't exist, add it with its evidence list
            current[case_description] = new_evidence_list
    
    return current

def append_evidence(
    current: Optional[List[Any]],
    new: Optional[List[Any]]
) -> List[Any]:
    """
    Appends new items to a list.
    Handles None values gracefully.
    
    Args:
        current: Current list
        new: New list of items to append
        
    Returns:
        Combined list
    """
    if current is None:
        current = []
    if new is None:
        return current
    
    return current + new

def merge_evidence_from_subgraph(
    current: Optional[Dict[str, List[Any]]], 
    new: Optional[List[Any]]
) -> Dict[str, List[Any]]:
    """
    Merges evidence from subgraph into the main state's evidence_list.
    
    Args:
        current: Current evidence_list in main state (dict keyed by code)
        new: New evidence list from subgraph (flat list)
    
    Returns:
        Updated evidence_list with evidence grouped by code_description
    """
    if current is None:
        current = {}
    if not new:
        return current
    
    # Group new evidence by code_description
    for item in new:
        if not isinstance(item, dict):
            continue
            
        code_desc = item.get("code_description", "unknown")
        if code_desc not in current:
            current[code_desc] = []
        current[code_desc].append(item)
    
    return current

class Evidence(TypedDict):
    quote: str
    reasoning: str
    aspect: List[str]
    chronology: str
    code_description: str  # For tracking which code this evidence belongs to
    doc_name: str  # For tracking source document

class CaseInfo(TypedDict):
    directory: str
    description: Optional[str]
    intervention: Optional[str]

class CaseProcessingState(MessagesState):
    case_id: str
    directory: str
    intervention: str
    research_question: str
    codes: Dict[str, List[str]]
    evidence_list: Annotated[List[Evidence], append_evidence]

class CodingState(TypedDict):
    research_question: str
    codes: Annotated[Dict[str, Optional[List[str]]], merge_aspects]
    cases_info: Annotated[Dict[str, CaseInfo], merge_case_info]
    evidence_list: Annotated[Dict[str, List[Evidence]], merge_evidence_from_subgraph]
