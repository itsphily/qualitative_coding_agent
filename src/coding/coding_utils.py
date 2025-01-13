import os
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
        png_data = graph.get_graph(xray=1).draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        with open(f'{name}.png', 'wb') as f:
            f.write(png_data)
        print(f"Graph visualization saved to '{name}.png'")
    except Exception as e:
        print(f"Error saving graph visualization: {e}")

def save_final_markdown(filepath: str, cleaned_text: str):
    """
    This function takes the cleaned_text and the filepath as arguments and saves the cleaned_text to a .md file.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
