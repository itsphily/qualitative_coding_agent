from pathlib import Path
from collections import defaultdict
import sys
from io import StringIO
import os
from dotenv import load_dotenv
import getpass
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma



folder_path = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/01_GiveDirectly"
folder = folder_path.split("/")[-1]
# Load environment variables from .env file
load_dotenv()

# Get the API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=200
)

vector_store = Chroma.from_documents(
    documents=doc_splits,
    collection_name="vector_store{}".format(folder),
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

def get_markdown_filepaths(base_directory):
    """
    Recursively retrieve all markdown file paths from the given directory and its subdirectories.
    
    Args:
        base_directory (str): The root directory to start searching from
        
    Returns:
        list: A list of Path objects for all markdown files found
    """
    base_path = Path(base_directory)
    if not base_path.exists():
        raise FileNotFoundError(f"Directory not found: {base_directory}")
    
    # Use rglob to recursively find all .md files
    markdown_files = list(base_path.rglob("*.md"))
    return markdown_files

def get_documents_by_main_directory(base_directory):
    """
    Create a dictionary with main directory names as keys and lists of all documents (including those in subdirectories) as values.
    
    Args:
        base_directory (str): The root directory to start searching from
        
    Returns:
        dict: A dictionary where keys are main directory names and values are lists of document names
    """
    try:
        markdown_files = get_markdown_filepaths(base_directory)
        
        # Create a dictionary to organize files by main directory
        organized_files = defaultdict(list)
        base_path = Path(base_directory)
        
        for file_path in markdown_files:
            # Get the relative path from the base directory
            relative_path = file_path.relative_to(base_path)
            # Get the main directory (first part of the path)
            main_dir = str(relative_path).split('/')[0]
            # Add the filename to the appropriate directory list
            organized_files[main_dir].append(file_path.name)
        
        # Convert defaultdict to regular dict and sort the file lists
        return {k: sorted(v) for k, v in organized_files.items()}
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def print_organized_documents(base_directory, output_file=None):
    """
    Print all markdown documents organized by their directory structure.
    
    Args:
        base_directory (str): The root directory to start searching from
        output_file (str, optional): If provided, write the output to this file instead of printing to console
    """
    try:
        markdown_files = get_markdown_filepaths(base_directory)
        
        # Create a dictionary to organize files by directory
        organized_files = defaultdict(list)
        base_path = Path(base_directory)
        
        for file_path in markdown_files:
            # Get the relative path from the base directory
            relative_path = file_path.relative_to(base_path)
            # Get the parent directory path
            parent_dir = str(relative_path.parent)
            # Add the filename to the appropriate directory list
            organized_files[parent_dir].append(file_path.name)
        
        # Create the output string
        output = StringIO()
        output.write(f"\nDocument Structure in {base_directory}:\n")
        output.write("=" * 50 + "\n")
        
        for directory, files in sorted(organized_files.items()):
            output.write(f"\n📁 {directory}\n")
            for file in sorted(files):
                output.write(f"  📄 {file}\n")
        
        result = output.getvalue()
        output.close()
        
        if output_file:
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Document structure has been written to {output_file}")
        else:
            # Print to console
            print(result)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_structure_to_file(base_directory, output_file):
    """
    Write the document structure to a specified file.
    
    Args:
        base_directory (str): The root directory to start searching from
        output_file (str): The file to write the structure to
    """
    print_organized_documents(base_directory, output_file)

if __name__ == "__main__":
    # Example usage with the specified directory
    base_dir = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files"
    
    # Get documents organized by main directory
    docs_by_directory = get_documents_by_main_directory(base_dir)
    
    # Print the dictionary to see the structure
    for main_dir, files in sorted(docs_by_directory.items()):
        print(f"\nMain Directory: {main_dir}")
        print(f"Number of files: {len(files)}")
        print("Files:")
        for file in files:
            print(f"  - {file}")