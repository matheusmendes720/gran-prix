"""
Comprehensive Reorganization Script
Separates success reports from diagnostics/documentation and cleans root/docs folders.
"""
import shutil
from pathlib import Path
import re
from datetime import datetime
from typing import List, Tuple, Dict

BASE_DIR = Path(__file__).parent.parent.parent

# File classification patterns
SUCCESS_KEYWORDS = [
    "SUCCESS", "COMPLETE", "FINAL", "MILESTONE", "CELEBRATION",
    "ACHIEVEMENT", "ACCOMPLISHED", "DONE", "READY", "LAUNCH"
]

DIAGNOSTIC_KEYWORDS = [
    "ANALYSIS", "DIAGNOSTIC", "REPORT", "GAP", "ISSUE", "PROBLEM",
    "ERROR", "BUG", "INVESTIGATION", "TROUBLESHOOTING", "REVIEW"
]

DOCUMENTATION_KEYWORDS = [
    "GUIDE", "README", "INDEX", "NAVIGATION", "TUTORIAL", "HOWTO",
    "INSTRUCTIONS", "DOCUMENTATION", "SUMMARY", "OVERVIEW"
]

# Topic detection keywords
TOPIC_KEYWORDS = {
    "pipeline": ["pipeline", "processing", "data", "etl"],
    "datasets": ["dataset", "data", "download", "fetch", "kaggle", "zenodo"],
    "models": ["model", "training", "arima", "prophet", "lstm", "ensemble"],
    "dashboard": ["dashboard", "ui", "visualization", "web"],
    "api": ["api", "endpoint", "server", "integration"],
    "deployment": ["deployment", "docker", "kubernetes", "infrastructure"],
    "integration": ["integration", "brazilian", "external", "api"],
    "performance": ["performance", "benchmark", "optimization"],
    "mathematics": ["math", "formula", "calculation", "mathematical"],
}

def classify_file(filename: str, content: str = "") -> Tuple[str, str]:
    """
    Classify file as success report, diagnostic, or documentation.
    
    Returns: (category, topic)
    - category: "success", "diagnostic", "documentation", or "misc"
    - topic: detected topic or "general"
    """
    filename_upper = filename.upper()
    
    # Determine category
    if any(keyword in filename_upper for keyword in SUCCESS_KEYWORDS):
        category = "success"
    elif any(keyword in filename_upper for keyword in DIAGNOSTIC_KEYWORDS):
        category = "diagnostic"
    elif any(keyword in filename_upper for keyword in DOCUMENTATION_KEYWORDS):
        category = "documentation"
    else:
        category = "misc"
    
    # Detect topic
    filename_lower = filename.lower()
    content_lower = content.lower() if content else ""
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in filename_lower for keyword in keywords):
            return category, topic
        if content and any(keyword in content_lower for keyword in keywords):
            return category, topic
    
    return category, "general"

def extract_date(filename: str) -> str:
    """Extract date from filename."""
    patterns = [
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{4}\d{2}\d{2})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            date_str = match.group(1)
            if len(date_str) == 8:
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            return date_str
    
    return datetime.now().strftime("%Y-%m-%d")

def organize_docs_folder():
    """Organize docs/ folder - separate success reports from diagnostics."""
    print(f"\n{'='*60}")
    print("Organizing docs/ Folder")
    print(f"{'='*60}\n")
    
    docs_dir = BASE_DIR / "docs"
    organized = []
    
    # Create structure
    success_dir = docs_dir / "archives" / "success"
    diagnostic_dir = docs_dir / "diagnostics"
    documentation_dir = docs_dir / "documentation"
    
    success_dir.mkdir(parents=True, exist_ok=True)
    diagnostic_dir.mkdir(parents=True, exist_ok=True)
    documentation_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to keep in docs root
    keep_in_root = {
        "README.md",
        "BENCHMARK_REGISTRY.md",
        "DOCUMENTATION_INDEX.md",
        "ARCHIVE_INDEX.md",
    }
    
    # Organize all markdown files in docs root
    for md_file in docs_dir.glob("*.md"):
        if md_file.name in keep_in_root:
            continue
        
        # Read first 500 chars for classification
        try:
            content = md_file.read_text(encoding="utf-8")[:500]
        except:
            content = ""
        
        category, topic = classify_file(md_file.name, content)
        date = extract_date(md_file.name)
        year = date.split("-")[0]
        
        try:
            if category == "success":
                # Success reports go to archives/success/
                dest = success_dir / topic / year / date / md_file.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(md_file), str(dest))
                organized.append((md_file.name, f"archives/success/{topic}/{year}/{date}/"))
                print(f"[SUCCESS] {md_file.name} -> archives/success/{topic}/")
                
            elif category == "diagnostic":
                # Diagnostic files go to diagnostics/
                dest = diagnostic_dir / topic / md_file.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(md_file), str(dest))
                organized.append((md_file.name, f"diagnostics/{topic}/"))
                print(f"[DIAGNOSTIC] {md_file.name} -> diagnostics/{topic}/")
                
            elif category == "documentation":
                # Documentation goes to documentation/
                dest = documentation_dir / topic / md_file.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(md_file), str(dest))
                organized.append((md_file.name, f"documentation/{topic}/"))
                print(f"[DOCS] {md_file.name} -> documentation/{topic}/")
                
            else:
                # Misc files
                dest = docs_dir / "misc" / md_file.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(md_file), str(dest))
                organized.append((md_file.name, "misc/"))
                print(f"[MISC] {md_file.name} -> misc/")
                
        except Exception as e:
            print(f"[ERROR] Failed to move {md_file.name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Organized {len(organized)} files in docs/")
    print(f"{'='*60}\n")
    
    return organized

def clean_root_folder():
    """Clean root folder - move everything to proper subfolders."""
    print(f"\n{'='*60}")
    print("Cleaning Root Folder")
    print(f"{'='*60}\n")
    
    moved = []
    
    # Essential files to keep
    keep_files = {
        "README.md",
        "docker-compose.yml",
        ".gitignore",
        ".dockerignore",
    }
    
    # Essential directories to keep
    keep_dirs = {
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
        "demand_forecasting",  # Legacy backup
    }
    
    # Move all files in root
    for root_file in BASE_DIR.iterdir():
        if root_file.is_file() and root_file.name not in keep_files:
            # Determine destination
            name = root_file.name
            ext = root_file.suffix.lower()
            
            try:
                if ext == ".md":
                    dest = BASE_DIR / "docs" / "documentation" / "general" / name
                elif ext == ".py":
                    dest = BASE_DIR / "backend" / "scripts" / name
                elif ext in [".txt", ".log"]:
                    dest = BASE_DIR / "docs" / "misc" / name
                elif ext in [".json", ".yaml", ".yml"]:
                    dest = BASE_DIR / "config" / name
                elif ext in [".html", ".css"]:
                    dest = BASE_DIR / "frontend" / "public" / name
                elif ext in [".sh", ".bat"]:
                    dest = BASE_DIR / "backend" / "scripts" / name
                elif ext == ".csv":
                    dest = BASE_DIR / "data" / "processed" / "samples" / name
                else:
                    dest = BASE_DIR / "docs" / "misc" / name
                
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root_file), str(dest))
                moved.append((name, str(dest.relative_to(BASE_DIR))))
                print(f"[OK] Moved: {name} -> {dest.relative_to(BASE_DIR)}")
                
            except Exception as e:
                print(f"[ERROR] Failed to move {name}: {e}")
    
    # Handle legacy directories
    for root_dir in BASE_DIR.iterdir():
        if root_dir.is_dir() and root_dir.name not in keep_dirs:
            name = root_dir.name
            
            try:
                # src/ - move remaining files
                if name == "src":
                    backend_pipelines = BASE_DIR / "backend" / "pipelines"
                    for item in root_dir.rglob("*.py"):
                        if "pipeline" in str(item.parent):
                            dest = backend_pipelines / "data_processing" / item.name
                        elif "validation" in str(item.parent):
                            dest = backend_pipelines / "monitoring" / item.name
                        else:
                            dest = BASE_DIR / "backend" / "scripts" / item.name
                        
                        if not dest.exists():
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(item), str(dest))
                            moved.append((f"{name}/{item.name}", str(dest.relative_to(BASE_DIR))))
                            print(f"[OK] Moved: {name}/{item.name} -> {dest.relative_to(BASE_DIR)}")
                    
                    # Remove if empty
                    try:
                        if not any(root_dir.rglob("*")):
                            root_dir.rmdir()
                            moved.append((f"{name}/", "removed"))
                            print(f"[OK] Removed empty: {name}/")
                    except:
                        pass
                
                # scripts/ - move remaining files
                elif name == "scripts":
                    backend_scripts = BASE_DIR / "backend" / "scripts"
                    for item in root_dir.iterdir():
                        if item.is_file() and not (backend_scripts / item.name).exists():
                            shutil.move(str(item), str(backend_scripts / item.name))
                            moved.append((f"{name}/{item.name}", "backend/scripts/"))
                            print(f"[OK] Moved: {name}/{item.name} -> backend/scripts/")
                    
                    # Remove if empty
                    try:
                        if not any(root_dir.iterdir()):
                            root_dir.rmdir()
                            moved.append((f"{name}/", "removed"))
                            print(f"[OK] Removed empty: {name}/")
                    except:
                        pass
                
                # docs_html/ - move to frontend/public/
                elif name == "docs_html":
                    dest = BASE_DIR / "frontend" / "public" / "docs_html"
                    if not dest.exists():
                        shutil.move(str(root_dir), str(dest))
                        moved.append((f"{name}/", str(dest.relative_to(BASE_DIR))))
                        print(f"[OK] Moved: {name}/ -> frontend/public/")
                
                else:
                    # Unknown directory -> docs/misc/
                    dest = BASE_DIR / "docs" / "misc" / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if not dest.exists():
                        shutil.move(str(root_dir), str(dest))
                        moved.append((f"{name}/", str(dest.relative_to(BASE_DIR))))
                        print(f"[OK] Moved: {name}/ -> docs/misc/")
                    
            except Exception as e:
                print(f"[ERROR] Failed to organize {name}/: {e}")
    
    print(f"\n{'='*60}")
    print(f"Moved {len(moved)} items from root")
    print(f"{'='*60}\n")
    
    return moved

def create_docs_index():
    """Create documentation index in docs/ folder."""
    docs_dir = BASE_DIR / "docs"
    index_file = docs_dir / "DOCUMENTATION_INDEX.md"
    
    index_content = f"""# 📚 Documentation Index

## Nova Corrente - Documentation Organization

This folder contains all project documentation organized by type and topic.

## 📁 Folder Structure

### `/archives/success/` - Success Reports
All milestone reports, completion summaries, and success stories organized by:
- **Topic** (pipeline, datasets, models, dashboard, etc.)
- **Timeline** (by year and date)

### `/diagnostics/` - Diagnostic Reports
All analysis, troubleshooting, gap analysis, and diagnostic documents organized by:
- **Topic** (pipeline, datasets, models, etc.)

### `/documentation/` - Guides & Documentation
All guides, tutorials, READMEs, and documentation organized by:
- **Topic** (guides, tutorials, READMEs, etc.)

### `/guides/` - User Guides
User-facing guides and tutorials.

### `/mathematics/` - Mathematical Documentation
Mathematical formulas, proofs, and implementations.

### `/misc/` - Miscellaneous
Other documentation files.

---

## 🔍 Quick Navigation

- **Success Reports:** `docs/archives/success/`
- **Diagnostics:** `docs/diagnostics/`
- **Documentation:** `docs/documentation/`
- **User Guides:** `docs/guides/`
- **Mathematics:** `docs/mathematics/`

---

*Last updated: {datetime.now().strftime("%Y-%m-%d")}*
"""
    
    index_file.write_text(index_content, encoding="utf-8")
    print(f"[OK] Created: docs/DOCUMENTATION_INDEX.md")

def main():
    """Main reorganization function."""
    print(f"\n{'='*80}")
    print("COMPREHENSIVE REORGANIZATION")
    print("Separating Success Reports from Diagnostics & Documentation")
    print(f"{'='*80}\n")
    
    # 1. Organize docs folder
    docs_organized = organize_docs_folder()
    
    # 2. Clean root folder
    root_cleaned = clean_root_folder()
    
    # 3. Create documentation index
    create_docs_index()
    
    print(f"\n{'='*80}")
    print("REORGANIZATION COMPLETE!")
    print(f"{'='*80}")
    print(f"[OK] Organized {len(docs_organized)} files in docs/")
    print(f"[OK] Moved {len(root_cleaned)} items from root")
    print(f"\n[OK] Root folder: Clean (only 4 essential files)")
    print(f"[OK] Docs folder: Organized (success/diagnostics/documentation separated)")
    print(f"{'='*80}\n")
    
    return docs_organized, root_cleaned

if __name__ == "__main__":
    main()

