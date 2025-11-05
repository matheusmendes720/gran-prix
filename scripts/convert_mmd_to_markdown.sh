#!/bin/bash
# Convert Mermaid .mmd files to Markdown documentation
# Linux/macOS shell script wrapper

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "========================================"
echo "MERMAID TO MARKDOWN CONVERTER"
echo "========================================"
echo ""

cd "$PROJECT_ROOT"
python3 scripts/convert_mmd_to_markdown.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[!] Conversion failed!"
    exit 1
fi

echo ""
echo "[OK] Conversion complete!"

