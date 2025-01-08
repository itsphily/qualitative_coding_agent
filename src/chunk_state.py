from dataclasses import dataclass, field
from typing import Dict
from typing_extensions import TypedDict
from state import EvaluationResult
from dotenv import load_dotenv
from typing import Annotated
import operator

load_dotenv()

class PDFToMarkdownState(TypedDict):
    extracted_text: str 
    filepath: str 
    cleaned_text: str 
    chunks_dict: Dict
    cleaned_chunk_dict: Dict
    qa_loop_limit: int

class PDFToMarkdownInputState(TypedDict):
    extracted_text: str
    filepath: str
    qa_loop_limit: int

class PDFToMarkdownOutputState(TypedDict):
    cleaned_text: str

class ChunktoMarkdownState(TypedDict):
    chunks_dict: Dict
    chunk_number: int
    chunk_text: str
    cleaned_chunk_text: str 
    chunk_qa_feedback: str 
    chunk_feedback_application_counter: int
    cleaned_chunk_dict: Dict
    qa_loop_limit: int

class ChunktoMarkdownInputState(TypedDict):
    chunk_number: int
    chunk_text: str
    qa_loop_limit: int 
    chunk_feedback_application_counter: int
    
class ChunktoMarkdownOutputState(TypedDict):
    cleaned_chunk_dict: Dict
