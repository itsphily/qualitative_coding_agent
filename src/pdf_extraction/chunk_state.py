from typing import Dict
from typing_extensions import TypedDict
from dotenv import load_dotenv
from typing import Annotated
from chunk_utils import merge_dicts

load_dotenv()

class PDFToMarkdownState(TypedDict):
    extracted_text: str 
    filepath: str 
    cleaned_text: Dict[str, str]
    chunks_dict: Dict[str, Dict[int, str]]
    cleaned_chunk_dict: Annotated[Dict[str, Dict[int, str]], merge_dicts]
    files_dict: Dict[str, str]
    qa_loop_limit: int

class PDFToMarkdownInputState(TypedDict):
    extracted_text: str
    filepath: str
    qa_loop_limit: int


class ChunktoMarkdownInputState(TypedDict):
    chunk_name: str
    chunk_number: int
    chunk_text: str
    qa_loop_limit: int
    chunk_feedback_application_counter: int

class ChunktoMarkdownOutputState(TypedDict):
    cleaned_chunk_dict: Annotated[Dict[str, Dict[int, str]], merge_dicts]

# Merge input + output + optional internal keys
class ChunktoMarkdownState(ChunktoMarkdownInputState, ChunktoMarkdownOutputState):
    chunk_qa_feedback: str
    chunk_cleaned_text: str

