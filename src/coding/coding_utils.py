import os
from collections import defaultdict
from langchain_core.runnables.graph import MermaidDrawMethod

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
    Generate a Markdown string with three sections:
    1) Document Evidence: Grouped by code (#), charity_id (##), and doc_name - document_importance (###) with the list of quote–reasoning pairs.
       Only includes documents that have quote-reasoning pairs.
    2) Important Documents: Under a fixed title "Important documents" with document_importance (##) and list of document names.
    3) Unprocessed Documents: Under a fixed title "Unprocessed documents" with a list of document names.
    """
    markdown_sections = []

    # Section 1: Document Evidence
    evidence_lines = []
    # Group by code -> charity_id -> doc_name with document importance (displayed next to doc_name)
    grouped = {}
    for doc in documents:
        # Skip documents without quote-reasoning pairs
        if not doc["quote"] or not doc["reasoning"]:
            continue
            
        code = doc["code"]
        charity_id = doc["charity_id"]
        key = (code, charity_id)
        if key not in grouped:
            grouped[key] = {}
        # Each doc_name with its document importance and a list of quote-reasoning pairs
        doc_key = f'{doc["doc_name"]} - {doc["document_importance"]}'
        if doc_key not in grouped[key]:
            grouped[key][doc_key] = []
        grouped[key][doc_key].append((doc["quote"], doc["reasoning"]))

    # Only add section 1 if there are documents with quote-reasoning pairs
    if grouped:
        for (code, charity_id), docs in grouped.items():
            evidence_lines.append(f"# {code}")
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

        markdown_sections.append("\n".join(evidence_lines))

    # Section 2: Important Documents
    important_docs = {}
    for doc in documents:
        imp = doc["document_importance"]
        if imp not in important_docs:
            important_docs[imp] = set()
        important_docs[imp].add(doc["doc_name"])
    # Order the importance categories as specified.
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

    # Join sections with a separator line.
    markdown_doc = ("\n\n----\n\n").join(markdown_sections)
    return markdown_doc

def save_final_markdown(filepath: str, cleaned_text: str):
    """
    This function takes the cleaned_text and the filepath as arguments and saves the cleaned_text to a .md file.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
