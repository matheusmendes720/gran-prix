"""
Generate visual documentation from Mermaid diagrams.

Converts .mmd files to beautiful HTML pages with interactive diagrams.
"""

import os
from pathlib import Path
from typing import List
import re

# Paths
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
DIAGRAMS_DIR = DOCS_DIR / "diagrams"
OUTPUT_DIR = BASE_DIR / "docs_html"

def find_mermaid_files() -> List[Path]:
    """Find all .mmd files in docs directory."""
    if not DIAGRAMS_DIR.exists():
        print(f"[!] Diagrams directory not found: {DIAGRAMS_DIR}")
        return []
    diagrams = list(DIAGRAMS_DIR.glob("*.mmd"))
    print(f"[+] Found {len(diagrams)} Mermaid diagrams")
    return diagrams

def load_mermaid_content(file_path: Path) -> str:
    """Load content from .mmd file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_html_page(title: str, mermaid_content: str, description: str = "") -> str:
    """
    Generate beautiful HTML page with Mermaid diagram.
    
    Uses Material Design theme with dark mode.
    """
    
    # Escape special characters in Mermaid
    mermaid_escaped = mermaid_content.replace('`', '\\`')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Nova Corrente</title>
    
    <!-- Material Design Icons -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    
    <!-- Material Design CSS -->
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    
    <!-- Mermaid.js -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            color: #f5f5f5;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: #2d2d2d;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 300;
            color: white;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .description {{
            background: #3d3d3d;
            border-left: 4px solid #4A90E2;
            padding: 20px;
            margin-bottom: 40px;
            border-radius: 8px;
        }}
        
        .diagram-container {{
            background: #1e1e1e;
            border-radius: 12px;
            padding: 40px;
            overflow-x: auto;
            margin-bottom: 40px;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
        }}
        
        .mermaid {{
            text-align: center;
        }}
        
        /* Mermaid overrides for dark theme */
        .mermaid svg {{
            max-width: 100%;
            height: auto;
        }}
        
        .footer {{
            background: #1a1a1a;
            padding: 30px 40px;
            text-align: center;
            color: #888;
            font-size: 0.9rem;
        }}
        
        .nav-links {{
            margin-top: 20px;
        }}
        
        .nav-links a {{
            color: #4A90E2;
            text-decoration: none;
            margin: 0 15px;
            padding: 8px 16px;
            border: 1px solid #4A90E2;
            border-radius: 4px;
            transition: all 0.3s;
        }}
        
        .nav-links a:hover {{
            background: #4A90E2;
            color: white;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .diagram-container {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>Nova Corrente - Demand Forecasting System</p>
        </div>
        
        <div class="content">
            {f'<div class="description"><p>{description}</p></div>' if description else ''}
            
            <div class="diagram-container">
                <div class="mermaid">
{mermaid_content}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Nova Corrente Documentation System</p>
            <div class="nav-links">
                <a href="index.html">← Back to Index</a>
                <a href="../docs/COMPLETE_DATASET_MASTER_INDEX.md">📚 Documentation</a>
                <a href=".." onclick="window.history.back(); return false;">🔙 Previous</a>
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            securityLevel: 'loose',
            themeVariables: {{
                primaryColor: '#1e1e1e',
                primaryTextColor: '#fff',
                primaryBorderColor: '#444',
                lineColor: '#888',
                secondaryColor: '#2d2d2d',
                tertiaryColor: '#1a1a1a'
            }},
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
</body>
</html>"""
    
    return html

def generate_index_page(diagram_files: List[Path]) -> str:
    """Generate index page listing all diagrams."""
    
    diagram_list = ""
    for diagram in diagram_files:
        title = diagram.stem.replace('_', ' ').title()
        filename = diagram.with_suffix('.html').name
        diagram_list += f"""
            <div class="diagram-card">
                <h3>{title}</h3>
                <a href="{filename}" class="view-link">View Diagram →</a>
            </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nova Corrente - Visual Documentation</title>
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            color: #f5f5f5;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
            border-radius: 16px;
            margin-bottom: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 300;
            color: white;
            margin-bottom: 15px;
        }}
        
        .header p {{
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .diagrams-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 30px;
        }}
        
        .diagram-card {{
            background: #2d2d2d;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .diagram-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }}
        
        .diagram-card h3 {{
            font-size: 1.3rem;
            margin-bottom: 15px;
            color: #4A90E2;
        }}
        
        .view-link {{
            display: inline-block;
            color: #4A90E2;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        .view-link:hover {{
            color: #66b3ff;
        }}
        
        .footer {{
            margin-top: 60px;
            text-align: center;
            padding: 30px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Visual Documentation</h1>
            <p>Nova Corrente - System Architecture Diagrams</p>
        </div>
        
        <div class="diagrams-grid">
{diagram_list}
        </div>
        
        <div class="footer">
            <p>📊 System Architecture Documentation | Nova Corrente Grand Prix</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Generate all HTML documentation from Mermaid diagrams."""
    # Set UTF-8 encoding for stdout on Windows
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("="*80)
    print("GENERATING VISUAL DOCUMENTATION")
    print("Nova Corrente - System Architecture")
    print("="*80)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all .mmd files
    diagram_files = find_mermaid_files()
    
    if not diagram_files:
        print("[!] No .mmd files found in docs/diagrams/")
        return
    
    # Generate HTML for each diagram
    for diagram_file in diagram_files:
        print(f"\n[+] Processing: {diagram_file.name}")
        
        # Load content
        mermaid_content = load_mermaid_content(diagram_file)
        
        # Generate title
        title = diagram_file.stem.replace('_', ' ').title()
        
        # Generate description
        descriptions = {
            'nova_corrente_system_architecture': 'Complete system architecture showing data flow from sources through preprocessing, models, evaluation, visualization, and deployment.',
            'brazilian_integration_flow': 'Brazilian dataset integration pipeline showing download, parsing, enrichment, and integration phases with 22 new features.'
        }
        description = descriptions.get(diagram_file.stem, '')
        
        # Generate HTML
        html = generate_html_page(title, mermaid_content, description)
        
        # Save HTML file
        output_file = OUTPUT_DIR / diagram_file.with_suffix('.html').name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[OK] Generated: {output_file.name}")
    
    # Generate index page
    print("\n[+] Generating index page...")
    index_html = generate_index_page(diagram_files)
    index_file = OUTPUT_DIR / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"[OK] Generated: {index_file.name}")
    
    print("\n" + "="*80)
    print("[SUCCESS] VISUAL DOCUMENTATION GENERATION COMPLETE")
    print("="*80)
    print(f"\n[INFO] Output directory: {OUTPUT_DIR}")
    print(f"[INFO] Generated {len(diagram_files)} diagram pages + index")
    print(f"\n[INFO] Open in browser: {OUTPUT_DIR / 'index.html'}")
    print("\nNext steps:")
    print("1. Open index.html in your browser")
    print("2. Click on any diagram to view")
    print("3. Share links to team members")

if __name__ == "__main__":
    main()


