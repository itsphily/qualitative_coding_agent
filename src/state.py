from dataclasses import dataclass, field
from typing_extensions import TypedDict, Annotated
from typing import Dict
from dotenv import load_dotenv
import os
import operator

load_dotenv()

@dataclass(kw_only=True)
class EvaluationResult:
    metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    overall_quality_score: float = field(default=None)
    grade: str = field(default=None)

# State
#------------------------------------------------------------------------------

@dataclass(kw_only=True)
class PDFToMarkdownState:
    filepath: str = field(default=None)
    extracted_text: str = field(default=None)
    cleaned_text: str = field(default=None)
    qa_feedback: str = field(default=None)
    feedback_application_counter: int = field(default=0)
    evaluation_result: EvaluationResult = field(default=None)

@dataclass(kw_only=True)
class PDFToMarkdownInputState(TypedDict):
    filepath: str = field(default=None)
    extracted_text: str = field(default=None)

@dataclass(kw_only=True)
class PDFToMarkdownOutputState(TypedDict):
    cleaned_text: str = field(default=None) # Final report
    evaluation_result: EvaluationResult = field(default=None)
