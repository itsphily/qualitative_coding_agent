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

def generate_markdown(prompt_per_code_results: list, unprocessed_documents: list) -> dict:
    """
    Generate markdown strings organized by charity_id.
    
    Args:
        prompt_per_code_results: List of documents, each containing charity data
        unprocessed_documents: List of unprocessed documents
        
    Returns:
        dict: Dictionary with charity_id as key and markdown string as value
    """
    print("Debug - Type of prompt_per_code_results:", type(prompt_per_code_results))
    print("Debug - First item:", prompt_per_code_results[0] if prompt_per_code_results else None)
    
    # Initialize storage for organizing data by charity
    charity_data = {}
    
    try:
        # First pass: Organize data by charity
        for doc in prompt_per_code_results:
            print(f"Debug - Processing document type: {type(doc)}")
            print(f"Debug - Document content: {doc}")
            
            # Skip if doc is not a dictionary
            if not isinstance(doc, dict):
                print(f"Warning: Expected dictionary but got {type(doc)}: {doc}")
                continue
            
            charity_id = doc.get("charity_id")
            if not charity_id:
                print(f"Warning: No charity_id found for document")
                continue
            
            if charity_id not in charity_data:
                charity_data[charity_id] = {
                    "codes": {},
                    "documents": {
                        "important to read": [],
                        "worth reading": [],
                        "not worth reading": []
                    }
                }
            
            # Rest of the function remains the same...
            doc_importance = doc.get("document_importance", "").lower()
            if doc_importance and doc.get("doc_name") not in charity_data[charity_id]["documents"][doc_importance]:
                charity_data[charity_id]["documents"][doc_importance].append(doc.get("doc_name"))
            
            code = doc.get("code")
            if code and code not in charity_data[charity_id]["codes"]:
                charity_data[charity_id]["codes"][code] = {}
            
            if code and doc.get("doc_name") not in charity_data[charity_id]["codes"][code]:
                charity_data[charity_id]["codes"][code][doc.get("doc_name")] = []
            
            if (doc.get("quote") and doc.get("reasoning") and 
                doc.get("quote") != "Empty string" and 
                doc.get("reasoning") != "Empty string"):
                charity_data[charity_id]["codes"][code][doc.get("doc_name")].append({
                    "quote": doc.get("quote"),
                    "reasoning": doc.get("reasoning")
                })
        
        # Second pass: Generate markdown (this part stays exactly the same)
        markdown_output = {}
        
        for charity_id, data in charity_data.items():
            markdown_sections = [f"# Charity Id: {charity_id}\n"]
            
            markdown_sections.append("# Document Importance")
            for importance in ["important to read", "worth reading", "not worth reading"]:
                markdown_sections.append(f"### {importance.title()}")
                for doc_name in data["documents"][importance]:
                    markdown_sections.append(f"- {doc_name}")
                markdown_sections.append("")
            
            for code, documents in data["codes"].items():
                markdown_sections.append(f"## Code: {code}")
                for doc_name, pairs in documents.items():
                    if pairs:
                        markdown_sections.append(f"### Doc Name: {doc_name}")
                        for pair in pairs:
                            markdown_sections.append(f"- **Quote:** {pair['quote']}")
                            markdown_sections.append(f"- **Reasoning:** {pair['reasoning']}\n")
            
            markdown_output[charity_id] = "\n".join(markdown_sections)
        
        return markdown_output
        
    except Exception as e:
        print(f"Error in generate_markdown: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

def save_final_markdown(filepath: str, cleaned_text: dict):
    """
    This function takes a base filepath string and a dictionary (cleaned_text) containing markdown content.
    For each key in the dictionary, it builds a new file path by appending an underscore and the key name
    to the base filename. For example, if filepath is 'quote_reasoning_output.md' and a key is 'GiveDirectly',
    then the final filepath becomes 'quote_reasoning_output_GiveDirectly.md'. The function then writes the
    corresponding markdown content to that file.
    
    Args:
        filepath (str): The base file path (e.g., "quote_reasoning_output.md").
        cleaned_text (dict): A dictionary whose keys determine file name suffixes and whose values are
                             the markdown content to be saved.
    """
    import os
    
    output_dir = "coding_output"
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Split the base filepath into filename and extension
    base_filename, base_ext = os.path.splitext(filepath)
    if not base_ext:
        base_ext = ".md"  # default extension
    
    # Iterate over each key-value pair in the cleaned_text dictionary
    for key, content in cleaned_text.items():
        final_filename = f"{base_filename}_{key}{base_ext}"
        final_filepath = os.path.join(output_dir, final_filename)
        
        # Save the corresponding markdown content to the file
        with open(final_filepath, 'w', encoding='utf-8') as file:
            file.write(content)


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

def transform_qa_results_to_list(qa_results_list: list) -> list:
    """
    Transform a list of QAValuePerCode objects into a list of dictionaries containing:
        - charity_id (str)
        - code (str)
        - doc_name (str)
        - quote (str)
        - reasoning (str)
        - document_importance (str)
    """
    return [
        {
            "charity_id": item.charity_id,
            "code": item.code,
            "doc_name": item.doc_name,
            "quote": item.quote,
            "reasoning": item.reasoning,
            "document_importance": item.document_importance
        }
        for item in qa_results_list
    ]

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
