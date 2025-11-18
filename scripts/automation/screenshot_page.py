from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--output", type=Path, default=Path("page.png"))
    parser.add_argument("--full-page", action="store_true")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(args.url, wait_until="networkidle", timeout=60000)
        page.screenshot(path=str(args.output), full_page=args.full_page)
        browser.close()


if __name__ == "__main__":
    main()

