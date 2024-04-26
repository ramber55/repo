from pprint import pprint
from pathlib import Path

import http.server
import socketserver
from urllib.parse import parse_qs, urlparse
import jinja2 as j

import GB_ensembl_client

import termcolor

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

# -- Some directories commonly used along this code:
GBSERVER_DIR = Path.cwd()
HTML_FOLDER = GBSERVER_DIR / "HTML"

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

        file_to_serve = ""
        if parsed_path == "/":
            # index.html must be served
            file_to_serve = HTML_FOLDER / "index.html"
        elif parsed_path == "/getSpeciesList":
            received_limit = parsed_arguments.get("limit", ["0"])
            limit = int(received_limit[0])
            print("Límite: ", limit)

            # file_to_serve = HTML_FOLDER / "SpeciesList.HTML"
            file_to_serve = HTML_FOLDER / "test.html"
        else:
            # error.HTML must be served
            file_to_serve = HTML_FOLDER / "error.HTML"

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
gb_ensembl_client = GB_ensembl_client

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
