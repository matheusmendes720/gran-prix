"""
Comprehensive script to move ALL remaining files into their proper subfolders.
"""
import shutil
from pathlib import Path
import os
from typing import List, Tuple

BASE_DIR = Path(__file__).parent

# File organization mappings: (source_relative_path, destination_relative_path)
FILE_ORGANIZATIONS = [
    # Documentation files -> docs/
    ("*.md", "docs/"),
    ("README.md", "README.md"),  # Keep README in root
    
    # Python scripts -> backend/scripts/
    ("setup_directory_structure.py", "backend/scripts/setup_directory_structure.py"),
    ("setup_reports_archive.py", "backend/scripts/setup_reports_archive.py"),
    ("migrate_to_new_structure.py", "backend/scripts/migrate_to_new_structure.py"),
    ("organize_all_files.py", "backend/scripts/organize_all_files.py"),
    ("dashboard_app.py", "backend/scripts/dashboard_app.py"),
    ("nova_corrente_forecasting.py", "backend/scripts/nova_corrente_forecasting.py"),
    ("nova_corrente_forecasting_main.py", "backend/scripts/nova_corrente_forecasting_main.py"),
    ("test_forecasting_system.py", "backend/tests/test_forecasting_system.py"),
    ("verify_brazilian_integration.py", "backend/scripts/verify_brazilian_integration.py"),
    ("setup_and_run.py", "backend/scripts/setup_and_run.py"),
    ("run_dashboard.py", "backend/scripts/run_dashboard.py"),
    ("run_pipeline.py", "backend/scripts/run_pipeline.py"),
    
    # Configuration files -> config/
    ("config.yaml", "config/config.yaml"),
    ("kaggle.json", "config/kaggle.json"),
    ("requirements.txt", "backend/requirements.txt"),
    ("requirements_api.txt", "backend/requirements_api.txt"),
    ("requirements_forecasting.txt", "backend/requirements_forecasting.txt"),
    
    # Shell scripts -> backend/scripts/ or infrastructure/scripts/
    ("run_api.sh", "backend/scripts/run_api.sh"),
    ("run_dashboard.sh", "backend/scripts/run_dashboard.sh"),
    ("launch_dashboard.bat", "backend/scripts/launch_dashboard.bat"),
    
    # HTML files -> frontend/public/ or docs_html/
    ("web_dashboard.html", "frontend/public/web_dashboard.html"),
    
    # CSV sample files -> data/processed/samples/
    ("exemplo_reorder_point.csv", "data/processed/samples/exemplo_reorder_point.csv"),
    
    # Docker files -> infrastructure/docker/
    ("Dockerfile", "infrastructure/docker/Dockerfile.legacy"),
    
    # Results -> reports/results/
    ("results/", "reports/results/"),
]

# Patterns to move to specific directories
PATTERNS = {
    # All markdown docs (except README.md) -> docs/guides/ or docs/
    "*.md": "docs/guides/",
    # All Python scripts in root -> backend/scripts/
    "*.py": "backend/scripts/",
    # All JSON configs -> config/
    "*.json": "config/",
    # All YAML configs -> config/
    "*.yaml": "config/",
    "*.yml": "config/",
    # All HTML -> frontend/public/ or docs_html/
    "*.html": "frontend/public/",
    # All shell scripts -> backend/scripts/
    "*.sh": "backend/scripts/",
    "*.bat": "backend/scripts/",
    # All CSV -> data/processed/samples/
    "*.csv": "data/processed/samples/",
    # All txt files -> docs/guides/
    "*.txt": "docs/guides/",
}

# Files/directories to keep in root
KEEP_IN_ROOT = {
    "README.md",
    "README_REORGANIZATION.md",
    "PROJECT_REORGANIZATION_COMPLETE.md",
    "MIGRATION_STATUS.md",
    ".gitignore",
    ".git",
    "frontend",
    "backend",
    "shared",
    "infrastructure",
    "docs",
    "data",
    "models",
    "reports",
    "logs",
    "config",
    "scripts",  # Will organize later
    "src",  # Will organize later
    "demand_forecasting",  # Will organize later
    "backup_migration",
    "notebooks",
    "static",
    "templates",
    "docs_export",
    "docs_html",
    "tests",
    "docker-compose.yml",
    "setup_directory_structure.py",
    "setup_reports_archive.py",
    "migrate_to_new_structure.py",
    "organize_all_files.py",
}

def should_keep(file_path: Path) -> bool:
    """Check if file should stay in root."""
    name = file_path.name
    if name in KEEP_IN_ROOT:
        return True
    if any(name.startswith(keep) for keep in KEEP_IN_ROOT):
        return True
    return False

def organize_markdown_files():
    """Organize markdown documentation files."""
    organized = []
    
    # Find all markdown files in root
    for md_file in BASE_DIR.glob("*.md"):
        if should_keep(md_file):
            continue
        
        # Determine destination based on filename
        if "README" in md_file.name.upper():
            dest = BASE_DIR / "docs" / "guides" / md_file.name
        elif "MIGRATION" in md_file.name.upper() or "REORGANIZATION" in md_file.name.upper():
            dest = BASE_DIR / "docs" / md_file.name
        else:
            dest = BASE_DIR / "docs" / "guides" / md_file.name
        
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(md_file), str(dest))
            organized.append((md_file.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {md_file.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {md_file.name}: {e}")
    
    return organized

def organize_python_scripts():
    """Organize Python scripts."""
    organized = []
    
    for py_file in BASE_DIR.glob("*.py"):
        if should_keep(py_file):
            continue
        
        # Determine destination
        if "test" in py_file.name.lower():
            dest = BASE_DIR / "backend" / "tests" / py_file.name
        elif "setup" in py_file.name.lower() or "organize" in py_file.name.lower() or "migrate" in py_file.name.lower():
            dest = BASE_DIR / "backend" / "scripts" / py_file.name
        else:
            dest = BASE_DIR / "backend" / "scripts" / py_file.name
        
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(py_file), str(dest))
            organized.append((py_file.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {py_file.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {py_file.name}: {e}")
    
    return organized

def organize_config_files():
    """Organize configuration files."""
    organized = []
    
    # YAML files
    for yaml_file in BASE_DIR.glob("*.yaml"):
        if should_keep(yaml_file):
            continue
        dest = BASE_DIR / "config" / yaml_file.name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(yaml_file), str(dest))
            organized.append((yaml_file.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {yaml_file.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {yaml_file.name}: {e}")
    
    # JSON configs (except in node_modules, etc.)
    for json_file in BASE_DIR.glob("*.json"):
        if should_keep(json_file) or json_file.name in ["package.json", "package-lock.json", "tsconfig.json"]:
            continue
        dest = BASE_DIR / "config" / json_file.name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(json_file), str(dest))
            organized.append((json_file.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {json_file.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {json_file.name}: {e}")
    
    return organized

def organize_scripts():
    """Organize shell scripts."""
    organized = []
    
    for script in BASE_DIR.glob("*.sh"):
        dest = BASE_DIR / "backend" / "scripts" / script.name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(script), str(dest))
            organized.append((script.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {script.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {script.name}: {e}")
    
    for bat in BASE_DIR.glob("*.bat"):
        dest = BASE_DIR / "backend" / "scripts" / bat.name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(bat), str(dest))
            organized.append((bat.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {bat.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {bat.name}: {e}")
    
    return organized

def organize_html_files():
    """Organize HTML files."""
    organized = []
    
    for html_file in BASE_DIR.glob("*.html"):
        if should_keep(html_file):
            continue
        dest = BASE_DIR / "frontend" / "public" / html_file.name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(html_file), str(dest))
            organized.append((html_file.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {html_file.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {html_file.name}: {e}")
    
    return organized

def organize_csv_files():
    """Organize CSV sample files."""
    organized = []
    
    for csv_file in BASE_DIR.glob("*.csv"):
        dest = BASE_DIR / "data" / "processed" / "samples" / csv_file.name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(csv_file), str(dest))
            organized.append((csv_file.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {csv_file.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {csv_file.name}: {e}")
    
    return organized

def organize_requirements():
    """Organize requirements files."""
    organized = []
    
    for req_file in BASE_DIR.glob("requirements*.txt"):
        dest = BASE_DIR / "backend" / req_file.name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(req_file), str(dest))
            organized.append((req_file.name, str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: {req_file.name} -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move {req_file.name}: {e}")
    
    return organized

def organize_docker_files():
    """Organize Docker files."""
    organized = []
    
    if (BASE_DIR / "Dockerfile").exists():
        dest = BASE_DIR / "infrastructure" / "docker" / "Dockerfile.legacy"
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(BASE_DIR / "Dockerfile"), str(dest))
            organized.append(("Dockerfile", str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: Dockerfile -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move Dockerfile: {e}")
    
    return organized

def organize_results():
    """Organize results directory."""
    organized = []
    
    results_dir = BASE_DIR / "results"
    if results_dir.exists() and results_dir.is_dir():
        dest = BASE_DIR / "reports" / "results"
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                # Move contents
                for item in results_dir.iterdir():
                    shutil.move(str(item), str(dest / item.name))
            else:
                shutil.move(str(results_dir), str(dest))
            organized.append(("results/", str(dest.relative_to(BASE_DIR))))
            print(f"[OK] Moved: results/ -> {dest.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"[ERROR] Failed to move results/: {e}")
    
    return organized

def organize_all(dry_run: bool = False):
    """Organize all files."""
    if dry_run:
        print("[DRY RUN] Would organize files...")
        # Show what would be organized
        print("\nMarkdown files to move:")
        for md_file in BASE_DIR.glob("*.md"):
            if not should_keep(md_file):
                print(f"  - {md_file.name} -> docs/guides/")
        print("\nPython scripts to move:")
        for py_file in BASE_DIR.glob("*.py"):
            if not should_keep(py_file):
                print(f"  - {py_file.name} -> backend/scripts/")
        return
    
    print(f"\n{'='*60}")
    print("Organizing ALL Files into Proper Subfolders")
    print(f"{'='*60}\n")
    
    all_organized = []
    
    # Organize by type
    print("\n[1] Organizing Markdown files...")
    all_organized.extend(organize_markdown_files())
    
    print("\n[2] Organizing Python scripts...")
    all_organized.extend(organize_python_scripts())
    
    print("\n[3] Organizing Configuration files...")
    all_organized.extend(organize_config_files())
    
    print("\n[4] Organizing Shell scripts...")
    all_organized.extend(organize_scripts())
    
    print("\n[5] Organizing HTML files...")
    all_organized.extend(organize_html_files())
    
    print("\n[6] Organizing CSV files...")
    all_organized.extend(organize_csv_files())
    
    print("\n[7] Organizing Requirements files...")
    all_organized.extend(organize_requirements())
    
    print("\n[8] Organizing Docker files...")
    all_organized.extend(organize_docker_files())
    
    print("\n[9] Organizing Results directory...")
    all_organized.extend(organize_results())
    
    print(f"\n{'='*60}")
    print(f"Organized {len(all_organized)} files/directories")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Organize all files into subfolders")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving")
    
    args = parser.parse_args()
    
    organize_all(dry_run=args.dry_run)
    
    if not args.dry_run:
        print("[SUCCESS] All files organized!")
    else:
        print("[DRY RUN] Preview complete. Run without --dry-run to organize.")

