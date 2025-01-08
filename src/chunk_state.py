from dataclasses import dataclass, field
from typing import Dict
from state import EvaluationResult
from dotenv import load_dotenv

load_dotenv()

@dataclass(kw_only=True)
class PDFToMarkdownState:
    extracted_text: str = field(default=None)
    filepath: str = field(default=None)
    cleaned_text: str = field(default=None)
    chunks_dict: Dict[int, str] = field(default_factory=dict)
    cleaned_chunks_dict: Dict[int, str] = field(default_factory=dict)
    qa_loop_limit: int = field(default=1)

@dataclass(kw_only=True)
class PDFToMarkdownInputState:
    extracted_text: str = field(default=None)
    filepath: str = field(default=None)
    qa_loop_limit: int = field(default=1)

@dataclass(kw_only=True)
class PDFToMarkdownOutputState:
    cleaned_text: str = field(default=None)


@dataclass(kw_only=True)
class ChunktoMarkdownState:
    chunks_dict: Dict[int, str] = field(default_factory=dict)
    chunk_number: int = field(default=None)
    chunk_text: str = field(default=None)
    cleaned_chunk_text: str = field(default=None)
    chunk_qa_feedback: str = field(default=None)
    chunk_feedback_application_counter: int = field(default=0)
    cleaned_chunk_dict: Dict[int, str] = field(default_factory=dict)
    qa_loop_limit: int = field(default=1)


@dataclass(kw_only=True)
class ChunktoMarkdownInputState:
    chunk_number: int = field(default=None)
    chunk_text: str = field(default=None)
    qa_loop_limit: int = 1

@dataclass(kw_only=True)
class ChunktoMarkdownOutputState:
    cleaned_chunk_dict: Dict[int, str] = field(default_factory=dict)
