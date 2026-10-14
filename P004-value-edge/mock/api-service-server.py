from __future__ import annotations

import json
import os
import re
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8765"))
JQUANTS_URL = "https://api.jquants.com/v2/equities/bars/daily"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, _format, *_args):
        # Do not log request headers or API keys.
        return

    def send_json(self, status: int, payload: object):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path != "/api/daily":
            if parsed.path == "/":
                self.path = "/api-service.html"
            return super().do_GET()

        api_key = self.headers.get("x-api-key", "").strip()
        params = parse_qs(parsed.query)
        code = params.get("code", [""])[0].strip()
        date_from = params.get("from", [""])[0]
        date_to = params.get("to", [""])[0]

        if not api_key:
            return self.send_json(400, {"message": "APIキーを入力してください。"})
        if not re.fullmatch(r"\d{4,5}", code):
            return self.send_json(400, {"message": "銘柄コードは4桁または5桁で指定してください。"})
        try:
            start = date.fromisoformat(date_from)
            end = date.fromisoformat(date_to)
        except ValueError:
            return self.send_json(400, {"message": "取得期間の日付形式が正しくありません。"})
        if start > end:
            return self.send_json(400, {"message": "取得開始日は終了日以前にしてください。"})

        query = urlencode({"code": code, "from": date_from, "to": date_to})
        request = Request(
            f"{JQUANTS_URL}?{query}",
            headers={"x-api-key": api_key, "Accept": "application/json"},
            method="GET",
        )
        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", response.headers.get("Content-Type", "application/json; charset=utf-8"))
                self.send_header("Content-Length", str(len(payload)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(payload)
        except HTTPError as error:
            payload = error.read()
            self.send_response(error.code)
            self.send_header("Content-Type", error.headers.get("Content-Type", "application/json; charset=utf-8"))
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)
        except (URLError, TimeoutError, OSError) as error:
            self.send_json(502, {"message": f"J-Quants APIへの接続に失敗しました: {error.reason if isinstance(error, URLError) else error}"})

    def do_POST(self):
        self.send_json(405, {"message": "このAPIサービスモックはGETのみ対応しています。"})


if __name__ == "__main__":
    print(f"VALUE EDGE APIサービスモック: http://{HOST}:{PORT}/")
    print("終了するには、このウィンドウで Ctrl+C を押してください。")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
