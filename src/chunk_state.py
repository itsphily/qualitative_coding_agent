from typing import Dict
from typing_extensions import TypedDict
from dotenv import load_dotenv
from typing import Annotated
from chunk_utils import merge_dicts

load_dotenv()

class PDFToMarkdownState(TypedDict):
    extracted_text: str 
    filepath: str 
    cleaned_text: str 
    chunks_dict: Dict
    cleaned_chunk_dict: Annotated[Dict[int, str], merge_dicts]
    qa_loop_limit: int

class PDFToMarkdownInputState(TypedDict):
    extracted_text: str
    filepath: str
    qa_loop_limit: int

class PDFToMarkdownOutputState(TypedDict):
    cleaned_text: str

class ChunktoMarkdownInputState(TypedDict):
    chunk_number: int
    chunk_text: str
    qa_loop_limit: int
    chunk_feedback_application_counter: int

class ChunktoMarkdownOutputState(TypedDict):
    cleaned_chunk_dict: Dict

# Merge input + output + optional internal keys
class ChunktoMarkdownState(ChunktoMarkdownInputState, ChunktoMarkdownOutputState):
    chunk_qa_feedback: str

