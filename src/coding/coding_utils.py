from __future__ import annotations
import argparse, json, logging
from typing import Dict, List, Tuple, Optional, cast
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