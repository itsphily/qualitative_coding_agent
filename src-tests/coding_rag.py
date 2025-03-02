from pathlib import Path
from collections import defaultdict
import sys
from io import StringIO
import os
from dotenv import load_dotenv
import getpass
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from uuid import uuid4
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

# Get the API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

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

def process_documents(folder_path):
    """
    Process documents from a folder and create a vector store.
    
    Args:
        folder_path (str): Path to the folder containing markdown files
    """
    folder = folder_path.split("/")[-1]
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=200
    )
    
    # Load and process documents
    all_docs = []
    md_files = list(Path(folder_path).rglob("*.md"))
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        all_docs.append(Document(page_content=text, metadata={"source": str(file_path)}))
    
    # Split documents
    doc_splits = text_splitter.split_documents(all_docs)
    
    # Create persist directory if it doesn't exist
    persist_dir = "./chroma_db"
    os.makedirs(persist_dir, exist_ok=True)
    
    # Initialize and persist Chroma store
    vector_store = Chroma.from_documents(
        documents=doc_splits,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=f"vector_store_{folder}"
    )
    
    # Create retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    
    return retriever

if __name__ == "__main__":
    # Example usage with the specified directory
    base_dir = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files"
    folder_path = f"{base_dir}/01_GiveDirectly"
    
    # Get documents organized by main directory
    docs_by_directory = get_documents_by_main_directory(base_dir)
    
    # Print the dictionary to see the structure
    for main_dir, files in sorted(docs_by_directory.items()):
        print(f"\nMain Directory: {main_dir}")
        print(f"Number of files: {len(files)}")
        print("Files:")
        for file in files:
            print(f"  - {file}")
    
    # Process documents and create retriever
    retriever = process_documents(folder_path)
    
    # Test the retriever
    question = "how to estimate the ROI from cash transfers"
    retrieved_docs = retriever.get_relevant_documents(question)
    
    print(f"\nNumber of retrieved texts: {len(retrieved_docs)}\n")
    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"Document {i}:\n{doc.page_content}\n{'-' * 40}\n")

