from http.server import HTTPServer, BaseHTTPRequestHandler
import json
HOST = ""
# HOST = "10.8.31.158"
PORT = 9999

class SampleHTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("Getting\n")
        print("Path = ", self.path[1:])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Hello world!</h1></body></html>", "utf-8"))

    def do_POST(self):
        print("POST received.\n")
        self._set_headers()
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        try:
            post_body = json.loads(post_body)
            # print(f"Test: {json.dumps(post_body)} - Type: {type(json.dumps(post_body))}\n")
        except json.decoder.JSONDecodeError:
            print("Not json format!")
        print(f"Header: {(self.headers.get('Action'))} - Content: {(post_body)} - Type: {type(post_body)}\n")
        self.wfile.write(bytes(f"Content: {post_body}", "utf-8"))


server = HTTPServer((HOST, PORT), SampleHTTP)
print("Server is now running")

server.serve_forever()
server.server_close()
print("Server terminated")