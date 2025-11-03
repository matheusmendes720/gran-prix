"""
Reorganize design assets to fit fullstack app architecture.
Moves design folder assets to proper frontend/public structure.
"""
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

def reorganize_design_assets():
    """Reorganize design assets following fullstack architecture."""
    print("\n" + "="*60)
    print("DESIGN ASSETS REORGANIZATION")
    print("="*60 + "\n")
    
    moved = []
    created = []
    
    # Create proper design asset directories
    design_dirs = [
        "frontend/public/images/design",      # UI mockups, reference images
        "frontend/public/images/icons",       # Icons
        "frontend/public/images/logos",       # Logos
        "frontend/public/assets/fonts",      # Custom fonts
        "docs/design/mockups",                # Design mockups documentation
        "docs/design/specs",                  # Design specifications
    ]
    
    print("[1] Creating design asset directories...")
    for dir_path in design_dirs:
        full_path = BASE_DIR / dir_path
        try:
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(dir_path)
            print(f"[OK] Created: {dir_path}")
        except Exception as e:
            print(f"[SKIP] {dir_path} - {e}")
    
    # Move design folder assets
    print("\n[2] Moving design folder assets...")
    design_source = BASE_DIR / "design"
    
    if design_source.exists():
        # Move images to frontend/public/images/design
        dest_dir = BASE_DIR / "frontend/public/images/design"
        
        for item in design_source.iterdir():
            if item.is_file():
                dest_file = dest_dir / item.name
                try:
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(dest_file))
                    moved.append(f"{item.name} -> frontend/public/images/design/")
                    print(f"[OK] Moved: {item.name}")
                except Exception as e:
                    print(f"[ERROR] Failed to move {item.name}: {e}")
            elif item.is_dir():
                # Move subdirectories recursively
                dest_subdir = dest_dir / item.name
                try:
                    shutil.move(str(item), str(dest_subdir))
                    moved.append(f"{item.name}/ -> frontend/public/images/design/")
                    print(f"[OK] Moved directory: {item.name}/")
                except Exception as e:
                    print(f"[ERROR] Failed to move {item.name}/: {e}")
        
        # Remove empty design folder
        try:
            design_source.rmdir()
            print(f"[OK] Removed empty design folder")
        except Exception as e:
            print(f"[INFO] design folder not empty or already removed: {e}")
    else:
        print("[INFO] design folder not found - may have been moved already")
    
    # Create README for design assets
    print("\n[3] Creating design assets README...")
    readme_content = """# Design Assets

## Structure

```
frontend/public/images/
├── design/          # UI mockups, reference images, WhatsApp screenshots
├── icons/           # Application icons
└── logos/           # Brand logos

frontend/public/assets/
└── fonts/           # Custom fonts

docs/design/
├── mockups/         # Design mockups documentation
└── specs/           # Design specifications
```

## Usage

### Images in Next.js Components

```tsx
import Image from 'next/image'

<Image
  src="/images/design/screenshot.jpg"
  alt="Design reference"
  width={800}
  height={600}
/>
```

### Static Assets

All files in `frontend/public/` are served at the root URL:
- `/images/design/file.jpg` → accessible at `http://localhost:3000/images/design/file.jpg`

## Guidelines

- **UI Mockups**: Place in `frontend/public/images/design/`
- **Icons**: Place in `frontend/public/images/icons/`
- **Logos**: Place in `frontend/public/images/logos/`
- **Fonts**: Place in `frontend/public/assets/fonts/`
- **Design Docs**: Place in `docs/design/mockups/` or `docs/design/specs/`

## Next.js Image Optimization

Next.js automatically optimizes images from `/public`:
- Automatic WebP/AVIF conversion
- Responsive images
- Lazy loading
- Blur placeholder support
"""
    
    readme_path = BASE_DIR / "frontend/public/images/README.md"
    try:
        readme_path.write_text(readme_content, encoding='utf-8')
        print("[OK] Created design assets README")
    except Exception as e:
        print(f"[ERROR] Failed to create README: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("REORGANIZATION SUMMARY")
    print("="*60)
    print(f"\n[OK] Created {len(created)} directories")
    print(f"[OK] Moved {len(moved)} items")
    print(f"\nDesign assets are now organized in:")
    print("  - frontend/public/images/design/ (UI assets)")
    print("  - frontend/public/images/icons/ (Icons)")
    print("  - frontend/public/images/logos/ (Logos)")
    print("  - docs/design/ (Design documentation)")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    reorganize_design_assets()

