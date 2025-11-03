"""
Fix Math Docs Organization
Move all math docs back to docs/mathematics/ with current structure,
removing duplicates from misc/ and documentation/ folders.
"""
import shutil
from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).parent.parent.parent
docs_dir = BASE_DIR / "docs"

# Math files that should be in mathematics/ (not elsewhere)
# Map: {filename: proper_subfolder}
MATH_FILES_MAP = {
    # Advanced Theory (03_advanced_theory/)
    "MATH_ADVANCED_THEORY_EXPANSION.md": "03_advanced_theory",
    "MATH_NUMERICAL_METHODS.md": "03_advanced_theory",
    "MATH_PROOFS_AND_DERIVATIONS.md": "03_advanced_theory",
    
    # Implementations (02_implementations/)
    "MATH_ADVANCED_PYTHON_IMPLEMENTATIONS.md": "02_implementations",
    
    # Examples (04_examples_and_practice/)
    "MATH_SOLVED_EXAMPLES.md": "04_examples_and_practice",
    
    # Index (00_index_and_navigation/)
    "MATH_DOCS_INDEX.md": "00_index_and_navigation",
    "MATH_DOCS_SUMMARY_FINAL.md": "00_index_and_navigation",
}

def check_and_remove_duplicates():
    """Check for duplicates and remove them if math file exists in proper location."""
    print(f"\n{'='*60}")
    print("Fixing Math Docs Organization")
    print(f"{'='*60}\n")
    
    math_dir = docs_dir / "mathematics"
    misc_dir = docs_dir / "misc"
    doc_dir = docs_dir / "documentation"
    
    moved = []
    removed = []
    skipped = []
    
    # Check misc/ folder
    print("\n[1] Checking docs/misc/ for math files...")
    for filename, subfolder in MATH_FILES_MAP.items():
        misc_file = misc_dir / filename
        math_file = math_dir / subfolder / filename
        
        if misc_file.exists():
            if math_file.exists():
                # Duplicate - remove from misc
                misc_file.unlink()
                removed.append(f"misc/{filename} (duplicate)")
                print(f"  [REMOVED] misc/{filename} (duplicate - exists in mathematics/{subfolder}/)")
            else:
                # Move to proper location
                math_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(misc_file), str(math_file))
                moved.append(f"misc/{filename} -> mathematics/{subfolder}/")
                print(f"  [MOVED] misc/{filename} -> mathematics/{subfolder}/")
        elif math_file.exists():
            skipped.append(f"mathematics/{subfolder}/{filename} (already in place)")
    
    # Check documentation/ folder
    print("\n[2] Checking docs/documentation/ for math files...")
    for filename, subfolder in MATH_FILES_MAP.items():
        # Check all subdirectories in documentation/
        for doc_subdir in doc_dir.rglob(filename):
            math_file = math_dir / subfolder / filename
            
            if doc_subdir.exists() and doc_subdir.is_file():
                if math_file.exists():
                    # Duplicate - remove
                    doc_subdir.unlink()
                    removed.append(f"{doc_subdir.relative_to(docs_dir)} (duplicate)")
                    print(f"  [REMOVED] {doc_subdir.relative_to(docs_dir)} (duplicate)")
                else:
                    # Move to proper location
                    math_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(doc_subdir), str(math_file))
                    moved.append(f"{doc_subdir.relative_to(docs_dir)} -> mathematics/{subfolder}/")
                    print(f"  [MOVED] {doc_subdir.relative_to(docs_dir)} -> mathematics/{subfolder}/")
    
    # Verify structure
    print("\n[3] Verifying mathematics/ structure...")
    missing = []
    for filename, subfolder in MATH_FILES_MAP.items():
        math_file = math_dir / subfolder / filename
        if not math_file.exists():
            missing.append(f"mathematics/{subfolder}/{filename}")
            print(f"  [MISSING] mathematics/{subfolder}/{filename}")
        else:
            print(f"  [OK] mathematics/{subfolder}/{filename}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Moved: {len(moved)} files")
    print(f"Removed (duplicates): {len(removed)} files")
    print(f"Already in place: {len(skipped)} files")
    if missing:
        print(f"Missing: {len(missing)} files")
    
    print(f"\n{'='*60}")
    print("Math docs organization complete!")
    print(f"{'='*60}\n")
    
    return moved, removed, missing

def main():
    """Main function."""
    moved, removed, missing = check_and_remove_duplicates()
    
    if missing:
        print("\n[WARNING] Some math files are missing from mathematics/ folder!")
        print("Please check the files above.")
    else:
        print("\n[OK] All math docs are properly organized in mathematics/ folder!")

if __name__ == "__main__":
    main()

