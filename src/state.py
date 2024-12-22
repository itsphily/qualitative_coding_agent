from dataclasses import dataclass, field
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
import os
import operator

load_dotenv()

# State
#------------------------------------------------------------------------------
@dataclass(kw_only=True)
class qa_feedback(TypedDict):
    qa_feedback: str = field(default= None)

@dataclass(kw_only=True)
class PDFToMarkdownState:
    extracted_text: str = field(default= None)
    cleaned_text: str= field(default= None)
    qa_feedback_list: Annotated[qa_feedback, operator.add] = field(default_factory= list)

@dataclass(kw_only=True)
class PDFToMarkdownInputState(TypedDict):
    extracted_text: str = field(default = None) # Report topic

@dataclass(kw_only=True)
class PDFToMarkdownOutputState(TypedDict):
    cleaned_text: str = field(default = None) # Final report