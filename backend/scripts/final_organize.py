"""
Final organization script - Move remaining files and directories.
"""
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

def organize_remaining():
    """Organize all remaining files and directories."""
    print(f"\n{'='*60}")
    print("FINAL ORGANIZATION")
    print(f"{'='*60}\n")
    
    moved = []
    
    # Move remaining files in root
    print("[1] Moving remaining root files...")
    root_files = [
        ("UPDATE_README.py", "backend/scripts/"),
        ("deep_cleanup.py", "backend/scripts/"),
        ("COMPLETE_REORGANIZATION_SUMMARY.md", "docs/"),
        ("MIGRATION_STATUS.md", "docs/"),
        ("PROJECT_REORGANIZATION_COMPLETE.md", "docs/"),
        ("README_REORGANIZATION.md", "docs/"),
        ("ROOT_CLEANUP_STATUS.md", "docs/"),
    ]
    
    for filename, dest_dir in root_files:
        source = BASE_DIR / filename
        if source.exists():
            dest = BASE_DIR / dest_dir / filename
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(dest))
                moved.append(filename)
                print(f"[OK] Moved: {filename} -> {dest_dir}")
            except Exception as e:
                print(f"[ERROR] Failed to move {filename}: {e}")
    
    # Organize remaining directories
    print("\n[2] Organizing remaining directories...")
    
    # demand_forecasting/ - Keep as legacy (already migrated)
    demand_dir = BASE_DIR / "demand_forecasting"
    if demand_dir.exists():
        print(f"[INFO] demand_forecasting/ exists - keep as legacy backup or delete manually")
    
    # src/ - Move remaining files
    src_dir = BASE_DIR / "src"
    if src_dir.exists():
        # Move any remaining Python files
        for py_file in src_dir.rglob("*.py"):
            if "pipeline" in str(py_file.parent):
                dest = BASE_DIR / "backend" / "pipelines" / "data_processing" / py_file.name
            elif "validation" in str(py_file.parent):
                dest = BASE_DIR / "backend" / "pipelines" / "monitoring" / py_file.name
            else:
                dest = BASE_DIR / "backend" / "scripts" / py_file.name
            
            if not dest.exists():
                try:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(py_file), str(dest))
                    moved.append(f"src/{py_file.name}")
                    print(f"[OK] Moved: src/{py_file.name} -> {dest.relative_to(BASE_DIR)}")
                except Exception as e:
                    print(f"[ERROR] Failed to move {py_file.name}: {e}")
        
        # Remove if empty
        try:
            if not any(src_dir.rglob("*")):
                src_dir.rmdir()
                print(f"[OK] Removed empty: src/")
        except:
            pass
    
    # scripts/ - Move remaining files
    scripts_dir = BASE_DIR / "scripts"
    if scripts_dir.exists():
        backend_scripts = BASE_DIR / "backend" / "scripts"
        for script_file in scripts_dir.iterdir():
            if script_file.is_file() and not (backend_scripts / script_file.name).exists():
                try:
                    shutil.move(str(script_file), str(backend_scripts / script_file.name))
                    moved.append(f"scripts/{script_file.name}")
                    print(f"[OK] Moved: scripts/{script_file.name} -> backend/scripts/")
                except Exception as e:
                    print(f"[ERROR] Failed to move {script_file.name}: {e}")
        
        # Remove if empty
        try:
            if not any(scripts_dir.iterdir()):
                scripts_dir.rmdir()
                print(f"[OK] Removed empty: scripts/")
        except:
            pass
    
    print(f"\n{'='*60}")
    print(f"Moved {len(moved)} items")
    print(f"{'='*60}\n")
    
    return moved

if __name__ == "__main__":
    moved = organize_remaining()
    print(f"\n[SUCCESS] Final organization complete! Moved {len(moved)} items.")
    print("\nRoot directory should now be clean!")





