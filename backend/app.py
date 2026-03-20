from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = b'Hello from Effective Mobile!'
            self.wfile.write(response)
            self.log_request_custom(200, len(response))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = b'{"status": "ok"}'
            self.wfile.write(response)
            self.log_request_custom(200, len(response))
        else:
            self.send_response(404)
            self.end_headers()
            self.log_request_custom(404, 0)

    def log_request_custom(self, status_code, size):
        client_ip = self.client_address[0]
        date = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        request_line = self.requestline
        self.log_message('%s - - [%s] "%s" %s %s',
                         client_ip,
                         date,
                         request_line,
                         status_code,
                         size)

def run(port: int):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, Handler)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple HTTP server with healthcheck')
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port to listen on (default: 8080)'
    )

    args = parser.parse_args()
    run(args.port)
