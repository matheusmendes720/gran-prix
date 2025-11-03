"""
Deep cleanup - Move EVERY file and directory into proper subfolders.
No files left in root except essential ones.
"""
import shutil
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent

# Essential files to keep in root
ESSENTIAL_ROOT_FILES = {
    "README.md",
    "README_REORGANIZATION.md",
    "PROJECT_REORGANIZATION_COMPLETE.md",
    "MIGRATION_STATUS.md",
    "COMPLETE_REORGANIZATION_SUMMARY.md",
    "UPDATE_README.py",
    "deep_cleanup.py",
    "docker-compose.yml",
    ".gitignore",
    ".dockerignore",
    ".git",
}

# Essential directories to keep in root
ESSENTIAL_ROOT_DIRS = {
    "frontend",
    "backend",
    "shared",
    "infrastructure",
    "docs",
    "config",
    "data",
    "models",
    "reports",
    "logs",
    "backup_migration",
    "notebooks",
    ".git",
}

def deep_cleanup():
    """Move everything not essential to proper subfolders."""
    print(f"\n{'='*60}")
    print("DEEP CLEANUP - Organizing ALL Files")
    print(f"{'='*60}\n")
    
    moved = []
    
    # Get all files in root
    root_files = [f for f in BASE_DIR.iterdir() if f.is_file() and f.name not in ESSENTIAL_ROOT_FILES]
    
    print(f"[1] Found {len(root_files)} files to organize...")
    
    # Organize files by extension
    for file_path in root_files:
        name = file_path.name
        ext = file_path.suffix.lower()
        
        try:
            if ext == ".md":
                # Markdown files -> docs/guides/ (except special ones)
                if "MIGRATION" in name.upper() or "REORGANIZATION" in name.upper() or "COMPLETE" in name.upper():
                    dest = BASE_DIR / "docs" / name
                else:
                    dest = BASE_DIR / "docs" / "guides" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> {dest.relative_to(BASE_DIR)}")
                
            elif ext == ".py":
                # Python files -> backend/scripts/
                dest = BASE_DIR / "backend" / "scripts" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> backend/scripts/")
                
            elif ext in [".txt", ".log"]:
                # Text files -> docs/guides/ or logs/
                dest = BASE_DIR / "docs" / "guides" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> docs/guides/")
                
            elif ext in [".json", ".yaml", ".yml"]:
                # Config files -> config/
                dest = BASE_DIR / "config" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> config/")
                
            elif ext in [".html", ".css"]:
                # HTML/CSS -> frontend/public/
                dest = BASE_DIR / "frontend" / "public" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> frontend/public/")
                
            elif ext in [".sh", ".bat", ".ps1"]:
                # Scripts -> backend/scripts/
                dest = BASE_DIR / "backend" / "scripts" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> backend/scripts/")
                
            elif ext == ".csv":
                # CSV -> data/processed/samples/
                dest = BASE_DIR / "data" / "processed" / "samples" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> data/processed/samples/")
                
            else:
                # Unknown files -> docs/misc/
                dest = BASE_DIR / "docs" / "misc" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> docs/misc/")
                
        except Exception as e:
            print(f"[ERROR] Failed to move {name}: {e}")
    
    # Organize remaining directories
    print(f"\n[2] Organizing remaining directories...")
    root_dirs = [d for d in BASE_DIR.iterdir() if d.is_dir() and d.name not in ESSENTIAL_ROOT_DIRS]
    
    for dir_path in root_dirs:
        name = dir_path.name
        
        try:
            # demand_forecasting/ -> Move contents to backend/ml/ (if exists)
            if name == "demand_forecasting":
                print(f"[INFO] demand_forecasting/ found - contents already migrated, can be removed")
                # Keep for now as backup
                
            # src/ -> Move remaining contents
            elif name == "src":
                print(f"[INFO] src/ found - checking remaining files...")
                # Should be mostly empty now
                if any(dir_path.iterdir()):
                    print(f"[INFO] src/ still has files - manual review needed")
                
            # scripts/ -> Move remaining to backend/scripts/
            elif name == "scripts":
                backend_scripts = BASE_DIR / "backend" / "scripts"
                backend_scripts.mkdir(parents=True, exist_ok=True)
                for item in dir_path.iterdir():
                    if item.is_file():
                        dest = backend_scripts / item.name
                        if not dest.exists():
                            shutil.move(str(item), str(dest))
                            moved.append((f"{name}/{item.name}", f"backend/scripts/"))
                            print(f"[OK] Moved: {name}/{item.name} -> backend/scripts/")
                # Remove if empty
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"[OK] Removed empty: {name}/")
                    
            # tests/ -> Move to backend/tests/
            elif name == "tests":
                backend_tests = BASE_DIR / "backend" / "tests"
                backend_tests.mkdir(parents=True, exist_ok=True)
                for item in dir_path.iterdir():
                    dest = backend_tests / item.name
                    if not dest.exists():
                        shutil.move(str(item), str(dest))
                        moved.append((f"{name}/{item.name}", f"backend/tests/"))
                        print(f"[OK] Moved: {name}/{item.name} -> backend/tests/")
                # Remove if empty
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"[OK] Removed empty: {name}/")
                    
            # templates/ -> Move to frontend/public/templates/
            elif name == "templates":
                dest = BASE_DIR / "frontend" / "public" / "templates"
                if not dest.exists():
                    shutil.move(str(dir_path), str(dest))
                    moved.append((name, str(dest.relative_to(BASE_DIR))))
                    print(f"[OK] Moved: {name}/ -> frontend/public/")
                    
            # static/ -> Move to frontend/public/static/
            elif name == "static":
                dest = BASE_DIR / "frontend" / "public" / "static"
                if not dest.exists():
                    shutil.move(str(dir_path), str(dest))
                    moved.append((name, str(dest.relative_to(BASE_DIR))))
                    print(f"[OK] Moved: {name}/ -> frontend/public/")
                    
            # docs_html/ -> Move to frontend/public/docs_html/
            elif name == "docs_html":
                dest = BASE_DIR / "frontend" / "public" / "docs_html"
                if not dest.exists():
                    try:
                        shutil.move(str(dir_path), str(dest))
                        moved.append((name, str(dest.relative_to(BASE_DIR))))
                        print(f"[OK] Moved: {name}/ -> frontend/public/")
                    except:
                        print(f"[WARN] Could not move {name}/ - may be in use")
                        
            # Unknown directories -> docs/misc/
            else:
                dest = BASE_DIR / "docs" / "misc" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dir_path), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name}/ -> docs/misc/")
                
        except Exception as e:
            print(f"[ERROR] Failed to organize {name}/: {e}")
    
    print(f"\n{'='*60}")
    print(f"Moved {len(moved)} items")
    print(f"{'='*60}\n")
    
    return moved

if __name__ == "__main__":
    moved = deep_cleanup()
    print(f"\n[SUCCESS] Deep cleanup complete! Moved {len(moved)} items.")





