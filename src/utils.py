from langchain_core.runnables.graph import MermaidDrawMethod
import os
import datetime

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


def save_research_results(research_topic: str, summary: str):
    """Save research results to a markdown file.
    
    Args:
        research_topic (str): The topic of the research
        summary (str): The research summary to save
        
    Returns:
        str: Path to the saved file
    """
    # Create outputs directory if it doesn't exist
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp and sanitized topic
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize topic for filename (remove special chars, spaces to underscores)
    safe_topic = "".join(c if c.isalnum() else "_" for c in research_topic).lower()
    filename = f"{safe_topic}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Write the content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Research: {research_topic}\n\n")
        f.write(f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(f"{summary}\n")
    
    print(f"\nResearch results saved to: {filepath}")
    return filepath


def save_cleaned_text(text: str, step_name: str):
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
    filename = f"cleaned_text_{step_name}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Write the content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Cleaned Text - {step_name}\n\n")
        f.write(f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("## Content\n\n")
        f.write(f"{text}\n")
    
    print(f"\nCleaned text saved to: {filepath}")
    return filepath