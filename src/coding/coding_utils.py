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

def generate_markdown(documents):
    """
    Generate a Markdown string grouped by:
      1) code (top-level #)
      2) charity_id (##)
      3) doc_name (###)
    For each document, include lines for "Quote" and "Reasoning".
    """
    # Group data in a nested structure: code -> charity_id -> doc_name -> list of (quote, reasoning)
    grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for doc in documents:
        code = doc["code"]
        charity_id = doc["charity_id"]
        doc_name = doc["doc_name"]
        quote = doc["quote"]
        reasoning = doc["reasoning"]
        
        grouped_data[code][charity_id][doc_name].append((quote, reasoning))

    # Build the Markdown output
    markdown_lines = []
    for code, charities in grouped_data.items():
        # Top-level heading for code
        markdown_lines.append(f"# {code}\n")
        
        for charity_id, doc_names in charities.items():
            # Heading for charity_id
            markdown_lines.append(f"## {charity_id}\n")
            
            for doc_name, entries in doc_names.items():
                # Sub-heading for doc_name
                markdown_lines.append(f"### {doc_name}\n")
                for (quote, reasoning) in entries:
                    markdown_lines.append(f"**Quote:** {quote}\n")
                    markdown_lines.append(f"**Reasoning:** {reasoning}\n")
                    markdown_lines.append("")  # Blank line for spacing
        
        markdown_lines.append("")  # Blank line after each code
    
    return "\n".join(markdown_lines)

def save_final_markdown(filepath: str, cleaned_text: str):
    """
    This function takes the cleaned_text and the filepath as arguments and saves the cleaned_text to a .md file.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
