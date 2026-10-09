from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging

logging.basicConfig(level=logging.INFO)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/warn":
            status, level, message = 401, "WARN", "Unauthorized request"
        elif self.path == "/error":
            status, level, message = 500, "ERROR", "Internal server error"
        else:
            status, level, message = 200, "INFO", "Request successful"

        log = {
            "level": level,
            "status_code": status,
            "path": self.path,
            "message": message
        }
        print(json.dumps(log), flush=True)

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": message}).encode())

    def log_message(self, format, *args):
        pass

HTTPServer(("0.0.0.0", 5000), Handler).serve_forever()
