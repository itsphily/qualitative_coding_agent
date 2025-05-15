from typing import List, Annotated, cast,Callable, List, Any
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, ToolException
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command
from coding_state import Evidence, FinalInsight, FinalEvidence
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

    # Create tool message
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

    # Create tool message
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

@tool
def log_evidence_relationship(
    insight_label: str,
    evidence_doc_name: str,
    evidence_quote: str,
    evidence_chronology: str,
    agreement_level: str,
    original_reasoning_for_quote: str,
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    """
    Tool for logging the relationship between evidence and a final insight.
    
    Args:
        insight_label: The insight label from the final insight
        evidence_doc_name: The document name of the evidence
        evidence_quote: The exact quote from the evidence
        evidence_chronology: Timing relative to intervention (before/during/after/unclear)
        agreement_level: One of: 'strongly_agrees', 'agrees', 'disagrees', 'strongly_disagrees'
        original_reasoning_for_quote: The original reasoning provided for the quote
        state: Injected state containing code_description
        tool_call_id: Injected tool call ID
    """
    # Input validation
    if not insight_label or not isinstance(insight_label, str):
        raise ToolException("Insight label must be a non-empty string")
    if not evidence_doc_name or not isinstance(evidence_doc_name, str):
        raise ToolException("Evidence document name must be a non-empty string")
    if not evidence_quote or not isinstance(evidence_quote, str):
        raise ToolException("Evidence quote must be a non-empty string")
    if not evidence_chronology or evidence_chronology not in ["before", "during", "after", "unclear"]:
        raise ToolException("Evidence chronology must be one of: before, during, after, unclear")
    if not agreement_level or agreement_level not in ["strongly_agrees", "agrees", "disagrees", "strongly_disagrees"]:
        raise ToolException("Agreement level must be one of: strongly_agrees, agrees, disagrees, strongly_disagrees")
    if not original_reasoning_for_quote or not isinstance(original_reasoning_for_quote, str):
        raise ToolException("Original reasoning for quote must be a non-empty string")

    # Get the insight info from the state
    code_description = state["code_description"]

    # Create evidence relationship item
    new_evidence = cast(FinalEvidence, {
        "insight_label": insight_label,
        "evidence_doc_name": evidence_doc_name,
        "evidence_quote": evidence_quote,
        "evidence_chronology": evidence_chronology,
        "agreement_level": agreement_level,
        "original_reasoning_for_quote": original_reasoning_for_quote
    })

    # Create tool message
    tool_message = ToolMessage(
        content=f"Successfully logged evidence relationship for insight '{insight_label}': '{evidence_quote[:50]}...' - {agreement_level}",
        tool_call_id=tool_call_id
    )

    # Return Command object with final_evidence_list update
    return Command(
        update={
            "final_evidence_list": [new_evidence],
        }
    )

# Define the evidence extraction tools
QUOTE_REASONING_TOOL: List[Callable[..., Any]] = [log_quote_reasoning]
INSIGHT_TOOL: List[Callable[..., Any]] = [log_insight]
EVIDENCE_RELATIONSHIP_TOOL: List[Callable[..., Any]] = [log_evidence_relationship]