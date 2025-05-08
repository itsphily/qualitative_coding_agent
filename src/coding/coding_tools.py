from typing import List, Annotated, cast,Callable, List, Any
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, ToolException
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command
from coding_state import Evidence
from langgraph.config import get_config


# --- logging tool ---
@tool
def log_quote_reasoning(
    quote: str,
    reasoning: str,
    aspect: List[str],
    chronology: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """
    Tool for logging evidence found during text analysis.
    
    Args:
        quote: The text passage extracted as evidence
        reasoning: Explanation of why this quote is evidence
        aspect: List of aspects this quote relates to
        chronology: Timing relative to intervention (before/during/after/unclear)
        tool_call_id: Injected tool call ID
        code_description: The code this evidence relates to
        doc_name: Source document name
    """
    # Input validation
    if not quote or not isinstance(quote, str):
        raise ToolException("Quote must be a non-empty string")
    if not reasoning or not isinstance(reasoning, str):
        raise ToolException("Reasoning must be a non-empty string")
    if not aspect or not isinstance(aspect, list):
        raise ToolException("Aspect must be a non-empty list")
    if not chronology or chronology not in ["before", "during", "after", "unclear"]:
        raise ToolException("Chronology must be one of: before, during, after, unclear")
    
    # Get code_description and doc_name from config if not provided
    cfg = get_config().get("configurable", {})
    code_description = cfg.get("code_description", "unknown_code")
    doc_name = cfg.get("doc_name", "unknown_doc")
    
    # Create evidence item
    new_evidence = cast(Evidence, {
        "quote": quote,
        "reasoning": reasoning,
        "aspect": aspect,
        "chronology": chronology,
        "code_description": code_description,
        "doc_name": doc_name
    })
    
    # Create tool message - REQUIRED for Command objects from tools
    tool_message = ToolMessage(
        content=f"Successfully logged evidence from document '{doc_name}': '{quote[:50]}...'",
        tool_call_id=tool_call_id
    )
    
    # Return Command object with both evidence_list and messages updates
    return Command(
        update={
            "evidence_list": [new_evidence],
            "messages": [tool_message]
        }
    )

# Define the evidence extraction tools
TOOLS: List[Callable[..., Any]] = [log_quote_reasoning]