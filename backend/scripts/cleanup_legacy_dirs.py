"""
Clean up legacy directories - Move remaining files and remove empty dirs.
"""
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

def cleanup_legacy_directories():
    """Clean up all legacy directories."""
    print(f"\n{'='*60}")
    print("CLEANUP LEGACY DIRECTORIES")
    print(f"{'='*60}\n")
    
    moved = []
    removed = []
    
    # 1. scripts/ directory
    scripts_dir = BASE_DIR / "scripts"
    if scripts_dir.exists():
        print("[1] Cleaning scripts/ directory...")
        backend_scripts = BASE_DIR / "backend" / "scripts"
        backend_scripts.mkdir(parents=True, exist_ok=True)
        
        for item in scripts_dir.iterdir():
            if item.is_file():
                dest = backend_scripts / item.name
                if not dest.exists():
                    try:
                        shutil.move(str(item), str(dest))
                        moved.append(f"scripts/{item.name}")
                        print(f"[OK] Moved: scripts/{item.name} -> backend/scripts/")
                    except Exception as e:
                        print(f"[ERROR] Failed to move {item.name}: {e}")
        
        # Remove if empty
        try:
            if not any(scripts_dir.iterdir()):
                scripts_dir.rmdir()
                removed.append("scripts/")
                print(f"[OK] Removed empty: scripts/")
        except:
            print(f"[INFO] scripts/ not empty - keeping")
    
    # 2. src/ directory
    src_dir = BASE_DIR / "src"
    if src_dir.exists():
        print("\n[2] Cleaning src/ directory...")
        
        for item in src_dir.rglob("*.py"):
            # Determine destination
            if "pipeline" in str(item.parent):
                dest = BASE_DIR / "backend" / "pipelines" / "data_processing" / item.name
            elif "validation" in str(item.parent):
                dest = BASE_DIR / "backend" / "pipelines" / "monitoring" / item.name
            else:
                dest = BASE_DIR / "backend" / "scripts" / item.name
            
            if not dest.exists():
                try:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(dest))
                    moved.append(f"src/{item.relative_to(src_dir)}")
                    print(f"[OK] Moved: src/{item.name} -> {dest.relative_to(BASE_DIR)}")
                except Exception as e:
                    print(f"[ERROR] Failed to move {item.name}: {e}")
        
        # Remove if empty
        try:
            if not any(src_dir.rglob("*")):
                src_dir.rmdir()
                removed.append("src/")
                print(f"[OK] Removed empty: src/")
        except:
            print(f"[INFO] src/ not empty - keeping")
    
    # 3. demand_forecasting/ directory (legacy - keep or move)
    demand_dir = BASE_DIR / "demand_forecasting"
    if demand_dir.exists():
        print("\n[3] demand_forecasting/ directory (legacy)...")
        print(f"[INFO] demand_forecasting/ exists - files already migrated")
        print(f"[INFO] Can be kept as legacy backup or deleted manually")
        print(f"[INFO] Contents are in backup_migration/demand_forecasting/")
    
    # 4. docs_html/ directory
    docs_html = BASE_DIR / "docs_html"
    if docs_html.exists():
        print("\n[4] Cleaning docs_html/ directory...")
        if not any(docs_html.iterdir()):
            try:
                docs_html.rmdir()
                removed.append("docs_html/")
                print(f"[OK] Removed empty: docs_html/")
            except:
                print(f"[INFO] docs_html/ not empty or in use")
        else:
            # Move to frontend/public/
            dest = BASE_DIR / "frontend" / "public" / "docs_html"
            try:
                if dest.exists():
                    # Merge
                    for item in docs_html.iterdir():
                        shutil.move(str(item), str(dest / item.name))
                    docs_html.rmdir()
                else:
                    shutil.move(str(docs_html), str(dest))
                moved.append("docs_html/")
                print(f"[OK] Moved: docs_html/ -> frontend/public/")
            except Exception as e:
                print(f"[ERROR] Failed to move docs_html/: {e}")
    
    # 5. Move CLEAN_ROOT_FINAL.md and PROJECT_CLEAN_COMPLETE.md to docs/
    print("\n[5] Moving final documentation...")
    final_docs = [
        "CLEAN_ROOT_FINAL.md",
        "PROJECT_CLEAN_COMPLETE.md",
    ]
    
    for doc_name in final_docs:
        doc_file = BASE_DIR / doc_name
        if doc_file.exists():
            dest = BASE_DIR / "docs" / doc_name
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(doc_file), str(dest))
                moved.append(doc_name)
                print(f"[OK] Moved: {doc_name} -> docs/")
            except Exception as e:
                print(f"[ERROR] Failed to move {doc_name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Moved {len(moved)} items")
    print(f"Removed {len(removed)} empty directories")
    print(f"{'='*60}\n")
    
    return moved, removed

if __name__ == "__main__":
    moved, removed = cleanup_legacy_directories()
    print(f"\n[SUCCESS] Legacy cleanup complete!")
    print(f"Moved {len(moved)} items, removed {len(removed)} directories")





