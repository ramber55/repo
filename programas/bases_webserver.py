from pathlib import Path
import http.server
import socketserver
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

        print(" Command: ", end="")
        termcolor.cprint(self.command, 'green')

        print(" Path: ", end="")
        termcolor.cprint(self.path, 'green')

        file_to_serve = ""
        if self.path == "/":
            # index.HTML must be served
            file_to_serve = MY_HTML_PAGES / "index.HTML"
        elif self.path == "/info/A.HTML":
            # index.HTML must be served
            file_to_serve = MY_HTML_INFO_PAGES / "A.HTML"
        elif self.path == "/info/C.HTML":
            # index.HTML must be served
            file_to_serve = MY_HTML_INFO_PAGES / "C.HTML"
        elif self.path == "/info/G.HTML":
            # index.HTML must be served
            file_to_serve = MY_HTML_INFO_PAGES / "G.HTML"
        elif self.path == "/info/T.HTML":
            # index.HTML must be served
            file_to_serve = MY_HTML_INFO_PAGES / "T.HTML"
        else:
            # error.HTML must be served
            file_to_serve = MY_HTML_PAGES / "error.HTML"

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
