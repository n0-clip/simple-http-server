import http.server
import socketserver
import logging

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
    content_length = int(self.headers['Content-Length'])  # Get the size of data
    post_data = self.rfile.read(content_length)  # Get the data itself
    logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                 str(self.path), str(self.headers), post_data.decode('utf-8'))

    # Begin the response
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # Send the html message
    response = BytesIO()
    response.write(b'This is POST request. ')
    response.write(b'Received: ')
    response.write(post_data)
    self.wfile.write(response.getvalue())

Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    logging.basicConfig(level=logging.INFO)
    logging.info("serving at port %s", PORT)
    httpd.serve_forever()