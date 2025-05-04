from typing import TypedDict, List, Dict, Optional

class QualitativeAnalysisInputState(TypedDict):
    research_question: str
    code_list: List[str]
    case_list: List[Dict]

class QualitativeAnalysisState(QualitativeAnalysisInputState):
    case_interventions: Dict[str, str]
    codes_to_process_aspects: List[str]
