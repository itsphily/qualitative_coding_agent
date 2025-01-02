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
        tuple[str, str]: Tuple containing (filepath, full_text)
    """
    # Create outputs directory if it doesn't exist
    output_dir = "cleaned_text_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp and step name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cleaned_text_{title}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Prepare the full text content
    full_text = (
        f"{qa_feedback_prompt}\n\n"
        f"<Original Text>\n"
        f"{extracted_text}\n"
        f"</Original Text>\n\n"
        f"<Restructured Output>\n"
        f"{cleaned_text}\n"
        f"</Restructured Output>\n\n"
    )
    
    # Write the content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"\nCleaned text saved to: {filepath}")
    
    return full_text