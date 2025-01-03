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


def save_cleaned_text(
    extracted_text: str,
    cleaned_text: str,
    title: str,
    include_feedback: bool = True,
    qa_feedback: str = None
):
    """Save cleaned text to a markdown file.
    
    Args:
        extracted_text (str): The original text before cleaning
        cleaned_text (str): The cleaned text to save
        title (str): Name of the cleaning step (e.g., 'text_cleaner', 'boilerplate_remover')
        include_feedback (bool): Whether to include the QA feedback prompt in the output
        
    Returns:
        str: The full text content that was written to the file
    """
    # Create outputs directory if it doesn't exist
    output_dir = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp and step name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cleaned_text_{title}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Prepare the full text content
    full_text = ""
    
    if include_feedback:
        full_text += qa_feedback_prompt
    
    full_text += (
        f"<Original Text>\n"
        f"{extracted_text}\n"
        f"</Original Text>\n\n"
        f"<Restructured Output>\n"
        f"{cleaned_text}\n"
        f"</Restructured Output>\n\n"
    )
    
    if qa_feedback is not None:
        full_text += f"<QA Feedback>\n{qa_feedback}\n</QA Feedback>\n\n"
    
    # Write the content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"\nCleaned text saved to: {filepath}")
    
    return full_text
