from typing import TypedDict, List, Dict, Optional, Annotated, Any
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

def merge_synthesis_results(
    current: Optional[Dict[str, str]],
    new: Optional[Dict[str, str]]
) -> Dict[str, str]:
    """
    Merges new synthesis results into the current state.
    
    Args:
        current: Dictionary mapping code descriptions to their synthesis results
        new: Dictionary containing new synthesis results for codes
    
    Returns:
        Updated dictionary with merged synthesis results
    """
    if current is None:
        current = {}
    if new is None:
        return current
    
    current.update(new)
    return current

def merge_final_insights_from_subgraph(
    current: Optional[Dict[str, List[Any]]], 
    new: Optional[List[Any]]
) -> Dict[str, List[Any]]:
    """
    Merges final insights from subgraph into the main state's final_insights_list.
    
    Args:
        current: Current final_insights_list in main state (dict keyed by code)
        new: New final insights list from subgraph (flat list)
    
    Returns:
        Updated final_insights_list with insights grouped by code_description
    """
    if current is None:
        current = {}
    if not new:
        return current

    # Group new insights by code_description
    for item in new:
        if not isinstance(item, dict):
            continue

        code_desc = item.get("code_description", "unknown")
        if code_desc not in current:
            current[code_desc] = []
        current[code_desc].append(item)

    return current

def append_evidence(
    current: Optional[List[Any]],
    new: Optional[List[Any]]
) -> List[Any]:
    """
    Reducer for lists, especially CaseProcessingState.evidence_list and CaseProcessingState.final_insights_list.
    - For FinalInsight objects: Updates existing insight if label matches, otherwise appends.
    - For Evidence objects: Appends if quote is unique for that document.
    - For FinalEvidence objects (tool output for FindEvidenceInputState.processed_evidence_for_insight): Appends.
    - For other types: Appends if not an exact duplicate.
    """
    if current is None:
        current = []
    if new is None:
        return current

    logging.info(f"[append_evidence_reducer] Called with {len(current)} current items and {len(new)} new items.")

    # --- Part 1: Handle FinalInsight objects (typically when reducing CaseProcessingState.final_insights_list) ---
    # Create a map of current FinalInsights for efficient update/lookup.
    # These are the FinalInsight objects already in the `current` list being reduced.
    current_final_insights_map = {
        fi['insight_label']: fi
        for fi in current
        if isinstance(fi, dict) and "insight_label" in fi and "insight_explanation" in fi # Identifies FinalInsight
    }

    # Identify FinalInsight objects coming from `new`
    new_final_insight_updates = [
        item for item in new
        if isinstance(item, dict) and "insight_label" in item and "insight_explanation" in item # Identifies FinalInsight
    ]

    for insight_update in new_final_insight_updates:
        label = insight_update['insight_label']
        # This replaces the existing entry in the map or adds a new one.
        current_final_insights_map[label] = insight_update
        logging.info(f"[append_evidence_reducer] Processed (updated/added) FinalInsight '{label}' with {len(insight_update.get('final_evidence_list', []))} evidence items.")

    # --- Part 2: Reconstruct the list and handle other item types ---
    result_list = [
        item for item in current
        if not (isinstance(item, dict) and "insight_label" in item and "insight_explanation" in item)
    ]

    # Add all unique FinalInsights (original, updated, or newly added) from the map
    # This ensures that if 'current' had FinalInsights not present in 'new', they are preserved,
    # and if 'new' had updates, those updates are used.
    result_list.extend(list(current_final_insights_map.values()))
    
    # Identify items in `new` that were not FinalInsight updates (already handled by map)
    other_new_items_to_process = [
        item for item in new
        if not (isinstance(item, dict) and "insight_label" in item and "insight_explanation" in item)
    ]

    # Create sets for de-duplication of Evidence and FinalEvidence items
    # These sets are built from the current state of `result_list` *after* FinalInsights are merged.
    existing_regular_evidence_ids = set()
    for item in result_list:
        if isinstance(item, dict) and "quote" in item and "doc_name" in item and \
           not ("insight_label" in item and "insight_explanation" in item): # Is Evidence
            existing_regular_evidence_ids.add((item["doc_name"], item["quote"][:100]))

    existing_final_evidence_ids = set()
    for item in result_list:
         if isinstance(item, dict) and "insight_label" in item and "agreement_level" in item: # Is FinalEvidence
            key = (item["insight_label"], item.get("evidence_doc_name"), item.get("evidence_quote", "")[:100])
            existing_final_evidence_ids.add(key)


    for item in other_new_items_to_process:
        if isinstance(item, dict):
            # Handling for regular Evidence objects (e.g. from log_quote_reasoning)
            if "quote" in item and "doc_name" in item and \
               not ("insight_label" in item and "insight_explanation" in item): # Is Evidence
                evidence_id = (item["doc_name"], item["quote"][:100])
                if evidence_id not in existing_regular_evidence_ids:
                    result_list.append(item)
                    existing_regular_evidence_ids.add(evidence_id)
                    logging.info(f"[append_evidence_reducer] Added new regular Evidence from doc '{item['doc_name']}': {item['quote'][:30]}...")
                else:
                    logging.info(f"[append_evidence_reducer] Skipping duplicate regular Evidence from doc '{item['doc_name']}': {item['quote'][:30]}...")
            
            # Handling for FinalEvidence objects (e.g. from log_evidence_relationship)
            # This is primarily for the `processed_evidence_for_insight` list within FindEvidenceInputState
            elif "insight_label" in item and "agreement_level" in item: # Is FinalEvidence
                final_evidence_id = (item["insight_label"], item.get("evidence_doc_name"), item.get("evidence_quote","")[:100])
                if final_evidence_id not in existing_final_evidence_ids:
                    result_list.append(item)
                    existing_final_evidence_ids.add(final_evidence_id)
                    logging.info(f"[append_evidence_reducer] Added new FinalEvidence for insight '{item['insight_label']}': {item.get('evidence_quote', '')[:30]}...")
                else:
                    logging.info(f"[append_evidence_reducer] Skipping duplicate FinalEvidence for insight '{item['insight_label']}': {item.get('evidence_quote', '')[:30]}...")
            
            # Fallback for other dictionary types not explicitly handled above
            else:
                is_present = False
                for existing_item in result_list:
                    if existing_item == item: # Simple equality check for other dicts
                        is_present = True
                        break
                if not is_present:
                    result_list.append(item)
                    logging.info(f"[append_evidence_reducer] Added other new dict item: {str(item)[:50]}...")
                else:
                    logging.info(f"[append_evidence_reducer] Skipping duplicate other dict item: {str(item)[:50]}...")
        else:
            # For non-dict items, append if not an exact duplicate in the list
            if item not in result_list:
                result_list.append(item)
                logging.info(f"[append_evidence_reducer] Added other non-dict item: {str(item)[:50]}...")
            else:
                logging.info(f"[append_evidence_reducer] Skipping duplicate other non-dict item: {str(item)[:50]}...")
                
    logging.info(f"[append_evidence_reducer] Returning merged list of {len(result_list)} items.")
    return result_list


class FinalEvidence(TypedDict):
    insight_label: str
    evidence_doc_name: str
    evidence_quote: str
    evidence_chronology: str
    agreement_level: str 
    original_reasoning_for_quote: str 

class FinalInsight(TypedDict):
    code_description: str
    insight_label: str
    insight_explanation: str
    supporting_evidence_summary: str
    final_evidence_list: List[FinalEvidence]

class Evidence(TypedDict):
    quote: str
    reasoning: str
    aspect: List[str]
    chronology: str
    code_description: str 
    doc_name: str  

class CaseInfo(TypedDict):
    directory: str
    description: Optional[str]
    intervention: Optional[str]
    synthesis_results: Annotated[Dict[str, str], merge_synthesis_results]
    revised_synthesis_results: Annotated[Dict[str, str], merge_synthesis_results]
    cross_case_analysis_results: Annotated[Dict[str, str], merge_synthesis_results]
    evidence_list: Optional[List[Evidence]]
    final_insights_list: Annotated[List[FinalInsight], append_evidence]


class CaseProcessingState(TypedDict):
    case_id: str
    directory: str
    intervention: str
    research_question: str
    codes: Dict[str, List[str]]
    evidence_list: Annotated[List[Evidence], append_evidence]
    synthesis_results: Annotated[Dict[str, str], merge_synthesis_results]
    revised_synthesis_results: Annotated[Dict[str, str], merge_synthesis_results]
    cross_case_analysis_results: Annotated[Dict[str, str], merge_synthesis_results]
    final_insights_list: Annotated[List[FinalInsight], append_evidence]

class CodeProcessingState(TypedDict):
    file_path: str
    code_description: str
    aspects: List[str]
    intervention: str
    research_question: str
    case_id: str
    evidence_list: Annotated[List[Evidence], append_evidence]

class CodingState(TypedDict):
    research_question: str
    codes: Annotated[Dict[str, Optional[List[str]]], merge_aspects]
    cases_info: Annotated[Dict[str, CaseInfo], merge_case_info]
    evidence_list: Annotated[List[Evidence], append_evidence]
    final_insights: Annotated[Dict[str, List[FinalInsight]], merge_final_insights_from_subgraph]

class SynthesisState(TypedDict):
    case_id: str
    code_description: str
    research_question: str
    intervention: str
    evidence_subset: List[Dict[str, Any]]

class EvaluateSynthesisState(TypedDict):
    case_id: str
    directory: str
    code_description: str
    research_question: str
    intervention: str
    synthesis_result: str
    
class CrossCaseAnalysisState(TypedDict):
    case_id: str
    code_description: str
    directory: str
    research_question: str
    intervention: str
    aspects: List[str]
    cross_case_analysis_result: str

class FinalInsightState(TypedDict):
      case_id: str
      code_description: str
      research_question: str
      intervention: str
      aspects: List[str]
      revised_synthesis_result: str
      cross_case_analysis_result: str
      final_insights_list: Annotated[List[FinalInsight], append_evidence]

class FindEvidenceInputState(TypedDict):
      current_final_insight: FinalInsight
      full_evidence_list: List[Evidence]
      processed_evidence_for_insight: Annotated[List[FinalEvidence], append_evidence]