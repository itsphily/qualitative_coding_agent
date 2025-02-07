import os
from typing import Dict
from langchain_core.runnables.graph import MermaidDrawMethod

def chunk_file(filepath: str, chunk_size: int = 2000) -> Dict[int, str]:
    """
    Reads a markdown file and divides it into chunks of approximately
    'chunk_size' words, ensuring chunks end at sentence boundaries.
    Returns a dictionary with chunk numbers as keys and chunk texts as values.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
    
    import nltk
    nltk.download('punkt', quiet=True)
    from nltk.tokenize import sent_tokenize

    sentences = sent_tokenize(text)
    chunks = {}
    current_chunk = ''
    current_length = 0
    chunk_number = 1

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= chunk_size:
            current_chunk += ' ' + sentence
            current_length += sentence_length
        else:
            chunks[chunk_number] = current_chunk.strip()
            chunk_number += 1
            current_chunk = sentence
            current_length = sentence_length

    if current_chunk:
        chunks[chunk_number] = current_chunk.strip()

    return chunks

def save_final_markdown(filepath: str, cleaned_text: str):
    """
    Save the cleaned text to the appropriate folder, mirroring the structure
    starting from 'nougat_extracted_text' in the original filepath.
    """
    nougat_path = 'storage/nougat_extracted_text'
    index = filepath.find(nougat_path)
    if index == -1:
        print("Error: 'nougat_extracted_text' not found in filepath.")
        return
    # Get the relative path starting from 'nougat_extracted_text'
    relative_path = filepath[index + len(nougat_path) + 1:]
    # Construct the output directory path
    output_dir = os.path.join('final_markdown_files', os.path.dirname(relative_path))
    # Create directories if they do not exist
    os.makedirs(output_dir, exist_ok=True)
    # Construct the output file path
    output_file = os.path.join(output_dir, os.path.basename(filepath))
    # Save the cleaned text
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"Final markdown saved to: {output_file}")

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


# Custom reducer to merge dicts
def merge_dicts(dict_a: dict, dict_b: dict) -> dict:
    """
    Merge dict_b into dict_a. 
    Returns a new dict, leaving the original dicts unchanged.
    """
    merged = dict_a.copy()
    merged.update(dict_b)
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
        
        # You can replace these lines with your actual logic for generating quotes and reasoning
        quote = f"Quote from {doc_name}"
        reasoning = f"Reasoning about {doc_name}"
        
        # Append to our nested data structure
        grouped_data[code][charity_id][doc_name].append((quote, reasoning))

    # Build the Markdown output
    markdown_lines = []
    for code, charities in grouped_data.items():
        # Top-level heading for code
        markdown_lines.append(f"# {code}")
        
        for charity_id, doc_names in charities.items():
            # Heading for charity_id
            markdown_lines.append(f"## {charity_id}")
            
            for doc_name, entries in doc_names.items():
                # Sub-heading for doc_name
                for (quote, reasoning) in entries:
                    markdown_lines.append(f"### {doc_name}")
                    markdown_lines.append(f"Quote: {quote}")
                    markdown_lines.append(f"Reasoning: {reasoning}")
                    
                    # Optional blank line for spacing
                    markdown_lines.append("")
    
    # Join everything with newlines
    return "\n".join(markdown_lines)