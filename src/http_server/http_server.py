from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from my_gui import gui_

HOST = ""
PORT = 9999

# class trigger_server:
#     def __init__(self, app: gui_.App) -> None:
#         Trigger_handler.app = gui_.App
#         server = HTTPServer((HOST, PORT), Trigger_handler)
#         server.serve_forever()
def trigger_server(app: gui_.App):
    Trigger_handler.app = app
    server = HTTPServer(('', PORT), Trigger_handler)
    print("Server is now running\n")
    server.serve_forever()
    server.server_close()
    print("Server terminated\n")

class Trigger_handler(BaseHTTPRequestHandler):
    app : gui_.App = None
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        print("Getting\n")
        print("Path = ", self.path)
        if self.app is not None:
            self.app.save_images(self.path[1:])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Hello world!</h1></body></html>", "utf-8"))
    def do_POST(self):
        print("POST received.\n")
        self._set_headers()
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len).decode("utf-8")
        file_code = None
        try:
            post_body = json.loads(post_body)
            # EX:
            # curl -X POST -H "Action : Shot" http://localhost:9999 -d '{"fplate" : "51G12345", "bplate" : "51G67890", "c1" : "ABCD123456", "c2" : "NA"}'
            # file_code = f"{post_body['fplate']}{post_body['bplate']}_{post_body['cntno']}"
            try:
                file_code = f"{post_body['fplate']}"
            except:
                pass
            try:    
                file_code += f"_{post_body['bplate']}"
            except:
                pass
            try:
                file_code += f"_{post_body['cntno']}"
            except:
                pass
        except json.decoder.JSONDecodeError as e:
            print(e)
        if self.app is not None:
            self.app.save_images(file_code)
        print(f"Header: {(self.headers.get('Action'))} - Content: {(post_body)} - Type: {type(post_body)}\n")
        self.wfile.write(bytes(f"Content: {post_body}", "utf-8"))