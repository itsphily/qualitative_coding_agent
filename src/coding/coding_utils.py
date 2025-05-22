from __future__ import annotations
import argparse, json, logging, os
from typing import Dict, List, Tuple, Optional, cast, Any
from coding_state import CodingState, CaseInfo
from langchain_core.runnables.graph import MermaidDrawMethod
import pypandoc

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
      Generate multiple markdown reports for a single case in separate files within a case-specific folder.
      
      Args:
          case_id: The identifier for the case (becomes folder name)
          case_info: Data for the case from CodingState.cases_info
          codes: Code descriptions and aspects from CodingState.codes
          output_dir: Base directory to save the reports (coding_output)
      """
      # Create case-specific directory
      case_dir = os.path.join(output_dir, case_id.replace('/', '_').replace(' ', '_'))
      os.makedirs(case_dir, exist_ok=True)
      
      # Generate the three report documents
      _generate_cross_case_analysis_report(case_id, case_info, codes, case_dir)
      _generate_evidence_list_report(case_id, case_info, codes, case_dir)
      _generate_insights_report(case_id, case_info, codes, case_dir)
      
      # Convert markdown files to PDF
      _convert_markdown_to_pdf(case_dir)
      
      logging.info(f"Generated all reports for case {case_id} in directory {case_dir}")


def _generate_cross_case_analysis_report(case_id: str, case_info: Dict[str, Any], codes: Dict[str, List[str]], case_dir: str) -> None:
      """
      Generate the Cross Case Analysis and Synthesis report.
      
      Structure:
      - Header with explanatory text about analysis types
      - For each code: Cross-Case Analysis, Synthesis Result, Revised Synthesis Result
      - Sections separated by horizontal rules
      """
      filepath = os.path.join(case_dir, "Cross Case Analysis and Synthesis.md")
      
      with open(filepath, 'w', encoding='utf-8') as f:
          # Document title
          f.write("# Cross Case Analysis and Synthesis\n\n")
          
          # Explanatory header sections
          f.write("**Cross-Case Analysis:** Independent analysis of the complete set of source texts for a specific case and "
                 "research code. The goal is to identify and describe robust, overarching patterns of evidence "
                 "and phenomena related to the defined research code, focusing specifically on how these patterns "
                 "manifest for **each of its defined aspects**. The analysis of the texts is done through the lens "
                 "of several synthesis dimensions (e.g., consistency, absence, evolution) for each aspect.\n\n")
          
          f.write("**Synthesis Result:** Thematic analysis and critical assessment of evidence collected by the LLM. "
                 "The goal is to identify dominant content themes, note relevant dimensional characteristics, "
                 "flag any direct contradictions or strong singular claims present in the data, and select "
                 "representative quotes.\n\n")
          
          f.write("**Revised Synthesis Result:** The synthesis results was compiled only using the quote/reasoning pairs that "
                 "were extracted. This step uses the synthesis results and all the texts from the case to "
                 "validate the findings in the synthesis.\n\n")
          
          f.write("---\n\n")
          
          # Process each code
          for code_description, aspects in codes.items():
              f.write(f"## {code_description}\n\n")
              
              # Cross-case analysis section
              f.write("### Cross-Case Analysis\n\n")
              cross_case_analysis = case_info.get("cross_case_analysis_results", {}).get(code_description, "")
              if cross_case_analysis:
                  f.write(f"{cross_case_analysis}\n\n")
              else:
                  f.write("*No cross-case analysis available for this code.*\n\n")
              
              f.write("---\n\n")
              
              # Synthesis result section
              f.write("### Synthesis Result\n\n")
              synthesis_result = case_info.get("synthesis_results", {}).get(code_description, "")
              if synthesis_result:
                  f.write(f"{synthesis_result}\n\n")
              else:
                  f.write("*No synthesis results available for this code.*\n\n")
              
              f.write("---\n\n")
              
              # Revised synthesis result section
              f.write("### Revised Synthesis Result\n\n")
              revised_synthesis = case_info.get("revised_synthesis_results", {}).get(code_description, "")
              if revised_synthesis:
                  f.write(f"{revised_synthesis}\n\n")
              else:
                  f.write("*No revised synthesis results available for this code.*\n\n")
              
              f.write("---\n\n")


def _generate_evidence_list_report(case_id: str, case_info: Dict[str, Any], codes: Dict[str, List[str]], case_dir: str) -> None:
      """
      Generate the Unfiltered Evidence List report.
      
      Structure:
      - Header explaining what this evidence represents
      - For each code: List all evidence with Quote, Doc Name, Chronology, Reasoning, Aspect
      """
      filepath = os.path.join(case_dir, "Unfiltered Evidence List.md")
      
      with open(filepath, 'w', encoding='utf-8') as f:
          # Document title and description
          f.write("# Unfiltered Evidence List\n\n")
          f.write("This is all the evidence that was collected by the LLM initially. It is an unfiltered list that contains all the potential evidence.\n\n")
          f.write("---\n\n")
          
          # Get all evidence from case_info
          evidence_list = case_info.get("evidence_list", [])
          
          # Group evidence by code_description
          evidence_by_code = {}
          for evidence in evidence_list:
              code_desc = evidence.get("code_description", "Unknown Code")
              if code_desc not in evidence_by_code:
                  evidence_by_code[code_desc] = []
              evidence_by_code[code_desc].append(evidence)
          
          # Process each code
          for code_description in codes.keys():
              f.write(f"## {code_description}\n\n")
              
              code_evidence = evidence_by_code.get(code_description, [])
              if code_evidence:
                  for i, evidence in enumerate(code_evidence, 1):
                      f.write(f"### Evidence #{i}\n\n")
                      
                      # Quote
                      quote = evidence.get("quote", "No quote available")
                      f.write(f"**Quote:** {quote}\n\n")
                      
                      # Doc Name (extract filename only)
                      doc_name = evidence.get("doc_name", "Unknown document")
                      doc_name_short = os.path.basename(doc_name) if doc_name else "Unknown document"
                      f.write(f"**Doc Name:** {doc_name_short}\n\n")
                      
                      # Chronology
                      chronology = evidence.get("chronology", "unclear")
                      f.write(f"**Chronology:** {chronology}\n\n")
                      
                      # Reasoning
                      reasoning = evidence.get("reasoning", "No reasoning provided")
                      f.write(f"**Reasoning:** {reasoning}\n\n")
                      
                      # Aspect (as bulleted list)
                      aspects = evidence.get("aspect", [])
                      f.write("**Aspect:**\n")
                      if aspects:
                          for aspect in aspects:
                              f.write(f"- {aspect}\n")
                      else:
                          f.write("- No aspects specified\n")
                      f.write("\n")
                      
                      f.write("---\n\n")
              else:
                  f.write("*No evidence available for this code.*\n\n")
                  f.write("---\n\n")


def _generate_insights_report(case_id: str, case_info: Dict[str, Any], codes: Dict[str, List[str]], case_dir: str) -> None:
      """
      Generate the Final Insights and Evidence report.
      
      Structure:
      - For each insight: Insight label as title, explanation, then related evidence list
      - Evidence includes: Quote, Chronology, Doc Name, Original Reasoning
      """
      filepath = os.path.join(case_dir, "Final Insights and Evidence.md")
      
      with open(filepath, 'w', encoding='utf-8') as f:
          f.write("# Final Insights and Evidence\n\n")
          f.write("---\n\n")
          
          # Get all insights from case_info
          insights_list = case_info.get("final_insights_list", [])
          
          if insights_list:
              for insight in insights_list:
                  insight_label = insight.get("insight_label", "Unnamed Insight")
                  insight_explanation = insight.get("insight_explanation", "No explanation provided")
                  
                  # Use insight label as main heading
                  f.write(f"## {insight_label}\n\n")
                  
                  # Write insight explanation
                  f.write(f"**Insight Explanation:** {insight_explanation}\n\n")
                  
                  # Process related evidence
                  f.write("### Related Evidence\n\n")
                  evidence_list = insight.get("final_evidence_list", [])
                  
                  if evidence_list:
                      for i, evidence in enumerate(evidence_list, 1):
                          f.write(f"#### Evidence #{i}\n\n")
                          
                          # Evidence Quote
                          evidence_quote = evidence.get("evidence_quote", "No quote available")
                          f.write(f"**Evidence Quote:** {evidence_quote}\n\n")
                          
                          # Evidence Chronology
                          evidence_chronology = evidence.get("evidence_chronology", "unclear")
                          f.write(f"**Evidence Chronology:** {evidence_chronology}\n\n")
                          
                          # Doc Name (extract filename only)
                          doc_name = evidence.get("evidence_doc_name", "Unknown document")
                          doc_name_short = os.path.basename(doc_name) if doc_name else "Unknown document"
                          f.write(f"**Doc Name:** {doc_name_short}\n\n")
                          
                          # Original Reasoning
                          reasoning = evidence.get("original_reasoning_for_quote", "No reasoning provided")
                          f.write(f"**Original Reasoning for Quote:** {reasoning}\n\n")
                          
                          f.write("---\n\n")
                  else:
                      f.write("*No evidence available for this insight.*\n\n")
                      f.write("---\n\n")
          else:
              f.write("*No final insights available for this case.*\n\n")


def _convert_markdown_to_pdf(case_dir: str) -> None:
      """
      Convert all markdown files in a case directory to PDF format.
      Keeps the original markdown files and creates PDFs alongside them.
      
      Args:
          case_dir: Directory containing the markdown files to convert
      """
      # Define the expected markdown files
      markdown_files = [
          "Cross Case Analysis and Synthesis.md",
          "Unfiltered Evidence List.md", 
          "Final Insights and Evidence.md"
      ]
      
      for md_file in markdown_files:
          md_path = os.path.join(case_dir, md_file)
          
          # Check if the markdown file exists
          if os.path.exists(md_path):
              try:
                  # Create PDF filename by replacing .md with .pdf
                  pdf_file = md_file.replace('.md', '.pdf')
                  pdf_path = os.path.join(case_dir, pdf_file)
                  
                  # Convert markdown to PDF using pypandoc
                  pypandoc.convert_file(
                      md_path,
                      'pdf',
                      outputfile=pdf_path,
                      extra_args=['--pdf-engine=pdflatex']
                  )
                  
                  logging.info(f"Successfully converted {md_file} to PDF")
                  
              except Exception as e:
                  logging.error(f"Failed to convert {md_file} to PDF: {e}")
                  # Continue with other files even if one fails
                  continue
          else:
              logging.warning(f"Markdown file not found: {md_path}")
      
      logging.info(f"PDF conversion completed for directory: {case_dir}")