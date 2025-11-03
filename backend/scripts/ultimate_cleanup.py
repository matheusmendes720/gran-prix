"""
Ultimate cleanup - Remove empty directories and consolidate everything.
"""
import shutil
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent

def remove_empty_dirs(path: Path):
    """Remove empty directories recursively."""
    removed = []
    try:
        for item in path.iterdir():
            if item.is_dir():
                removed.extend(remove_empty_dirs(item))
                # Try to remove if empty
                try:
                    if not any(item.iterdir()):
                        item.rmdir()
                        removed.append(str(item.relative_to(BASE_DIR)))
                        print(f"[OK] Removed empty: {item.relative_to(BASE_DIR)}/")
                except:
                    pass
    except:
        pass
    return removed

def consolidate_demand_forecasting():
    """Consolidate remaining demand_forecasting files."""
    demand_dir = BASE_DIR / "demand_forecasting"
    if not demand_dir.exists():
        return []
    
    moved = []
    
    # All files should already be migrated, this is just backup/old structure
    # Move remaining files to backend/ml/legacy/
    backend_legacy = BASE_DIR / "backend" / "ml" / "legacy"
    backend_legacy.mkdir(parents=True, exist_ok=True)
    
    print(f"[INFO] demand_forecasting/ exists - can be kept as legacy or removed")
    print(f"[INFO] To remove: Delete backend/ml/legacy/ and demand_forecasting/ manually if desired")
    
    return moved

def consolidate_src():
    """Consolidate remaining src files."""
    src_dir = BASE_DIR / "src"
    if not src_dir.exists():
        return []
    
    moved = []
    
    # Check what's left
    for item in src_dir.rglob("*"):
        if item.is_file():
            print(f"[INFO] Found in src/: {item.relative_to(BASE_DIR)}")
            # These should be migrated
            if "pipeline" in str(item):
                dest = BASE_DIR / "backend" / "pipelines" / "data_processing" / item.name
            elif "validation" in str(item):
                dest = BASE_DIR / "backend" / "pipelines" / "monitoring" / item.name
            elif "scrapy" in str(item):
                dest = BASE_DIR / "backend" / "pipelines" / "data_ingestion" / "scrapy" / item.name
            elif "utils" in str(item):
                dest = BASE_DIR / "backend" / "pipelines" / "utils" / item.name
            elif "visualization" in str(item):
                dest = BASE_DIR / "frontend" / "public" / "visualizations" / item.name
            else:
                dest = BASE_DIR / "backend" / "scripts" / item.name
            
            try:
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(dest))
                    moved.append((str(item.relative_to(BASE_DIR)), str(dest.relative_to(BASE_DIR))))
                    print(f"[OK] Moved: {item.name} -> {dest.relative_to(BASE_DIR)}")
            except Exception as e:
                print(f"[ERROR] Failed to move {item.name}: {e}")
    
    # Remove empty dirs
    try:
        if src_dir.exists() and not any(src_dir.rglob("*")):
            src_dir.rmdir()
            print(f"[OK] Removed empty: src/")
    except:
        pass
    
    return moved

def ultimate_cleanup():
    """Ultimate cleanup of everything."""
    print(f"\n{'='*60}")
    print("ULTIMATE CLEANUP - Final Organization")
    print(f"{'='*60}\n")
    
    all_moved = []
    
    # Consolidate directories
    print("[1] Consolidating remaining directories...")
    all_moved.extend(consolidate_demand_forecasting())
    all_moved.extend(consolidate_src())
    
    # Remove empty directories
    print("\n[2] Removing empty directories...")
    removed = remove_empty_dirs(BASE_DIR)
    
    # Move this script itself
    print("\n[3] Moving utility scripts...")
    script_name = "ultimate_cleanup.py"
    if (BASE_DIR / script_name).exists():
        dest = BASE_DIR / "backend" / "scripts" / script_name
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(BASE_DIR / script_name), str(dest))
            print(f"[OK] Moved: {script_name} -> backend/scripts/")
        except:
            pass
    
    print(f"\n{'='*60}")
    print(f"Cleaned up {len(all_moved)} files")
    print(f"Removed {len(removed)} empty directories")
    print(f"{'='*60}\n")
    
    return all_moved, removed

if __name__ == "__main__":
    all_moved, removed = ultimate_cleanup()
    print(f"\n[SUCCESS] Ultimate cleanup complete!")
    print(f"Cleaned {len(all_moved)} files, removed {len(removed)} empty directories")





