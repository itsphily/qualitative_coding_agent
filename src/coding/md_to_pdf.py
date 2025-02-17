import os
import argparse
import subprocess

def convert_md_to_pdf(input_path, output_path):
    """
    Convert a markdown file to PDF with nice formatting using pandoc and Chrome.
    
    Args:
        input_path (str): Path to the input markdown file.
        output_path (str): Path for the output PDF file.
    """
    # Create temporary HTML and CSS file paths based on the input markdown file
    html_path = os.path.splitext(input_path)[0] + '.html'
    css_path = os.path.join(os.path.dirname(input_path), 'style.css')
    
    # CSS content for better formatting
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
    
    # Write the CSS content to a file
    with open(css_path, 'w') as f:
        f.write(css_content)
    
    # Convert markdown to HTML using pandoc
    cmd_html = [
        'pandoc',
        input_path,
        '-o', html_path,
        '--css', css_path,
        '--self-contained',
        '-s',  # Generate a standalone HTML file
        '--highlight-style=tango'
    ]
    
    try:
        subprocess.run(cmd_html, check=True, capture_output=True, text=True)
        
        # Convert HTML to PDF using Google Chrome in headless mode
        cmd_pdf = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu',
            '--print-to-pdf=' + output_path,
            '--no-pdf-header-footer',
            html_path
        ]
        subprocess.run(cmd_pdf, check=True, capture_output=True, text=True)
        
        # Remove temporary HTML and CSS files
        os.remove(html_path)
        os.remove(css_path)
        
        print(f"PDF generated successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting markdown to PDF for {input_path}: {e.stderr}")
        raise
    except FileNotFoundError as e:
        print("Error: Required tools not installed. Please install:")
        print("1. pandoc: brew install pandoc")
        print("2. Google Chrome")
        raise

def main():
    parser = argparse.ArgumentParser(
        description='Search a directory for all .md files and convert them to PDFs in a folder called coding_output_pdf'
    )
    parser.add_argument('input_path', help='Path to a markdown file or directory containing markdown files')
    args = parser.parse_args()
    
    # Determine the directory to search:
    # If a directory is provided, use it; if a file is provided, use its directory.
    if os.path.isdir(args.input_path):
        search_dir = args.input_path
    elif os.path.isfile(args.input_path):
        search_dir = os.path.dirname(args.input_path)
    else:
        print("Invalid input path provided.")
        return
    
    # Create output directory named 'coding_output_pdf' inside the search directory
    output_dir = os.path.join(search_dir, 'coding_output_pdf')
    os.makedirs(output_dir, exist_ok=True)
    
    # Get a list of all .md files in the search directory
    md_files = [f for f in os.listdir(search_dir) if f.lower().endswith('.md')]
    
    if not md_files:
        print("No markdown files found in directory:", search_dir)
        return
    
    # Convert each markdown file to a PDF, saving it in the output directory
    for md_file in md_files:
        md_path = os.path.join(search_dir, md_file)
        pdf_name = os.path.splitext(md_file)[0] + '.pdf'
        output_pdf_path = os.path.join(output_dir, pdf_name)
        print(f"Converting {md_path} to {output_pdf_path}...")
        try:
            convert_md_to_pdf(md_path, output_pdf_path)
        except Exception as e:
            print(f"Failed to convert {md_path}: {e}")

if __name__ == '__main__':
    main()