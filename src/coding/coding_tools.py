from typing import List, Annotated, cast,Callable, List, Any
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, ToolException
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command
from coding_state import Evidence, FinalInsight
from langgraph.prebuilt import InjectedState


# --- logging tool ---
@tool
def log_quote_reasoning(
    quote: str,
    reasoning: str,
    aspect: List[str],
    chronology: str,
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
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
    
    # Get the current state dictionary
    code_description = state["code_description"]
    doc_name = state["file_path"]
    
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
        }
    )

@tool
def log_insight(
    insight_label: str,
    insight_explanation: str,
    supporting_evidence_summary: str,
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    """
    Tool for logging final insights after analyzing synthesis results.
    
    Args:
        insight_label: Short, clear title for the Final Insight
        insight_explanation: Clear and detailed explanation of the insight
        supporting_evidence_summary: Summary of evidence supporting this insight
        state: Injected state containing code_description
        tool_call_id: Injected tool call ID
    """
    # Input validation
    if not insight_label or not isinstance(insight_label, str):
        raise ToolException("Insight label must be a non-empty string")
    if not insight_explanation or not isinstance(insight_explanation, str):
        raise ToolException("Insight explanation must be a non-empty string")
    if not supporting_evidence_summary or not isinstance(supporting_evidence_summary, str):
        raise ToolException("Supporting evidence summary must be a non-empty string")

    # Get the current state dictionary
    code_description = state["code_description"]

    # Create final insight item
    new_final_insight = cast(FinalInsight, {
        "code_description": code_description,
        "insight_label": insight_label,
        "insight_explanation": insight_explanation,
        "supporting_evidence_summary": supporting_evidence_summary
    })

    # Create tool message - REQUIRED for Command objects from tools
    tool_message = ToolMessage(
        content=f"Successfully logged insight '{insight_label}' for code '{code_description[:30]}...'",
        tool_call_id=tool_call_id
    )

    # Return Command object with final_insights_list update
    return Command(
        update={
            "final_insights_list": [new_final_insight],
        }
    )

# Define the evidence extraction tools
QUOTE_REASONING_TOOL: List[Callable[..., Any]] = [log_quote_reasoning]
INSIGHT_TOOL: List[Callable[..., Any]] = [log_insight]