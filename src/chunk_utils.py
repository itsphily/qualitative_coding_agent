import os
from typing import Dict

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