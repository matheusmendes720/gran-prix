from mitmproxy import http
from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
REPORTS_RAW = BASE_DIR / "reports" / "raw"
REPORTS_RAW.mkdir(parents=True, exist_ok=True)


class HARRecorder:
    def __init__(self):
        self.entries = []

    def request(self, flow: http.HTTPFlow):  # pragma: no cover
        pass

    def response(self, flow: http.HTTPFlow):  # pragma: no cover
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "request": {
                "method": flow.request.method,
                "url": flow.request.pretty_url,
                "headers": dict(flow.request.headers),
                "content": flow.request.get_text(),
            },
            "response": {
                "status_code": flow.response.status_code,
                "headers": dict(flow.response.headers),
                "content": flow.response.get_text(),
            },
        }
        self.entries.append(entry)
        if len(self.entries) >= 50:
            self.flush()

    def flush(self):  # pragma: no cover
        if not self.entries:
            return
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        har_path = REPORTS_RAW / f"mitmproxy_capture_{timestamp}.json"
        with har_path.open("w", encoding="utf-8") as fh:
            json.dump(self.entries, fh, ensure_ascii=False, indent=2)
        self.entries.clear()

    def done(self):  # pragma: no cover
        self.flush()


addons = [HARRecorder()]
