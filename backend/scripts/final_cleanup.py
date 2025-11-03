"""
Final cleanup script - Move remaining files and organize everything.
"""
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent

def cleanup_remaining_files():
    """Clean up all remaining files in root."""
    print(f"\n{'='*60}")
    print("Final Cleanup - Organizing Remaining Files")
    print(f"{'='*60}\n")
    
    moved = []
    
    # Move utility scripts to backend/scripts/
    utility_scripts = [
        "migrate_to_new_structure.py",
        "organize_all_files.py",
        "organize_remaining_directories.py",
        "setup_directory_structure.py",
        "setup_reports_archive.py",
        "final_cleanup.py",
    ]
    
    print("[1] Moving utility scripts...")
    for script in utility_scripts:
        source = BASE_DIR / script
        if source.exists():
            dest = BASE_DIR / "backend" / "scripts" / script
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(dest))
                moved.append(script)
                print(f"[OK] Moved: {script} -> backend/scripts/")
            except Exception as e:
                print(f"[ERROR] Failed to move {script}: {e}")
    
    # Move remaining documentation
    print("\n[2] Moving remaining documentation...")
    docs_to_move = [
        ("FINAL_FILE_ORGANIZATION_COMPLETE.md", "docs/FINAL_FILE_ORGANIZATION_COMPLETE.md"),
        ("FINAL_SUCCESS_REPORT.txt", "docs/archives/success/pipeline/2025/2025-11-01/FINAL_SUCCESS_REPORT.txt"),
    ]
    
    for source_name, dest_rel in docs_to_move:
        source = BASE_DIR / source_name
        if source.exists():
            dest = BASE_DIR / dest_rel
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(dest))
                moved.append(source_name)
                print(f"[OK] Moved: {source_name} -> {dest_rel}")
            except Exception as e:
                print(f"[ERROR] Failed to move {source_name}: {e}")
    
    # Move config.yaml if duplicate
    print("\n[3] Checking config files...")
    config_yaml = BASE_DIR / "config.yaml"
    config_dir_yaml = BASE_DIR / "config" / "config.yaml"
    if config_yaml.exists() and not config_dir_yaml.exists():
        try:
            shutil.move(str(config_yaml), str(config_dir_yaml))
            moved.append("config.yaml")
            print(f"[OK] Moved: config.yaml -> config/")
        except Exception as e:
            print(f"[ERROR] Failed to move config.yaml: {e}")
    
    # Move remaining directories
    print("\n[4] Cleaning up remaining directories...")
    
    # Move templates to frontend/public/templates/
    templates_dir = BASE_DIR / "templates"
    if templates_dir.exists():
        dest = BASE_DIR / "frontend" / "public" / "templates"
        try:
            if dest.exists():
                # Merge contents
                for item in templates_dir.iterdir():
                    shutil.move(str(item), str(dest / item.name))
                templates_dir.rmdir()
            else:
                shutil.move(str(templates_dir), str(dest))
            moved.append("templates/")
            print(f"[OK] Moved: templates/ -> frontend/public/")
        except Exception as e:
            print(f"[ERROR] Failed to move templates/: {e}")
    
    # Move static to frontend/public/static/
    static_dir = BASE_DIR / "static"
    if static_dir.exists():
        dest = BASE_DIR / "frontend" / "public" / "static"
        try:
            if dest.exists():
                # Merge contents
                for item in static_dir.iterdir():
                    shutil.move(str(item), str(dest / item.name))
                static_dir.rmdir()
            else:
                shutil.move(str(static_dir), str(dest))
            moved.append("static/")
            print(f"[OK] Moved: static/ -> frontend/public/")
        except Exception as e:
            print(f"[ERROR] Failed to move static/: {e}")
    
    # Move docs_export to backend/scripts/docs_export/
    docs_export = BASE_DIR / "docs_export"
    if docs_export.exists():
        dest = BASE_DIR / "backend" / "scripts" / "docs_export"
        try:
            shutil.move(str(docs_export), str(dest))
            moved.append("docs_export/")
            print(f"[OK] Moved: docs_export/ -> backend/scripts/")
        except Exception as e:
            print(f"[ERROR] Failed to move docs_export/: {e}")
    
    # Move docs_html to frontend/public/docs_html/
    docs_html = BASE_DIR / "docs_html"
    if docs_html.exists():
        dest = BASE_DIR / "frontend" / "public" / "docs_html"
        try:
            shutil.move(str(docs_html), str(dest))
            moved.append("docs_html/")
            print(f"[OK] Moved: docs_html/ -> frontend/public/")
        except Exception as e:
            print(f"[ERROR] Failed to move docs_html/: {e}")
    
    # Move remaining src/ files
    print("\n[5] Organizing remaining src/ files...")
    src_dir = BASE_DIR / "src"
    if src_dir.exists():
        # Move pipeline files
        src_pipeline = src_dir / "pipeline"
        if src_pipeline.exists():
            dest = BASE_DIR / "backend" / "pipelines" / "data_processing"
            try:
                for item in src_pipeline.iterdir():
                    if item.is_file() and not (dest / item.name).exists():
                        shutil.move(str(item), str(dest / item.name))
                        print(f"[OK] Moved: src/pipeline/{item.name} -> backend/pipelines/data_processing/")
            except Exception as e:
                print(f"[ERROR] Failed to move src/pipeline files: {e}")
        
        # Move validation files
        src_validation = src_dir / "validation"
        if src_validation.exists():
            dest = BASE_DIR / "backend" / "pipelines" / "monitoring"
            try:
                for item in src_validation.iterdir():
                    if item.is_file() and not (dest / item.name).exists():
                        shutil.move(str(item), str(dest / item.name))
                        print(f"[OK] Moved: src/validation/{item.name} -> backend/pipelines/monitoring/")
            except Exception as e:
                print(f"[ERROR] Failed to move src/validation files: {e}")
    
    # Move remaining scripts/ files
    print("\n[6] Organizing remaining scripts/ files...")
    scripts_dir = BASE_DIR / "scripts"
    if scripts_dir.exists():
        backend_scripts = BASE_DIR / "backend" / "scripts"
        backend_scripts.mkdir(parents=True, exist_ok=True)
        
        for script_file in scripts_dir.glob("*.py"):
            if not (backend_scripts / script_file.name).exists():
                try:
                    shutil.move(str(script_file), str(backend_scripts / script_file.name))
                    moved.append(f"scripts/{script_file.name}")
                    print(f"[OK] Moved: scripts/{script_file.name} -> backend/scripts/")
                except Exception as e:
                    print(f"[ERROR] Failed to move {script_file.name}: {e}")
    
    # Move remaining tests/
    print("\n[7] Organizing remaining tests/ files...")
    tests_dir = BASE_DIR / "tests"
    if tests_dir.exists():
        backend_tests = BASE_DIR / "backend" / "tests"
        backend_tests.mkdir(parents=True, exist_ok=True)
        
        for test_file in tests_dir.iterdir():
            if test_file.is_file():
                dest = backend_tests / test_file.name
                if not dest.exists():
                    try:
                        shutil.move(str(test_file), str(dest))
                        moved.append(f"tests/{test_file.name}")
                        print(f"[OK] Moved: tests/{test_file.name} -> backend/tests/")
                    except Exception as e:
                        print(f"[ERROR] Failed to move {test_file.name}: {e}")
    
    # Move remaining demand_forecasting/ files
    print("\n[8] Organizing remaining demand_forecasting/ files...")
    demand_forecasting_dir = BASE_DIR / "demand_forecasting"
    if demand_forecasting_dir.exists():
        # Check if files exist that weren't migrated
        for item in demand_forecasting_dir.rglob("*.py"):
            # Already migrated files should not be here
            print(f"[INFO] Found: {item.relative_to(BASE_DIR)} - may need manual review")
    
    print(f"\n{'='*60}")
    print(f"Moved {len(moved)} items")
    print(f"{'='*60}\n")
    
    return moved

if __name__ == "__main__":
    moved = cleanup_remaining_files()
    print(f"\n[SUCCESS] Final cleanup complete! Moved {len(moved)} items.")





