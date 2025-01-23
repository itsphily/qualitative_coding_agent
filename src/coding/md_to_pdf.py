import os
import argparse
import subprocess

def convert_md_to_pdf(input_path, output_path=None):
    """
    Convert a markdown file to PDF with nice formatting using pandoc and Chrome.
    
    Args:
        input_path (str): Path to the input markdown file
        output_path (str, optional): Path for the output PDF file. If not provided,
                                   will use the same name as input with .pdf extension
    """
    # If no output path specified, create one based on input path
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.pdf'
    
    # First convert markdown to HTML using pandoc
    html_path = os.path.splitext(input_path)[0] + '.html'
    
    # Add CSS for better formatting
    css_content = """
    body { 
        margin: 40px auto;
        max-width: 800px;
        line-height: 1.6;
        font-size: 16px;
        color: #444;
        padding: 0 10px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    h1, h2, h3 { line-height: 1.2; color: #333; }
    pre { background-color: #f5f5f5; padding: 10px; border-radius: 4px; }
    code { background-color: #f5f5f5; padding: 2px 4px; border-radius: 4px; }
    blockquote { border-left: 4px solid #ccc; margin: 0; padding-left: 16px; }
    """
    
    css_path = os.path.join(os.path.dirname(input_path), 'style.css')
    with open(css_path, 'w') as f:
        f.write(css_content)
    
    # Convert to HTML first
    cmd_html = [
        'pandoc',
        input_path,
        '-o', html_path,
        '--css', css_path,
        '--self-contained',
        '-s',  # Standalone document
        '--highlight-style=tango'
    ]
    
    try:
        # Run pandoc command to create HTML
        subprocess.run(cmd_html, check=True, capture_output=True, text=True)
        
        # Then convert HTML to PDF using Chrome in headless mode
        cmd_pdf = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu',
            '--print-to-pdf=' + output_path,
            '--no-pdf-header-footer',
            html_path
        ]
        subprocess.run(cmd_pdf, check=True, capture_output=True, text=True)
        
        # Clean up temporary files
        os.remove(html_path)
        os.remove(css_path)
        
        print(f"PDF generated successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting markdown to PDF: {e.stderr}")
        raise
    except FileNotFoundError as e:
        print("Error: Required tools not installed. Please install:")
        print("1. pandoc: brew install pandoc")
        print("2. Google Chrome")
        raise

def main():
    parser = argparse.ArgumentParser(description='Convert markdown file to PDF')
    parser.add_argument('input_path', help='Path to input markdown file')
    parser.add_argument('--output', '-o', help='Path to output PDF file (optional)')
    args = parser.parse_args()
    
    convert_md_to_pdf(args.input_path, args.output)

if __name__ == '__main__':
    main() 