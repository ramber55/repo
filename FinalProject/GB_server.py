from pprint import pprint
from pathlib import Path
import termcolor

import http.server
import socketserver
from urllib.parse import parse_qs, urlparse

import GB_html_mgmt

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

# -- Some directories commonly used along this code:
GBSERVER_DIR = Path.cwd()
HTML_FOLDER = GBSERVER_DIR / "HTML"

gb_html_handler = GB_html_mgmt.GB_html_handler()

# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class GB_Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        print(" Request line: ", end="")
        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path)
        parsed_path = url_path.path  # we get it from here
        parsed_arguments = parse_qs(url_path.query)

        print(" path: ", end="")
        pprint(parsed_path)
        print(" arguments: ", end="")
        pprint(parsed_arguments)

        if parsed_path == "/":
            # index.html must be served
            file_to_serve = HTML_FOLDER / "index.html"
            contents = file_to_serve.read_text("utf-8")
        elif parsed_path == "/getSpeciesList":
            contents = gb_html_handler.getSpeciesList(parsed_arguments)
        elif parsed_path == "/getSeqByLetter":
            file_to_serve = HTML_FOLDER / "test.html"
            contents = file_to_serve.read_text("utf-8")
        else:
            # error.HTML must be served
            file_to_serve = HTML_FOLDER / "error.html"
            contents = file_to_serve.read_text("utf-8")

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/HTML')
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
gb_handler = GB_Handler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), gb_handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
