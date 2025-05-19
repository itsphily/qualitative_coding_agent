
Before implementing the new nodes you must read this documentation:
Documentation to Read: LangGraph Send: https://langchain-ai.github.io/langgraph/concepts/low_level/?h=send#send
https://langchain-ai.github.io/langgraph/how-tos/tool-calling/
https://langchain-ai.github.io/langgraph/reference/agents/?h=injectedstate#langgraph.prebuilt.tool_node.InjectedState
https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/?h=tool+state+update#2-update-the-state-inside-the-tool

# New Node Implementation Plan: Find and Integrate Evidence for Final Insights
The goal is to add a new capability to our LangGraph application. After final insights are generated for a case, we need to find and associate specific pieces of supporting evidence from the existing evidence_list (within CaseProcessingState) to each FinalInsight object. This new evidence should be stored in the final_evidence_list attribute of each respective FinalInsight object within the CaseProcessingState.final_insights_list.

Overall Workflow for the New Nodes:

1. Dispatch: A new conditional edge function (continue_to_find_evidence_for_insights) will iterate through each FinalInsight in CaseProcessingState.final_insights_list. For each insight, it will Send the insight and the full evidence corpus (CaseProcessingState.evidence_list) to a worker node.
2. Process: The worker node (find_relevant_evidence_node) will use an LLM which is bound to the log_evidence_relationship tool (you will also implement this tool) to identify relevant evidence from the corpus for the given insight.
3. Collect & Return: The worker node will return the original FinalInsight object, but with its final_evidence_list attribute populated with the evidence found by the tool (the tool will directly update the FinalInsight object's final_evidence_list attribute).
4. Aggregate & Update: An aggregation node will collect all these updated FinalInsight objects. A crucial modification to the reducer for CaseProcessingState.final_insights_list will ensure these updates are correctly merged. 

Here are the detailed steps for the implementation plan:

1. Define State for Worker Node and Evidence Structure:
- Create a new TypedDict in coding_state.py for the input to the worker node. Name it FindEvidenceInputState:
class FindEvidenceInputState(TypedDict):
    current_final_insight: FinalInsight  # The specific insight being processed
    full_evidence_list: List[Evidence]   # The complete evidence_list from CaseProcessingState
    # The processed_evidence_for_insight will be populated by the tool within the worker node
    processed_evidence_for_insight: Annotated[List[FinalEvidence], append_evidence]

Note: processed_evidence_for_insight is added here to allow the tool to update this specific list within the worker's state. The append_evidence reducer for FinalEvidence will need to be robust or a new simple append reducer might be defined if append_evidence has complex logic not desired here.

- Ensure the FinalEvidence TypedDict in coding_state.py is suitable:
class FinalEvidence(TypedDict):
    insight_label: str      # Label of the insight this evidence supports
    evidence_doc_name: str  # From the Evidence object
    evidence_quote: str     # From the Evidence object
    evidence_chronology: str# From the Evidence object
    agreement_level: str    # e.g., 'strongly_agrees', 'agrees'
    original_reasoning_for_quote: str # From the Evidence object

2. Implement continue_to_find_evidence_for_insights (Conditional Edge Function):

- This function will be added to coding_exec.py.
- It is triggered after the aggregation_final_insights_node in the case_processing_subgraph.
- Inputs: Current CaseProcessingState.
- Logic:
-> Retrieve final_insights_list and evidence_list from the state.
-> If final_insights_list is empty, return END or an appropriate next step.
-> Iterate through each insight_object in state.final_insights_list.
-> For each insight_object, create an instance of FindEvidenceInputState:
payload = FindEvidenceInputState(
    current_final_insight=insight_object,
    full_evidence_list=state.evidence_list,
    processed_evidence_for_insight=[] # Initialize as empty
)

3. Implement find_relevant_evidence_node (Worker Node):

- This node will be added to coding_exec.py.
- Inputs: FindEvidenceInputState (as state for this node).
- Logic:
-> Extract current_final_insight and full_evidence_list from the input state.
-> Format full_evidence_list into the JSON string structure specified in the find_evidence_prompt (a dictionary where keys are indices "0", "1", etc., and values are the evidence details: chronology, Doc Name, Quote, Reasoning,...).
-> Prepare the prompt using find_evidence_prompt from coding_prompt.py.
The system message is find_evidence_prompt.
The human message should be: "Here is the final insight: {current_final_insight.insight_explanation} (Label: {current_final_insight.insight_label}). You must find all related evidence in this corpus of evidence <corpus_of_evidence> {formatted_evidence_corpus} </corpus_of_evidence>. For each piece of evidence you find that has a discernible relationship (supporting or contradicting) to this Final Insight, you MUST call the 'log_evidence_relationship' tool."
-> Invoke the LLM (e.g., llm_long_context_high_processing or a new one configured for tool use) with this prompt. The LLM should be bound with the log_evidence_relationship tool.
-> The LLM will make calls to log_evidence_relationship. These tool calls will update the state.processed_evidence_for_insight list within this worker node instance due to the Command returned by the tool (see tool implementation below).
-> After the LLM invocation and tool calls complete, the state.processed_evidence_for_insight list will contain all FinalEvidence objects found for the current_final_insight.
-> Return Value: The node must construct and return an updated FinalInsight object. This is achieved by taking a copy of state.current_final_insight and setting its final_evidence_list attribute to the contents of state.processed_evidence_for_insight.
updated_insight = state.current_final_insight.copy() # Shallow copy
updated_insight["final_evidence_list"] = state.processed_evidence_for_insight
return {"final_insights_list": [updated_insight]} # This specific structure is important for the reducer
Self-correction: Returning {"final_insights_list": [updated_insight]} assumes the reducer for final_insights_list at the CaseProcessingState level is robust enough. The map-reduce documentation shows workers returning values that are then collected. A cleaner return for the worker might be just the updated_insight object itself. The aggregation node will collect these into a list. Revised Worker Return:
updated_insight = state.current_final_insight.copy()
# Ensure final_evidence_list exists and append to it.
# If current_final_insight.final_evidence_list could already have items from a previous (different) step,
# you might want to append rather than overwrite.
# For this specific task, we are populating it fresh based on the find_evidence_prompt.
updated_insight["final_evidence_list"] = state.processed_evidence_for_insight
return updated_insight # The aggregation node will collect these.
4. Implement log_evidence_relationship Tool (in coding_tools.py):

This tool is invoked by the LLM within find_relevant_evidence_node.
Tool Name in Prompt: The find_evidence_prompt refers to this tool as log_evidence_relationship.
Pydantic Model for Arguments (as per find_evidence_prompt):
# (inside coding_tools.py)
# class LogEvidenceRelationshipArgs(BaseModel):
#     insight_label: str # Provided by LLM, should match the current insight
#     evidence_doc_name: str
#     evidence_quote: str
#     evidence_chronology: str
#     agreement_level: str # 'strongly_agrees' | 'agrees' | 'disagrees' | 'strongly_disagrees'
#     original_reasoning_for_quote: str

Tool Function:
from langgraph.prebuilt import InjectedState # If needed for insight_label

@tool
def log_evidence_relationship(
    # insight_label: str, # This comes from LLM, ensure it's used or verified
    evidence_doc_name: str,
    evidence_quote: str,
    evidence_chronology: str,
    agreement_level: str,
    original_reasoning_for_quote: str,
    state: Annotated[FindEvidenceInputState, InjectedState], # To get current_final_insight.insight_label
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Logs a piece of evidence found to be related to a specific final insight."""
    # Validation for agreement_level, etc. can be added here.

    # Get the insight_label from the current_final_insight in the worker's state
    current_insight_label = state.current_final_insight["insight_label"]

    final_evidence_item = FinalEvidence(
        insight_label=current_insight_label, # Use label from the specific insight being processed
        evidence_doc_name=evidence_doc_name,
        evidence_quote=evidence_quote,
        evidence_chronology=evidence_chronology,
        agreement_level=agreement_level,
        original_reasoning_for_quote=original_reasoning_for_quote,
    )
    # This command will append to the 'processed_evidence_for_insight'
    # list within the FindEvidenceInputState of the worker node.
    return Command(update={"processed_evidence_for_insight": [final_evidence_item]})

    Add this new tool to a list like EVIDENCE_RELATIONSHIP_TOOL = [log_evidence_relationship] and bind it to the LLM used in find_relevant_evidence_node.

5. Implement Aggregation and Reducer Logic (CRITICAL for avoiding lost evidence):

Add a new aggregation node in coding_exec.py to the case_processing_subgraph. Let's call it aggregate_processed_insights_node. This node will simply collect the outputs from all find_relevant_evidence_node branches. LangGraph handles the collection into a list if the previous node (the worker) returns individual items.
The aggregate_processed_insights_node will simply take the CaseProcessingState and return the state. In that node the map-reduce function of langgraph will be used to aggregate the processed insights. We need to make sure to modify the append_evidence Reducer in coding_state.py: The current append_evidence reducer, when used for CaseProcessingState.final_insights_list, skips FinalInsight objects if their insight_label already exists. This behavior must be changed to update the existing insight.
Current problematic logic for FinalInsight in append_evidence:
# existing_labels = set(fi['insight_label'] for fi in current if isinstance(fi, dict) and 'insight_label' in fi)
# ...
# elif "insight_label" in item: # item is from 'new'
#     if item["insight_label"] not in existing_labels:
#         items_to_add.append(item)
#     else: # SKIPS if label exists
#         logging.info(f"[append_evidence] SKIPPING duplicate insight: {item['insight_label']}")

Required Change to append_evidence (or create a new dedicated reducer):
The plan is to modify append_evidence. When an item from new (the list of updated insights from workers) is a FinalInsight:

Create a dictionary from the current list for easy lookup: current_map = {insight['insight_label']: insight for insight in current if isinstance(insight, dict) and 'insight_label' in insight}.
For each updated_insight_from_worker in new_items_that_are_insights:
If its insight_label is a key in current_map, then current_map[updated_insight_from_worker['insight_label']] = updated_insight_from_worker. This replaces the old insight with the new one (which contains the final_evidence_list).
Else, add it: current_map[updated_insight_from_worker['insight_label']] = updated_insight_from_worker.
The final list of insights for the state will be list(current_map.values()), combined with other non-insight items if append_evidence handles mixed types. The reducer should be careful to only apply this logic to FinalInsight objects.
Detailed instructions for modifying append_evidence in coding_state.py:

# Inside append_evidence function in coding_state.py

# ... (existing setup) ...

# Separate FinalInsight items from 'new' for special handling
new_final_insights = [item for item in new if isinstance(item, dict) and "insight_label" in item]
other_new_items = [item for item in new if not (isinstance(item, dict) and "insight_label" in item)]

# Handle FinalInsight updates
current_final_insights_map = {
    fi['insight_label']: fi for fi in current if isinstance(fi, dict) and 'insight_label' in fi
}

for insight_update in new_final_insights:
    label = insight_update['insight_label']
    # If the insight from worker has a populated final_evidence_list, it means it was processed.
    # Replace the existing insight in the map with this updated one.
    current_final_insights_map[label] = insight_update
    logging.info(f"[append_evidence] Updating/Adding insight: {label} with new evidence.")

# Reconstruct the 'current' list including updated insights and other original items
processed_current = [
    item for item in current if not (isinstance(item, dict) and 'insight_label' in item)
] # All non-FinalInsight items from current
processed_current.extend(list(current_final_insights_map.values())) # All updated/new FinalInsights

# Now, handle 'other_new_items' (non-FinalInsight items from 'new')
# using the existing logic of append_evidence (e.g., for Evidence items)
# This part needs to be carefully integrated with the existing append_evidence structure.
# For simplicity, the example below assumes 'current' and 'new' in append_evidence
# are *specifically* for final_insights_list when this logic path is hit.
# If append_evidence is generic, this specific logic for FinalInsight must be conditional.

# Assuming 'current' and 'new' are purely lists of FinalInsights for this part of the reducer:
# The return would be list(current_final_insights_map.values()) if 'other_new_items' is empty.

# A more robust way is to modify the section that handles 'FinalInsight' items:
# Rebuild 'items_to_add' and 'existing_labels' carefully.
# The core idea: if an insight_label from 'new' matches one in 'current',
# the 'new' item (which is the updated FinalInsight object from the worker) should replace the 'current' one.
# It should not be merely skipped or appended if unique.

Given the complexity, the most straightforward instruction to the LLM for the plan is:
"The append_evidence reducer in coding_state.py must be modified. When it is reducing final_insights_list and an incoming FinalInsight object from a worker node (present in new) has an insight_label that matches an existing FinalInsight in the current list, the incoming object (which contains the updated final_evidence_list) must replace the existing object in the list. If the insight_label is new, it should be appended."


6. Update Graph Structure in case_processing_subgraph (coding_exec.py):
Add the new nodes: find_relevant_evidence_node and aggregate_processed_insights_node.
Define edges:
case_processing_graph.add_conditional_edges("aggregation_final_insights_node", continue_to_find_evidence_for_insights, ["find_relevant_evidence_node", END]) (or similar, END if no insights).
case_processing_graph.add_edge("find_relevant_evidence_node", "aggregate_processed_insights_node")
case_processing_graph.add_edge("aggregate_processed_insights_node", END) (This END refers to the end of the case processing subgraph, ensuring the CaseProcessingState is updated).