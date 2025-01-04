# PDF to Markdown Converter

A Python-based tool that extracts text from PDF documents and converts it into clean, well-structured Markdown format. The tool uses advanced AI models for text extraction and cleaning, including Nougat for PDF processing and various language models for text restructuring.

## Features

- PDF text extraction using Nougat model
- Intelligent text cleaning and restructuring
- Boilerplate removal
- Markdown formatting
- Quality assurance feedback
- Support for batch processing
- Maintains directory structure for processed files

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (optional, for faster processing)
- Access to required API keys (OpenAI, Deepseek)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy the sample environment file:
     ```bash
     cp .env.sample .env
     ```
   - Open the `.env` file and replace the placeholder values with your actual API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     DEEPSEEK_API_KEY=your_deepseek_api_key_here
     # Optional APIs
     TAVILY_API_KEY=your_tavily_api_key_here
     GOOGLE_API_KEY=your_google_api_key_here
     LANGCHAIN_API_KEY=your_langchain_api_key_here
     ```

## Project Structure

```
.
├── src/
│   ├── PDF extract to md one prompt.py  # Main script with graph-based processing
│   ├── PDF to Markdown.py               # Alternative implementation
│   ├── prompt.py                        # LLM prompts
│   ├── state.py                         # State management
│   └── utils.py                         # Utility functions
├── storage/
│   ├── case documents/                  # Input PDFs
│   ├── nougat_extracted_text/           # Extracted text
│   └── cleaned_text_v2/                 # Cleaned output
└── cleaned_text_outputs/                # QA outputs
```

## Usage

### Using the Graph-based Implementation

```python
from src.PDF_extract_to_md_one_prompt import main

# Run the processing pipeline
main()
```

### Using the Batch Processing Implementation

```python
from src.PDF_to_Markdown import process_all_pdfs, process_extracted_text

# Process PDFs to extract text
pdf_stats = process_all_pdfs()

# Clean the extracted text
cleaning_stats = process_extracted_text()
```

## Processing Pipeline

1. **PDF Text Extraction**: Uses Nougat model to extract text while preserving structure
2. **Text Cleaning**: Reconstructs fragmented sentences and removes page labels
3. **Boilerplate Removal**: Identifies and removes repeated headers, footers, and notices
4. **Markdown Formatting**: Converts the cleaned text into proper Markdown format
5. **Quality Assurance**: Provides feedback on the cleaning process

## Output

The processed files maintain the same directory structure as the input:
- Extracted text: `storage/nougat_extracted_text/<case>/<subfolder>/`
- Cleaned text: `storage/cleaned_text_v2/<case>/<subfolder>/`
- QA outputs: `cleaned_text_outputs/`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.