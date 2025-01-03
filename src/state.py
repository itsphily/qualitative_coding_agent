from dataclasses import dataclass, field
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
import os
import operator

load_dotenv()

# State
#------------------------------------------------------------------------------

@dataclass(kw_only=True)
class PDFToMarkdownState:
    filepath: str = field(default=None)
    extracted_text: str = field(default=None)
    cleaned_text: str = field(default=None)
    qa_feedback: str = field(default=None)
    feedback_application_counter: int = field(default=0)

@dataclass(kw_only=True)
class PDFToMarkdownInputState(TypedDict):
    filepath: str = field(default=None)
    extracted_text: str = field(default=None)

@dataclass(kw_only=True)
class PDFToMarkdownOutputState(TypedDict):
    cleaned_text: str = field(default = None) # Final report
