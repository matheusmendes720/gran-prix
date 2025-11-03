"""Script to create comprehensive reports archive structure organized by topics/subjects."""
from pathlib import Path
import json

BASE_DIR = Path(__file__).parent

# Topic-based archive structure
TOPICS = {
    "pipeline": ["data_ingestion", "data_processing", "data_validation", "feature_engineering"],
    "datasets": ["kaggle", "zenodo", "github", "api_fetched", "scraped", "enrichment", "merging"],
    "models": ["arima", "prophet", "lstm", "xgboost", "ensemble", "training", "evaluation", "comparison"],
    "dashboard": ["ui", "visualizations", "charts", "metrics", "alerts", "user_experience"],
    "api": ["endpoints", "integration", "performance", "documentation", "testing"],
    "deployment": ["docker", "kubernetes", "infrastructure", "ci_cd", "monitoring"],
    "visualization": ["charts", "maps", "analytics", "reports", "exports"],
    "integration": ["brazilian_data", "external_apis", "third_party", "system_integration"],
    "performance": ["optimization", "benchmarks", "scalability", "resource_usage"],
    "benchmarks": ["model_comparison", "accuracy", "speed", "resource_usage", "cost_analysis"],
    "documentation": ["architecture", "guides", "tutorials", "api_docs", "changelog"],
    "testing": ["unit_tests", "integration_tests", "e2e_tests", "performance_tests"],
    "errors": ["bug_reports", "fixes", "investigations", "solutions"],
    "enhancements": ["features", "improvements", "optimizations", "new_capabilities"],
}

# Archive types
ARCHIVE_TYPES = [
    "reports",  # Detailed reports
    "success",  # Success summaries
    "changelogs",  # Change logs
    "benchmarks",  # Benchmark results
    "analysis",  # Analysis documents
    "screenshots",  # Visual documentation
    "exports",  # Exported data
]

def create_archive_structure():
    """Create comprehensive archive structure."""
    created = []
    base_archive = BASE_DIR / "docs" / "archives"
    
    for archive_type in ARCHIVE_TYPES:
        archive_dir = base_archive / archive_type
        
        # Create main archive type directory
        archive_dir.mkdir(parents=True, exist_ok=True)
        created.append(str(archive_dir))
        
        # Create topic-based subdirectories
        for topic, subtopics in TOPICS.items():
            topic_dir = archive_dir / topic
            topic_dir.mkdir(parents=True, exist_ok=True)
            created.append(str(topic_dir))
            
            # Create subtopic directories
            for subtopic in subtopics:
                subtopic_dir = topic_dir / subtopic
                subtopic_dir.mkdir(parents=True, exist_ok=True)
                created.append(str(subtopic_dir))
        
        # Create date-based subdirectories for better organization
        date_dirs = ["2024", "2025", "by_month", "by_quarter"]
        for date_dir in date_dirs:
            date_path = archive_dir / "timeline" / date_dir
            date_path.mkdir(parents=True, exist_ok=True)
            created.append(str(date_path))
    
    # Create index file
    create_archive_index(base_archive)
    
    print(f"\n{'='*60}")
    print(f"Created {len(created)} archive directories")
    print(f"{'='*60}")
    
    return created

def create_archive_index(base_dir: Path):
    """Create archive index file."""
    index_file = base_dir / "ARCHIVE_INDEX.md"
    
    index_content = """# 📚 Archive Index

## Nova Corrente - Reports & Documentation Archive

This archive contains all reports, success summaries, changelogs, benchmarks, and analysis documents organized by topic and subject.

## 📁 Archive Structure

### Archive Types

- **reports/** - Detailed analysis and status reports
- **success/** - Success summaries and milestone reports  
- **changelogs/** - Change logs and version history
- **benchmarks/** - Performance benchmarks and comparisons
- **analysis/** - Deep dive analysis documents
- **screenshots/** - Visual documentation and UI screenshots
- **exports/** - Exported data and results

### Topics & Subjects

"""
    
    for topic, subtopics in TOPICS.items():
        index_content += f"\n#### {topic.title()}\n"
        for subtopic in subtopics:
            index_content += f"- `{subtopic}/`\n"
    
    index_content += """
## 📅 Timeline Organization

Reports are also organized by:
- **by_year/** - 2024, 2025, etc.
- **by_month/** - Monthly archives
- **by_quarter/** - Quarterly archives

## 🔍 Quick Navigation

Use this index to quickly find reports by:
1. **Topic** - What subject area (pipeline, models, dashboard, etc.)
2. **Archive Type** - What kind of document (report, success, benchmark, etc.)
3. **Timeline** - When it was created

## 📝 Naming Convention

Files should follow this naming pattern:
- `REPORT_{TOPIC}_{SUBTOPIC}_{DATE}.md`
- `SUCCESS_{TOPIC}_{DESCRIPTION}_{DATE}.md`
- `BENCHMARK_{METRIC}_{DATE}.md`

Example: `REPORT_models_lstm_training_2025-11-01.md`

---
*Last updated: {date}*
""".replace("{date}", "2025-11-01")
    
    index_file.write_text(index_content, encoding="utf-8")
    print(f"Created archive index: {index_file}")

if __name__ == "__main__":
    print("Creating comprehensive archive structure...")
    print(f"Base directory: {BASE_DIR}\n")
    create_archive_structure()
    print("\n[SUCCESS] Archive structure creation complete!")

