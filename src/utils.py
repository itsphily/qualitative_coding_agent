from langchain_core.runnables.graph import MermaidDrawMethod
import os
import datetime
from prompt import qa_feedback_prompt

def visualize_graph(graph, name):
    """Visualize the graph"""
    # visualize the graph
    try:
        png_data = graph.get_graph(xray = 1).draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        with open(f'{name}.png', 'wb') as f:
            f.write(png_data)
        print(f"Graph visualization saved to '{name}.png'")
    except Exception as e:
        print(f"Error saving graph visualization: {e}")


def save_cleaned_text(extracted_text: str, cleaned_text: str, title: str):
    """Save cleaned text to a markdown file.
    
    Args:
        text (str): The cleaned text to save
        step_name (str): Name of the cleaning step (e.g., 'text_cleaner', 'boilerplate_remover')
        
    Returns:
        str: Path to the saved file
    """
    # Create outputs directory if it doesn't exist
    output_dir = "cleaned_text_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp and step name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cleaned_text_{title}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Write the content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{qa_feedback_prompt}\n\n")
        f.write("<original text extracted from a PDF>")
        f.write(f"{extracted_text}\n")
        f.write("</original text extracted from a PDF>\n\n")
        f.write("<cleaned Markdown output>")
        f.write(f"{cleaned_text}\n")
        f.write("</cleaned Markdown output>\n\n")

    
    print(f"\nCleaned text saved to: {filepath}")
    return filepath