
from urllib.parse import urlparse
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


highlight_key_words = ""

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(highlight_key_words, "utf-8"))
        return

    def log_message(self, format, *args):
        return


def run():
    server = HTTPServer(('localhost', 8080), GetHandler)
    server.serve_forever()

