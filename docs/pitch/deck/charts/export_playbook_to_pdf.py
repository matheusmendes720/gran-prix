#!/usr/bin/env python3
"""
Script to export kickoff_charts_playbook.md to PDF with proper image rendering.
Uses Playwright to convert Markdown (via HTML) to PDF, preserving all images.
"""

import os
import sys
from pathlib import Path
import markdown
from playwright.sync_api import sync_playwright

def convert_markdown_to_pdf(md_file_path, pdf_file_path=None):
    """
    Convert a Markdown file to PDF with proper image rendering.
    
    Args:
        md_file_path: Path to the Markdown file
        pdf_file_path: Optional output PDF path (defaults to same name as .md file)
    """
    md_path = Path(md_file_path)
    
    if not md_path.exists():
        print(f"Error: File not found: {md_file_path}")
        return False
    
    # Set output PDF path
    if pdf_file_path is None:
        pdf_file_path = md_path.with_suffix('.pdf')
    else:
        pdf_file_path = Path(pdf_file_path)
    
    # Read markdown file
    print(f"Reading markdown file: {md_path}")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    # Configure markdown to handle images properly
    md = markdown.Markdown(extensions=['extra', 'tables', 'codehilite', 'fenced_code'])
    html_content = md.convert(md_content)
    
    # Get the directory of the markdown file for resolving relative paths
    md_dir = md_path.parent.absolute()
    
    # Create full HTML document with proper base path and styling
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            page-break-inside: avoid;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 5px 0;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ecf0f1;
            margin: 30px 0;
        }}
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        p {{
            margin: 10px 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # Write HTML to temporary file
    html_file = md_path.with_suffix('.html')
    print(f"Creating temporary HTML file: {html_file}")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    # Convert HTML to PDF using Playwright
    print(f"Converting to PDF using Playwright: {pdf_file_path}")
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Load HTML file with file:// protocol to resolve relative image paths
            # On Windows, need to handle path conversion properly
            html_path = html_file.resolve()
            if os.name == 'nt':  # Windows
                file_url = f"file:///{html_path.as_posix()}"
            else:
                file_url = f"file://{html_path}"
            page.goto(file_url, wait_until='networkidle', timeout=30000)
            
            # Generate PDF
            page.pdf(
                path=str(pdf_file_path),
                format='A4',
                margin={
                    'top': '2cm',
                    'right': '2cm',
                    'bottom': '2cm',
                    'left': '2cm'
                },
                print_background=True
            )
            
            browser.close()
        
        # Clean up temporary HTML file
        html_file.unlink()
        
        print(f"Successfully created PDF: {pdf_file_path}")
        return True
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        import traceback
        traceback.print_exc()
        # Clean up temporary HTML file even on error
        if html_file.exists():
            html_file.unlink()
        return False

if __name__ == "__main__":
    # Default to kickoff_charts_playbook.md in the same directory
    script_dir = Path(__file__).parent
    default_md = script_dir / "kickoff_charts_playbook.md"
    
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
    else:
        md_file = str(default_md)
    
    if len(sys.argv) > 2:
        pdf_file = sys.argv[2]
    else:
        pdf_file = None
    
    success = convert_markdown_to_pdf(md_file, pdf_file)
    sys.exit(0 if success else 1)
