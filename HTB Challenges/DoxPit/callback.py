#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/x-component")
        self.end_headers()

    def do_GET(self):
        target = parse_qs(urlparse(self.path).query)["to"][0]
        self.send_response(302)
        self.send_header("Location", target)
        self.end_headers()

    def log_message(self, fmt, *args):
        print(f"{self.command} {self.path} -> {fmt % args}", flush=True)


ThreadingHTTPServer(("127.0.0.1", 8001), Handler).serve_forever()
