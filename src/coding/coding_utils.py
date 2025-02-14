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
    Generate a dictionary of Markdown strings, one for each code.
    Each markdown string has three sections:
    1) Document Evidence: Grouped by charity_id (##), and doc_name - document_importance (###) with the list of quote–reasoning pairs.
       Only includes documents that have quote-reasoning pairs.
    2) Important Documents: Under a fixed title "Important documents" with document_importance (##) and list of document names.
    3) Unprocessed Documents: Under a fixed title "Unprocessed documents" with a list of document names.
    
    Returns:
        dict[str, str]: A dictionary where keys are codes and values are markdown formatted strings
    """
    # Group documents by code first
    docs_by_code = {}
    for doc in documents:
        if not doc["quote"] or not doc["reasoning"]:
            continue
        code = doc["code"]
        if code not in docs_by_code:
            docs_by_code[code] = []
        docs_by_code[code].append(doc)

    markdown_output = {}
    
    for code, code_documents in docs_by_code.items():
        markdown_sections = []
        
        # Section 1: Document Evidence
        evidence_lines = []
        # Group by charity_id -> doc_name with document importance
        grouped = {}
        for doc in code_documents:
            charity_id = doc["charity_id"]
            if charity_id not in grouped:
                grouped[charity_id] = {}
            # Each doc_name with its document importance and a list of quote-reasoning pairs
            doc_key = f'{doc["doc_name"]} - {doc["document_importance"]}'
            if doc_key not in grouped[charity_id]:
                grouped[charity_id][doc_key] = []
            grouped[charity_id][doc_key].append((doc["quote"], doc["reasoning"]))

        # Generate evidence section
        for charity_id, docs in grouped.items():
            evidence_lines.append(f"## {charity_id}")
            for doc_key, pairs in docs.items():
                evidence_lines.append(f"### {doc_key}")
                for quote, reasoning in pairs:
                    # Format multi-line quote by indenting subsequent lines
                    quote_lines = quote.split('\n')
                    formatted_quote = quote_lines[0]
                    if len(quote_lines) > 1:
                        for line in quote_lines[1:]:
                            formatted_quote += f"\n  {line}"
                    
                    evidence_lines.append(f"- **Quote:** {formatted_quote}")
                    evidence_lines.append("")  # Add blank line between quote and reasoning
                    evidence_lines.append(f"  **Reasoning:** {reasoning}")
                    evidence_lines.append("")  # Add blank line after each quote-reasoning pair
                evidence_lines.append("")  # Add extra blank line between documents
            evidence_lines.append("")  # Blank line after each charity group

        if evidence_lines:
            markdown_sections.append("\n".join(evidence_lines))

        # Section 2: Important Documents for this code
        important_docs = {}
        for doc in code_documents:
            imp = doc["document_importance"]
            if imp not in important_docs:
                important_docs[imp] = set()
            important_docs[imp].add(doc["doc_name"])
        
        # Order the importance categories as specified
        importance_order = ["important to read", "worth reading", "not worth reading"]
        important_lines = ["# Important documents"]
        for imp in importance_order:
            if imp in important_docs:
                important_lines.append(f"## {imp}")
                for doc_name in sorted(important_docs[imp]):
                    important_lines.append(f"- {doc_name}")
        markdown_sections.append("\n".join(important_lines))

        # Section 3: Unprocessed Documents
        unprocessed_lines = ["# Unprocessed documents"]
        for doc_name in unprocessed_documents:
            unprocessed_lines.append(f"- {doc_name}")
        markdown_sections.append("\n".join(unprocessed_lines))

        # Join sections with a separator line and store in output dict
        markdown_output[code] = ("\n\n----\n\n").join(markdown_sections)

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
def synthesis_output_to_markdown(state: CodingAgentState):
    """
    Aggregate synthesis_layer_2 outputs and structure as markdown.
    Calls generate_synthesis_markdown for per charity and per code outputs.
    """
    per_charity = state.get("synthesis_layer_2_per_charity", {})
    per_code = state.get("synthesis_layer_2_per_code", {})
    synthesis_md_charity = ""
    for charity, text in per_charity.items():
        synthesis_md_charity += f"## Charity: {charity}\n{text}\n\n"
    synthesis_md_code = ""
    for code, text in per_code.items():
        synthesis_md_code += f"## Code: {code}\n{text}\n\n"
    output_charity = generate_synthesis_markdown(synthesis_md_charity, 'synthesis_output_per_charity', 'coding_output')
    output_code = generate_synthesis_markdown(synthesis_md_code, 'synthesis_output_per_code', 'coding_output')
    return {"synthesis_output_per_charity": output_charity,
            "synthesis_output_per_code": output_code}
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
