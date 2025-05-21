from __future__ import annotations
import argparse, json, logging, os
from typing import Dict, List, Tuple, Optional, cast, Any
from coding_state import CodingState, CaseInfo
from langchain_core.runnables.graph import MermaidDrawMethod

def _parse_code_string(raw: str) -> str:
    """
    Normalises an input like 'Name: Definition' or just 'Definition'
    into the key we store in the state.
    """
    name, sep, definition = raw.partition(":")
    if sep:
        name, definition = name.strip(), definition.strip()
        return f"{name}: {definition}" if definition else name
    return raw.strip()

def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for the main execution script."""
    parser = argparse.ArgumentParser(description="Run Multi-Phase Qualitative Analysis Workflow using LangGraph")
    parser.add_argument(
        "--research_question",
        required=True,
        help="Overall research question guiding the analysis."
    )
    parser.add_argument(
        "--code_list",
        required=True,
        nargs='+',
        help="List of code strings, typically 'Name: Definition' or just 'Description'."
    )
    parser.add_argument(
        "--charities",
        required=True,
        type=json.loads,
        help='JSON string representing a list of dictionaries, each with "charity_id", "charity_directory", and optional "charity_overview".'
    )
    return parser.parse_args()


def initialize_state(args: argparse.Namespace) -> CodingState:
    """Creates the initial LangGraph state from CLI arguments."""
    logging.info("‑‑‑ Initialising graph state ‑‑‑")

    # 1. Codes → dict keyed by description
    codes: Dict[str, Optional[List[str]]] = {}
    for raw in args.code_list:
        key = _parse_code_string(raw)
        if key in codes:
            logging.warning("Duplicate code skipped: %s", key)
            continue
        codes[key] = None  # Initialize with None, will be replaced with aspects list
    logging.info("Added %d code entries", len(codes))

    # 2. Charities / cases
    cases: Dict[str, CaseInfo] = {}
    for item in args.charities:
        if not isinstance(item, dict):
            logging.warning("Charity entry is not a dict: %s", item); continue
        cid, directory = item.get("charity_id"), item.get("charity_directory")
        if not (cid and directory):
            logging.warning("Missing id/directory in charity entry: %s", item); continue
        cases[cid] = CaseInfo(
            directory=directory,
            description=item.get("charity_overview"),
            intervention=None,
        )
    logging.info("Added %d case entries", len(cases))

    # 3. Assemble and return CodingState
    state: CodingState = cast(CodingState, {
        "research_question": args.research_question,
        "codes": codes,
        "cases_info": cases,
        "evidence_list": {},  # Initialize with empty dictionary
    })
    logging.info("‑‑‑ Initial state ready ‑‑‑")
    return state


def visualize_graph(graph, name):
    """Visualize the graph."""
    try:
        png_data = graph.get_graph(xray=2).draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        with open(f'{name}.png', 'wb') as f:
            f.write(png_data)
        print(f"Graph visualization saved to '{name}.png'")
    except Exception as e:
        print(f"Error saving graph visualization: {e}")


def generate_report_for_case(case_id: str, case_info: Dict[str, Any], codes: Dict[str, List[str]], output_dir: str) -> None:
      """
      Generate a markdown report for a single case.
      
      Args:
          case_id: The identifier for the case
          case_info: Data for the case from CodingState.cases_info
          codes: Code descriptions and aspects from CodingState.codes
          output_dir: Directory to save the report
      """
      intervention = case_info.get("intervention", "No intervention specified")

      # Create filename from case_id (sanitize if needed)
      filename = f"{case_id.replace('/', '_').replace(' ', '_')}.md"
      filepath = os.path.join(output_dir, filename)

      with open(filepath, 'w', encoding='utf-8') as f:
          # Title and description
          f.write(f"# {case_id}\n\n")
          f.write(f"## Description: {intervention}\n\n")

          # Process each code
          for code_description, aspects in codes.items():
              f.write(f"### Code: {code_description}\n\n")

              # Aspects of the code
              f.write("#### Aspects of the Code\n\n")
              f.write("Aspects represent a breakdown of the code into its distinct key aspects or sub-components. "
                     "These aspects help in finding quote/reasoning pairs in the text. They represent the "
                     "fundamental activities, considerations, or dimensions embedded within the code's definition.\n\n")

              if aspects:
                  for aspect in aspects:
                      f.write(f"- {aspect}\n")
              else:
                  f.write("*No aspects defined for this code.*\n")
              f.write("\n")

              # Cross-case analysis
              f.write("#### Cross-Case Analysis\n\n")
              f.write("Description: Independent analysis of the complete set of source texts for a specific case and "
                     "research code. The goal is to identify and describe robust, overarching patterns of evidence "
                     "and phenomena related to the defined research code, focusing specifically on how these patterns "
                     "manifest for **each of its defined aspects**. The analysis of the texts is done through the lens "
                     "of several synthesis dimensions (e.g., consistency, absence, evolution) for each aspect.\n\n")

              cross_case_analysis = case_info.get("cross_case_analysis_results", {}).get(code_description, "")
              if cross_case_analysis:
                  f.write(f"{cross_case_analysis}\n\n")
              else:
                  f.write("*No cross-case analysis available for this code.*\n\n")

              # Synthesis result
              f.write("#### Synthesis Result\n\n")
              f.write("Description: Thematic analysis and critical assessment of evidence collected by the LLM. "
                     "The goal is to identify dominant content themes, note relevant dimensional characteristics, "
                     "flag any direct contradictions or strong singular claims present in the data, and select "
                     "representative quotes.\n\n")

              synthesis_result = case_info.get("synthesis_results", {}).get(code_description, "")
              if synthesis_result:
                  f.write(f"{synthesis_result}\n\n")
              else:
                  f.write("*No synthesis results available for this code.*\n\n")

              # Revised synthesis result
              f.write("#### Revised Synthesis Results\n\n")
              f.write("Description: The synthesis results was compiled only using the quote/reasoning pairs that "
                     "were extracted. This step uses the synthesis results and all the texts from the case to "
                     "validate the findings in the synthesis.\n\n")

              revised_synthesis = case_info.get("revised_synthesis_results", {}).get(code_description, "")
              if revised_synthesis:
                  f.write(f"{revised_synthesis}\n\n")
              else:
                  f.write("*No revised synthesis results available for this code.*\n\n")

              # Final insights
              f.write("#### Final Insights\n\n")

              # Filter insights related to the current code
              insights = [
                  insight for insight in case_info.get("final_insights_list", [])
                  if insight.get("code_description") == code_description
              ]

              if insights:
                  for i, insight in enumerate(insights):
                      insight_label = insight.get("insight_label", f"Insight #{i+1}")
                      insight_explanation = insight.get("insight_explanation", "No explanation provided")
                      supporting_evidence = insight.get("supporting_evidence_summary", "No supporting evidence summary")

                      f.write(f"##### {insight_label}\n\n")
                      f.write(f"Insight explanation: {insight_explanation}\n\n")
                      f.write(f"Supporting evidence summary: {supporting_evidence}\n\n")

                      f.write("Evidence Collected for this insight:\n\n")

                      # Process evidence for the insight
                      evidence_list = insight.get("final_evidence_list", [])
                      if evidence_list:
                          for j, evidence in enumerate(evidence_list):
                              f.write(f"###### Evidence#{j+1}\n\n")

                              doc_name = evidence.get("evidence_doc_name", "Unknown document")
                              f.write(f"Evidence doc name: {doc_name}\n\n")

                              quote = evidence.get("evidence_quote", "No quote available")
                              f.write(f"Evidence quote: {quote}\n\n")

                              agreement = evidence.get("agreement_level", "Unknown agreement level")
                              f.write(f"Agreement level: {agreement}\n\n")

                              reasoning = evidence.get("original_reasoning_for_quote", "No reasoning provided")
                              f.write(f"Reasoning for extracting quote: {reasoning}\n\n")
                      else:
                          f.write("*No evidence available for this insight.*\n\n")
              else:
                  f.write("*No final insights available for this code.*\n\n")

              # Add separator between codes
              f.write("---\n\n")

      logging.info(f"Generated report for case {case_id} at {filepath}")