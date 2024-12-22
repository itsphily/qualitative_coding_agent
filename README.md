# PDF Processing and Text Extraction Tool

This tool processes PDF documents using Nougat (a state-of-the-art PDF understanding model) and cleans the extracted text using LLM-based processing. It maintains the directory structure of your documents while processing them.

## Features

- PDF text extraction using Nougat model
- Maintains original document structure and formatting
- LLM-based text cleaning and restructuring
- Recursive directory processing
- Progress tracking and statistics

## Directory Structure

```
.
├── src/
│   ├── coding_agent.py    # Main processing script
│   └── prompt.py          # LLM prompts for text processing
├── storage/
│   ├── case documents/    # Input PDF files
│   ├── nougat_extracted_text/  # Raw extracted text
│   └── cleaned_text_v2/   # Cleaned and processed text
```

## Prerequisites

- Python 3.12+
- Conda environment
- Poppler (for PDF processing)

## Installation

1. Create and activate a conda environment:
```bash
conda create -n coding_agent python=3.12
conda activate coding_agent
```

2. Install required Python packages (choose one method):

   Method A: Using requirements.txt (recommended):
   ```bash
   pip install -r requirements.txt
   ```

   Method B: Installing packages manually:
   ```bash
   pip install nougat-ocr pdf2image langchain-ollama langchain-core transformers torch torchvision
   ```

3. Install Poppler (required for PDF processing):
   - On macOS:
   ```bash
   brew install poppler
   ```
   - On Linux:
   ```bash
   apt-get install poppler-utils
   ```
   - On Windows:
   Download from: http://blog.alivate.com.au/poppler-windows/

## Usage

1. Place your PDF files in the `storage/case documents` directory, maintaining your desired folder structure.

2. Run the processing script:
```bash
python src/coding_agent.py
```

The script will:
1. Process all PDFs using Nougat and save the extracted text in `storage/nougat_extracted_text`
2. Clean and restructure the extracted text using LLM and save it in `storage/cleaned_text_v2`

## Output

- **Raw Extracted Text**: Found in `storage/nougat_extracted_text/`, preserving the original directory structure
- **Cleaned Text**: Found in `storage/cleaned_text_v2/`, with improved formatting and structure

## Dependencies

Main dependencies (see requirements.txt for complete list):
- `nougat-ocr`: For PDF text extraction
- `pdf2image`: For converting PDFs to images
- `langchain-ollama`: For LLM integration
- `transformers`: For the Nougat model
- `torch`: For neural network operations
- `Poppler`: For PDF processing

## Notes

- The script processes PDFs recursively, maintaining the original folder structure
- Progress and statistics are displayed during processing
- Errors are logged but won't stop the overall processing
- Make sure to check requirements.txt for the complete list of dependencies and their versions