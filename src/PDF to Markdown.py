import os
from typing import List, Dict
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from prompt import restructure_text_prompt, text_to_reformat_prompt, pdf_extraction_prompt
from transformers import NougatProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
from pdf2image import convert_from_path
from dotenv import load_dotenv

load_dotenv()
# LLM
#------------------------------------------------------------------------------
local_llm = 'llama3.3:70b-instruct-q2_K'
llm_chatgpt = ChatOpenAI(model="gpt-4o", temperature=0)
llm = ChatOllama(model=local_llm, temperature=0)
llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json")

# Initialize Nougat model and processor (do it once at module level)
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = NougatProcessor.from_pretrained("facebook/nougat-base")
model = VisionEncoderDecoderModel.from_pretrained("facebook/nougat-base").to(device)

def extract_text_from_pdf(pdf_path: str) -> bool:
    """
    Extract text from a PDF file using Nougat and save it to a corresponding .md file 
    in the 'nougat_extracted_text' directory.
    The output file maintains the same folder structure and naming as the input file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        bool: True if successful, False if an error occurred
    """
    try:
        # Convert to Path object for easier manipulation
        pdf_path = Path(pdf_path)
        
        # Check if file exists
        if not pdf_path.is_file():
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
        
        # Get the case name and subfolder from the path (case-insensitive)
        parts = pdf_path.parts
        case_docs_index = next(i for i, part in enumerate(parts) if part.lower() == 'case documents')
        case_name = parts[case_docs_index + 1]  
        subfolder = parts[case_docs_index + 2]  
        
        # Create the output path
        output_dir = Path('storage/nougat_extracted_text') / case_name.replace(' ', '_') / subfolder
        output_file = output_dir / pdf_path.name.replace('.pdf', '.md')
        
        # Create directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert PDF to images
        images = convert_from_path(str(pdf_path))
        
        # Process each page
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, image in enumerate(images):
                print(f"Processing page {i+1}/{len(images)}")
                
                # Prepare image for model
                pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
                
                # Generate text
                outputs = model.generate(
                    pixel_values,
                    max_length=1024,
                    num_beams=4,
                    early_stopping=True
                )
                
                # Decode the outputs
                decoded_text = processor.decode(outputs[0], skip_special_tokens=True)
                
                # Write to file with page marker
                f.write(f"=== Page {i+1} ===\n\n")
                f.write(decoded_text + "\n\n")
        
        print(f"Successfully extracted text to: {output_file}")
        return True
    
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return False

def clean_extracted_text(input_file: str) -> bool:
    """
    Process an extracted text file through the LLM for cleaning and restructuring.
    Saves the cleaned text in a parallel directory structure under 'cleaned_text_v2'.
    
    Args:
        input_file (str): Path to the extracted text file to process
        
    Returns:
        bool: True if successful, False if an error occurred
    """
    try:
        # Convert to Path object for easier manipulation
        input_path = Path(input_file)
        
        # Check if file exists
        if not input_path.is_file():
            raise FileNotFoundError(f"Text file not found at: {input_path}")
        
        # Read the input file
        with open(input_path, 'r', encoding='utf-8') as f:
            text_to_be_cleaned = f.read()
        
        # Process through LLM
        text_to_reformat_prompt_filled = text_to_reformat_prompt.format(text_to_be_cleaned=text_to_be_cleaned)
        response = llm.invoke([
            SystemMessage(content=restructure_text_prompt),
            HumanMessage(content=text_to_reformat_prompt_filled)
        ])
        
        # Create the output path (replace 'nougat_extracted_text' with 'cleaned_text_v2' in the path)
        output_path = Path(str(input_path).replace('nougat_extracted_text', 'cleaned_text_v2'))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the cleaned text
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.content)
        
        print(f"Successfully cleaned text saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing text through LLM: {str(e)}")
        return False

def process_all_pdfs(base_directory: str = "storage/case documents") -> Dict[str, int]:
    """
    Process all PDF files in the base directory and its subdirectories.
    
    Args:
        base_directory (str): Base directory containing case folders
        
    Returns:
        Dict[str, int]: Statistics about the processing {'success': n, 'failed': m}
    """
    stats = {'success': 0, 'failed': 0}
    base_path = Path(base_directory)
    
    if not base_path.exists():
        print(f"Error: Base directory '{base_directory}' not found!")
        return stats
    
    # Walk through all subdirectories
    for case_dir in base_path.iterdir():
        if not case_dir.is_dir() or case_dir.name.startswith('.'):
            continue
            
        print(f"\nProcessing case: {case_dir.name}")
        print("-" * 50)
        
        # Process each subfolder in the case directory
        for subfolder in case_dir.iterdir():
            if not subfolder.is_dir() or subfolder.name.startswith('.'):
                continue
                
            print(f"\nProcessing subfolder: {subfolder.name}")
            
            # Process each PDF in the subfolder
            for pdf_file in subfolder.glob('*.pdf'):
                print(f"\nProcessing: {pdf_file.name}")
                if extract_text_from_pdf(str(pdf_file)):
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
    
    return stats

def process_extracted_text(base_directory: str = "storage/nougat_extracted_text") -> Dict[str, int]:
    """
    Process all extracted text files through the LLM.
    
    Args:
        base_directory (str): Base directory containing extracted text files
        
    Returns:
        Dict[str, int]: Statistics about the processing {'success': n, 'failed': m}
    """
    stats = {'success': 0, 'failed': 0}
    base_path = Path(base_directory)
    
    if not base_path.exists():
        print(f"Error: Base directory '{base_directory}' not found!")
        return stats
    
    # Walk through all subdirectories
    for case_dir in base_path.iterdir():
        if not case_dir.is_dir() or case_dir.name.startswith('.'):
            continue
            
        print(f"\nProcessing case: {case_dir.name}")
        print("-" * 50)
        
        # Process each subfolder in the case directory
        for subfolder in case_dir.iterdir():
            if not subfolder.is_dir() or subfolder.name.startswith('.'):
                continue
                
            print(f"\nProcessing subfolder: {subfolder.name}")
            
            # Process each markdown file in the subfolder
            for text_file in subfolder.glob('*.md'):
                print(f"\nProcessing: {text_file.name}")
                if clean_extracted_text(str(text_file)):
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
    
    return stats

if __name__ == "__main__":
    # First, process PDFs to extract text using Nougat
    #print("Starting PDF processing with Nougat...")
    #print("=" * 50)
    #pdf_stats = process_all_pdfs()
    #print("\nPDF Processing Complete!")
    #print("=" * 50)
    #print(f"Successfully processed: {pdf_stats['success']} PDFs")
    #print(f"Failed to process: {pdf_stats['failed']} PDFs")
    
    # Then, clean the extracted text
    print("\nStarting text cleaning process...")
    print("=" * 50)
    cleaning_stats = process_extracted_text()
    print("\nText Cleaning Complete!")
    print("=" * 50)
    print(f"Successfully cleaned: {cleaning_stats['success']} files")
    print(f"Failed to clean: {cleaning_stats['failed']} files")
