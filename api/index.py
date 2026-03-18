from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            dashboard_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'index.html')
            with open(dashboard_path, 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/data.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'data.json')
            with open(data_path, 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/embed.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            js_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'embed.js')
            with open(js_path, 'r') as f:
                self.wfile.write(f.read().encode())
        else:
            self.send_response(404)
            self.end_headers()
        return
