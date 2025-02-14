import os
from collections import defaultdict
from langchain_core.runnables.graph import MermaidDrawMethod
import json

def path_to_text(path):
    """
    This function takes in a path and returns the content of the .md file.
    """
    with open(path, 'r', encoding='utf-8') as file:
        doc_text = file.read()
    return doc_text

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

def path_to_doc_name(path: str) -> str:
    """
    This function takes the path to a document and returns the document name.
    """
    return os.path.basename(path)

def merge_lists(list_a: list, list_b: list) -> list:
    """
    Merge list_b into list_a.
    Returns a new list, leaving the original list unchanged.
    """
    merged = list_a.copy()
    merged.extend(list_b)
    return merged

def generate_markdown(documents, unprocessed_documents):
    """
    Generate a dictionary of Markdown strings, one for each charity.
    For each charity (identified by charity_id), the markdown is structured as follows:
      - Charity Header: "# Charity Id: <charity_id>"
      - Document Importance Section: Under "Document Importance", list each doc_name grouped by:
           "Important to read", "Worth reading", and "Not worth reading".
      - Code-Specific Sections: For each code associated with that charity:
           "## Code: <code>"
             "### Doc Name: <doc_name>"
               - **Quote:** <quote>
               - **Reasoning:** <reasoning>
      - Unprocessed Documents Section: List any unprocessed document names.
    Returns a dictionary where keys are charity_id and values are the corresponding markdown strings.
    """
    markdown_output = {}
    # Group input documents by charity_id.
    charities = {}
    for doc in documents:
        charity = doc["charity_id"]
        charities.setdefault(charity, []).append(doc)
    
    for charity_id, docs in charities.items():
        sections = []
        # Charity Header
        sections.append(f"# Charity Id: {charity_id}")
        sections.append("")

        # Document Importance Section: group docs by importance.
        imp_groups = {"important to read": set(), "worth reading": set(), "not worth reading": set()}
        for doc in docs:
            imp = doc["document_importance"]
            imp_groups[imp].add(doc["doc_name"])
        imp_lines = ["# Document Importance"]
        for imp in ["important to read", "worth reading", "not worth reading"]:
            imp_lines.append(f"### {imp.capitalize()}")
            for doc_name in sorted(imp_groups[imp]):
                imp_lines.append(f"- {doc_name}")
        sections.append("\n".join(imp_lines))

        # Code-Specific Sections: group docs by code, then by doc_name.
        code_groups = {}
        for doc in docs:
            code = doc["code"]
            code_groups.setdefault(code, {}).setdefault(doc["doc_name"], []).append((doc["quote"], doc["reasoning"]))
        for code, docs_by_name in code_groups.items():
            sections.append("")
            sections.append(f"## Code: {code}")
            for doc_name, pairs in docs_by_name.items():
                sections.append(f"### Doc Name: {doc_name}")
                for quote, reasoning in pairs:
                    sections.append(f"- **Quote:** {quote}")
                    sections.append(f"  **Reasoning:** {reasoning}")
        # Unprocessed Documents Section
        if unprocessed_documents:
            sections.append("")
            sections.append("# Unprocessed Documents")
            for d in unprocessed_documents:
                sections.append(f"- {d}")

        markdown_output[charity_id] = "\n\n".join(sections)
    return markdown_output

def save_final_markdown(filepath: str, cleaned_text: str):
    """
    This function takes the cleaned_text and the filepath as arguments and saves the cleaned_text to a .md file.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)


def format_results_to_json(prompt_per_code_results: list) -> str:
    """
    Convert prompt_per_code_results into a formatted JSON string.
    
    Args:
        prompt_per_code_results (list): List of dictionaries containing coding results
        
    Returns:
        str: Formatted JSON string with proper indentation
    """
    formatted_results = []
    for item in prompt_per_code_results:
        formatted_item = {
            "charity_id": item["charity_id"],
            "code": item["code"],
            "doc_name": item["doc_name"],
            "document_importance": item["document_importance"],
            "quote": item["quote"] if item["quote"] else "Empty string",
            "reasoning": item["reasoning"] if item["reasoning"] else "Empty string"
        }
        formatted_results.append(formatted_item)
    
    return json.dumps(formatted_results, indent=2)

def transform_qa_results_to_dict(qa_results_list: list) -> dict:
    """
    Transform a list of QAValuePerCode objects into a dictionary with integer keys.

    Args:
        qa_results_list (list): List of QAValuePerCode objects

    Returns:
        dict: Dictionary where keys are integers and values are dictionaries containing:
            - charity_id (str)
            - code (str)
            - doc_name (str)
            - quote (str)
            - reasoning (str)
            - document_importance (str)
    """
    return {
        i: {
            "charity_id": item.charity_id,
            "code": item.code,
            "doc_name": item.doc_name,
            "quote": item.quote,
            "reasoning": item.reasoning,
            "document_importance": item.document_importance
        }
        for i, item in enumerate(qa_results_list)
    }

def generate_synthesis_markdown(markdown_text, name, output_folder):
    """
    Save markdown_text to a file named f"{name}.md" in output_folder.
    Return the markdown string.
    """
    import os
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    filepath = os.path.join(output_folder, f"{name}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_text)
    return markdown_text
