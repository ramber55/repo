from pprint import pprint
from pathlib import Path

import http.server
import socketserver
from urllib.parse import parse_qs, urlparse
import jinja2 as j


import termcolor

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

# -- Some directories commonly used along this code:
MY_PYTHON_REPO = Path.cwd().parent
MY_RESOURCES = MY_PYTHON_REPO / "resources"

MY_HTML_PAGES = MY_RESOURCES / "html_pages"
MY_HTML_INFO_PAGES = MY_HTML_PAGES / "info"

# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

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
            file_to_serve = MY_HTML_PAGES / "index.html"
        elif parsed_path == "/ping":
            file_to_serve = MY_HTML_PAGES / "ping.html"
        elif parsed_path == "/getSeqByLetter":
            base_to_get = parsed_arguments["baseLetter"][0]
            filename_to_serve = base_to_get + ".html"
            file_to_serve = MY_HTML_INFO_PAGES / filename_to_serve
        elif parsed_path == "/getSeqByName":
            base_to_get = parsed_arguments["baseName"][0]
            print("base name=", base_to_get)
            filename_to_serve = base_to_get + ".html"
            file_to_serve = MY_HTML_PAGES / "ping.html"
        elif parsed_path == "/operation":
            print("Parsed Arguments:")
            pprint(parsed_arguments)
            operation_to_do = parsed_arguments["operationType"]
            string_to_process = parsed_arguments["stringData"]
            print(f"I have to do {operation_to_do[0]} with \"{string_to_process[0]}\"")

            file_to_serve = MY_HTML_PAGES / "ping.html"

        else:
            # error.html must be served
            file_to_serve = MY_HTML_PAGES / "error.html"

        contents = file_to_serve.read_text("utf-8")

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
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
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
