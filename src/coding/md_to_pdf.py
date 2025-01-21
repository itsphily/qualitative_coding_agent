import os
import argparse
import subprocess

def convert_md_to_pdf(input_path, output_path=None):
    """
    Convert a markdown file to PDF with nice formatting using pandoc.
    
    Args:
        input_path (str): Path to the input markdown file
        output_path (str, optional): Path for the output PDF file. If not provided,
                                   will use the same name as input with .pdf extension
    """
    # If no output path specified, create one based on input path
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.pdf'
    
    # Build the pandoc command
    cmd = [
        'pandoc',
        input_path,
        '-o', output_path,
        '--pdf-engine=xelatex',
        '-V', 'geometry:margin=1in',
        '-V', 'fontsize=11pt',
        '--highlight-style=tango'
    ]
    
    try:
        # Run pandoc command
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"PDF generated successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting markdown to PDF: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Error: pandoc is not installed. Please install it using: brew install pandoc")
        raise

def main():
    parser = argparse.ArgumentParser(description='Convert markdown file to PDF')
    parser.add_argument('input_path', help='Path to input markdown file')
    parser.add_argument('--output', '-o', help='Path to output PDF file (optional)')
    args = parser.parse_args()
    
    convert_md_to_pdf(args.input_path, args.output)

if __name__ == '__main__':
    main() 