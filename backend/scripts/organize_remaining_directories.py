"""
Organize remaining directories (scripts/, src/, demand_forecasting/) into proper structure.
"""
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Directories to organize
DIRECTORIES_TO_ORGANIZE = [
    # scripts/ -> backend/scripts/ (if not already migrated)
    ("scripts", "backend/scripts"),
    
    # src/pipeline/ -> backend/pipelines/ (if not already migrated)
    ("src/pipeline", "backend/pipelines"),
    ("src/scrapy", "backend/pipelines/data_ingestion/scrapy"),
    ("src/utils", "backend/pipelines/utils"),
    ("src/validation", "backend/pipelines/monitoring"),
    ("src/visualization", "frontend/public/visualizations"),
    
    # demand_forecasting/ -> backend/ml/ (if not already migrated)
    ("demand_forecasting/models", "backend/ml/models"),
    ("demand_forecasting/data", "backend/ml/data"),
    ("demand_forecasting/utils", "backend/ml/utils"),
    ("demand_forecasting/validation", "backend/ml/evaluation"),
    ("demand_forecasting/inventory", "backend/app/core/inventory"),
    ("demand_forecasting/reporting", "backend/ml/evaluation/reporting"),
]

def organize_directory(source_rel: str, dest_rel: str):
    """Organize a directory."""
    source = BASE_DIR / source_rel
    dest = BASE_DIR / dest_rel
    
    if not source.exists():
        print(f"[SKIP] Source not found: {source_rel}")
        return False
    
    # Check if destination already exists
    if dest.exists():
        print(f"[SKIP] Destination exists: {dest_rel}")
        # Maybe merge contents?
        return False
    
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # If source is a file, copy it
        if source.is_file():
            shutil.copy2(str(source), str(dest))
            print(f"[OK] Copied file: {source_rel} -> {dest_rel}")
        else:
            # Move directory
            shutil.move(str(source), str(dest))
            print(f"[OK] Moved directory: {source_rel} -> {dest_rel}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to organize {source_rel}: {e}")
        return False

def move_remaining_files():
    """Move remaining files from old directories."""
    moved = []
    
    # Move scripts that weren't migrated yet
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
                    print(f"[ERROR] Failed to move scripts/{script_file.name}: {e}")
    
    # Move src/visualization if it has files
    src_viz = BASE_DIR / "src" / "visualization"
    if src_viz.exists():
        for item in src_viz.iterdir():
            if item.is_file() and not (BASE_DIR / "frontend" / "public" / item.name).exists():
                try:
                    shutil.move(str(item), str(BASE_DIR / "frontend" / "public" / item.name))
                    moved.append(f"src/visualization/{item.name}")
                    print(f"[OK] Moved: src/visualization/{item.name} -> frontend/public/")
                except Exception as e:
                    print(f"[ERROR] Failed to move {item.name}: {e}")
    
    return moved

def organize_all():
    """Organize all remaining directories."""
    print(f"\n{'='*60}")
    print("Organizing Remaining Directories")
    print(f"{'='*60}\n")
    
    organized = []
    
    # Organize main directories
    for source_rel, dest_rel in DIRECTORIES_TO_ORGANIZE:
        if organize_directory(source_rel, dest_rel):
            organized.append((source_rel, dest_rel))
    
    # Move remaining files
    print("\n[Moving remaining files...]")
    moved = move_remaining_files()
    
    print(f"\n{'='*60}")
    print(f"Organized {len(organized)} directories")
    print(f"Moved {len(moved)} additional files")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    organize_all()
    print("[SUCCESS] Remaining directories organized!")

