"""
Utility script to organize reports into the new archive structure.
Automatically categorizes reports by topic and subject.
"""
from pathlib import Path
import re
from datetime import datetime
import shutil

BASE_DIR = Path(__file__).parent.parent.parent
ARCHIVE_DIR = BASE_DIR / "docs" / "archives"

# Topic keywords mapping
TOPIC_KEYWORDS = {
    "pipeline": ["pipeline", "data ingestion", "processing", "preprocessing", "merging"],
    "datasets": ["dataset", "data", "kaggle", "zenodo", "github", "scraped", "fetch"],
    "models": ["model", "training", "arima", "prophet", "lstm", "xgboost", "ensemble"],
    "dashboard": ["dashboard", "ui", "visualization", "chart", "plot"],
    "api": ["api", "endpoint", "rest", "server"],
    "deployment": ["deployment", "docker", "kubernetes", "infrastructure"],
    "visualization": ["visualization", "chart", "plot", "graph"],
    "integration": ["integration", "brazilian", "external", "api"],
    "performance": ["performance", "benchmark", "optimization"],
    "benchmarks": ["benchmark", "comparison", "metrics", "evaluation"],
}

def detect_topic(filename: str, content: str = "") -> str:
    """Detect topic from filename and optional content."""
    filename_lower = filename.lower()
    
    # Check filename first
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in filename_lower for keyword in keywords):
            return topic
    
    # If content provided, check content
    if content:
        content_lower = content.lower()
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(keyword in content_lower for keyword in keywords):
                return topic
    
    return "general"

def extract_date(filename: str) -> str:
    """Extract date from filename or use current date."""
    # Try to find date in filename (YYYY-MM-DD or YYYYMMDD)
    date_patterns = [
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{4}\d{2}\d{2})",
        r"(\d{8})",
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            date_str = match.group(1)
            if len(date_str) == 8:  # YYYYMMDD
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            return date_str
    
    return datetime.now().strftime("%Y-%m-%d")

def organize_report(source_file: Path, archive_type: str = "reports") -> Path:
    """Organize a report file into the archive structure."""
    if not source_file.exists():
        print(f"[SKIP] File not found: {source_file}")
        return None
    
    # Read content for topic detection
    try:
        content = source_file.read_text(encoding="utf-8")[:1000]  # First 1000 chars
    except:
        content = ""
    
    # Detect topic and date
    topic = detect_topic(source_file.name, content)
    date = extract_date(source_file.name)
    year = date.split("-")[0]
    
    # Determine archive path
    archive_path = ARCHIVE_DIR / archive_type / topic / year / date
    archive_path.mkdir(parents=True, exist_ok=True)
    
    # Copy file to archive
    dest_file = archive_path / source_file.name
    shutil.copy2(source_file, dest_file)
    
    print(f"[OK] Organized: {source_file.name} -> {archive_path.relative_to(BASE_DIR)}")
    return dest_file

def organize_all_reports(source_dir: Path = None):
    """Organize all reports from source directory."""
    if source_dir is None:
        source_dir = BASE_DIR
    
    # Find all markdown reports
    reports = list(source_dir.glob("**/*.md"))
    reports.extend(list(source_dir.glob("**/*SUCCESS*.txt")))
    reports.extend(list(source_dir.glob("**/*REPORT*.txt")))
    
    organized = []
    
    for report_file in reports:
        # Skip if already in archive
        if "docs/archives" in str(report_file):
            continue
        
        # Skip README files
        if report_file.name.upper() in ["README.MD", "README.TXT"]:
            continue
        
        # Determine archive type
        filename_upper = report_file.name.upper()
        if "SUCCESS" in filename_upper:
            archive_type = "success"
        elif "BENCHMARK" in filename_upper or "PERFORMANCE" in filename_upper:
            archive_type = "benchmarks"
        elif "CHANGELOG" in filename_upper or "CHANGE" in filename_upper:
            archive_type = "changelogs"
        elif "ANALYSIS" in filename_upper or "ANALYZE" in filename_upper:
            archive_type = "analysis"
        else:
            archive_type = "reports"
        
        dest = organize_report(report_file, archive_type)
        if dest:
            organized.append(dest)
    
    print(f"\n{'='*60}")
    print(f"Organized {len(organized)} reports")
    print(f"{'='*60}")
    
    return organized

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Organize reports into archive structure")
    parser.add_argument("--source", type=str, help="Source directory (default: project root)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without organizing")
    
    args = parser.parse_args()
    
    source_dir = Path(args.source) if args.source else None
    
    if args.dry_run:
        print("[DRY RUN] Would organize reports:")
        # Just show what would be organized
    else:
        print("Organizing reports into archive structure...")
        organize_all_reports(source_dir)
        print("\n[SUCCESS] Reports organized!")

