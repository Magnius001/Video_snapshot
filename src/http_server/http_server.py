from http.server import HTTPServer, BaseHTTPRequestHandler
from my_gui import gui_

HOST = "10.8.31.158"
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
        print("Receiving POST...\n")
        self._set_headers()
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        self.wfile.write("received post request:<br>{}".format(post_body))