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
        post_body = self.rfile.read(content_len).decode("utf-8")
        try:
            post_body = json.loads(post_body)
            # print(f"Test: {json.dumps(post_body)} - Type: {type(json.dumps(post_body))}\n")
            # EX:
            # curl -X POST -H "Action : Shot" http://localhost:9999 -d '{"fplate" : "51G12345", "bplate" : "51G67890", "c1" : "ABCD123456", "c2" : "NA"}'
        except json.decoder.JSONDecodeError as e:
            print(e)
        print(f"Header: {(self.headers.get('Action'))} - Content: {(post_body)} - Type: {type(post_body)}\n")
        self.wfile.write(bytes(f"Content: {post_body}", "utf-8"))


server = HTTPServer((HOST, PORT), SampleHTTP)
print("Server is now running")

server.serve_forever()
server.server_close()
print("Server terminated")