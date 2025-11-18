import requests

from playwright.sync_api import sync_playwright


def main() -> None:
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://www.investing.com/indices/baltic-dry-historical-data"
    html = requests.get(url, headers=headers, timeout=30).text
    marker = 'smlId":'
    idx = html.find(marker)
    if idx == -1:
        with open("investing_bdi.html", "w", encoding="utf-8") as fp:
            fp.write(html)
        print("smlId marker not found in static HTML. Capturing dynamic content via Playwright...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            def log_request(request):
                if "histor" in request.url.lower() or "download" in request.url.lower():
                    print("request", request.method, request.url)
                    print("headers", request.headers)
            page.on("request", log_request)
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(5000)
            content = page.content()
            with open("investing_bdi_playwright.html", "w", encoding="utf-8") as fp:
                fp.write(content)
            cookies = context.cookies()
            print("cookies", cookies)
            browser.close()
            marker_dynamic = content.find(marker)
            if marker_dynamic == -1:
                print("smlId still not found after JS execution.")
            else:
                print("Found marker in dynamic content.")
    else:
        snippet = html[idx:idx + 50]
        print("snippet", snippet)


if __name__ == "__main__":
    main()

