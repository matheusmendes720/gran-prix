"""
Convert Mermaid .mmd files to Markdown documentation files.

This script finds all .mmd files in the project and converts them to
properly formatted markdown documentation files with embedded Mermaid diagrams.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "docs" / "diagrams"
DESCRIPTIONS = {
    'data_strategy_visual_breakdown': 'Visual breakdown of the data strategy implementation, showing problem diagnosis, current data inventory, solution architecture, and expected impact.',
    'brazilian_integration_flow': 'Brazilian dataset integration pipeline showing download, parsing, enrichment, and integration phases with 22 new features.',
    'nova_corrente_system_architecture': 'Complete system architecture showing data flow from sources through preprocessing, models, evaluation, visualization, and deployment.',
}


def find_mmd_files(root_dir: Path = None) -> List[Path]:
    """
    Find all .mmd files in the project.
    
    Args:
        root_dir: Root directory to search. Defaults to PROJECT_ROOT.
        
    Returns:
        List of paths to .mmd files.
    """
    if root_dir is None:
        root_dir = PROJECT_ROOT
    
    mmd_files = list(root_dir.rglob("*.mmd"))
    print(f"[+] Found {len(mmd_files)} Mermaid diagram file(s)")
    return sorted(mmd_files)


def load_mmd_content(file_path: Path) -> str:
    """
    Load content from a .mmd file.
    
    Args:
        file_path: Path to the .mmd file.
        
    Returns:
        Content of the file as string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"[!] Error reading {file_path}: {e}")
        return ""


def extract_title_from_filename(filename: str) -> str:
    """
    Convert filename to a readable title.
    
    Args:
        filename: Filename without extension.
        
    Returns:
        Formatted title.
    """
    # Replace underscores and hyphens with spaces
    title = filename.replace('_', ' ').replace('-', ' ')
    # Title case
    title = title.title()
    return title


def extract_description_from_content(content: str) -> Optional[str]:
    """
    Try to extract description from Mermaid diagram content.
    
    Args:
        content: Mermaid diagram content.
        
    Returns:
        Description if found, None otherwise.
    """
    # Look for subgraph labels that might contain descriptions
    subgraph_pattern = r'subgraph\s+\w+\["([^"]+)"\]'
    matches = re.findall(subgraph_pattern, content)
    
    if matches:
        # Use the first meaningful subgraph label
        return f"Diagram showing: {', '.join(matches[:3])}"
    
    return None


def generate_markdown_content(
    title: str,
    mermaid_content: str,
    description: Optional[str] = None,
    source_file: Optional[Path] = None
) -> str:
    """
    Generate markdown documentation content.
    
    Args:
        title: Title for the documentation.
        mermaid_content: Mermaid diagram code.
        description: Optional description.
        source_file: Optional source .mmd file path.
        
    Returns:
        Complete markdown content.
    """
    # Generate header
    markdown = f"# 📊 {title}\n\n"
    
    # Add metadata section
    markdown += "## 📋 Overview\n\n"
    
    if description:
        markdown += f"{description}\n\n"
    else:
        markdown += f"This document contains a Mermaid diagram visualization.\n\n"
    
    if source_file:
        relative_source = source_file.relative_to(PROJECT_ROOT)
        markdown += f"**Source File:** `{relative_source}`\n\n"
    
    markdown += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown += "---\n\n"
    
    # Add diagram section
    markdown += "## 🎨 Diagram\n\n"
    markdown += "```mermaid\n"
    markdown += mermaid_content
    markdown += "\n```\n\n"
    
    # Add components section if we can extract subgraph info
    subgraph_pattern = r'subgraph\s+\w+\["([^"]+)"\]'
    subgraphs = re.findall(subgraph_pattern, mermaid_content)
    
    if subgraphs:
        markdown += "## 🔧 Components\n\n"
        for i, subgraph in enumerate(subgraphs, 1):
            markdown += f"{i}. **{subgraph}**\n"
        markdown += "\n"
    
    # Add usage section
    markdown += "## 📖 Usage\n\n"
    markdown += "This diagram can be viewed in:\n\n"
    markdown += "- **GitHub/GitLab**: Automatically rendered when viewing this file\n"
    markdown += "- **VS Code**: Install the 'Markdown Preview Mermaid Support' extension\n"
    markdown += "- **Obsidian**: Native Mermaid support\n"
    markdown += "- **Documentation Sites**: MkDocs, Docusaurus, etc. with Mermaid plugin\n\n"
    
    # Add related documents section
    markdown += "---\n\n"
    markdown += "## 🔗 Related Documents\n\n"
    markdown += "- [Documentation Index](docs/INDEX_MASTER_NAVIGATION_PT_BR.md)\n"
    markdown += "- [Diagrams Directory](docs/diagrams/)\n"
    markdown += "- [Project Strategy](docs/proj/strategy/)\n"
    markdown += "- [Roadmaps](docs/proj/roadmaps/)\n\n"
    
    return markdown


def determine_output_path(source_file: Path, output_dir: Path = None) -> Path:
    """
    Determine where to save the markdown file.
    
    Args:
        source_file: Source .mmd file path.
        output_dir: Preferred output directory.
        
    Returns:
        Path for the output markdown file.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    # If source is in docs/diagrams/, keep it there
    if "docs" in source_file.parts and "diagrams" in source_file.parts:
        return source_file.with_suffix('.md')
    
    # If source is in root, put it in docs/diagrams/
    if source_file.parent == PROJECT_ROOT:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / source_file.with_suffix('.md').name
    
    # Otherwise, place markdown next to source file
    return source_file.with_suffix('.md')


def convert_mmd_to_markdown(
    mmd_file: Path,
    output_path: Path = None,
    description: Optional[str] = None
) -> bool:
    """
    Convert a single .mmd file to markdown.
    
    Args:
        mmd_file: Path to .mmd file.
        output_path: Optional output path. If None, determined automatically.
        description: Optional description for the diagram.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        print(f"\n[+] Processing: {mmd_file.relative_to(PROJECT_ROOT)}")
        
        # Load content
        mermaid_content = load_mmd_content(mmd_file)
        if not mermaid_content:
            print(f"[!] Empty or invalid file: {mmd_file}")
            return False
        
        # Generate title
        title = extract_title_from_filename(mmd_file.stem)
        
        # Get description
        if not description:
            description = DESCRIPTIONS.get(mmd_file.stem)
            if not description:
                description = extract_description_from_content(mermaid_content)
        
        # Determine output path
        if output_path is None:
            output_path = determine_output_path(mmd_file)
        
        # Generate markdown
        markdown_content = generate_markdown_content(
            title=title,
            mermaid_content=mermaid_content,
            description=description,
            source_file=mmd_file
        )
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        relative_output = output_path.relative_to(PROJECT_ROOT)
        print(f"[OK] Generated: {relative_output}")
        return True
        
    except Exception as e:
        print(f"[!] Error converting {mmd_file}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main conversion function."""
    print("="*80)
    print("MERMAID TO MARKDOWN CONVERTER")
    print("="*80)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print("="*80)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all .mmd files
    mmd_files = find_mmd_files()
    
    if not mmd_files:
        print("[!] No .mmd files found in the project")
        return
    
    # Convert each file
    success_count = 0
    for mmd_file in mmd_files:
        if convert_mmd_to_markdown(mmd_file):
            success_count += 1
    
    # Summary
    print("\n" + "="*80)
    print(f"CONVERSION COMPLETE")
    print(f"Processed: {len(mmd_files)} file(s)")
    print(f"Successful: {success_count} file(s)")
    print(f"Failed: {len(mmd_files) - success_count} file(s)")
    print("="*80)
    
    if success_count > 0:
        print(f"\n✅ Markdown files generated in: {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")
        print("📖 View the files in your markdown viewer or on GitHub/GitLab")


if __name__ == "__main__":
    main()

