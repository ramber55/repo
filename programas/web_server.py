import socket
import termcolor


# -- Server network parameters
IP = "127.0.0.1"
PORT = 8080


def get_request_line(request):
    # The request line is the first line. Lines are separated by "\n"
    return request.split("\n")[0]

def build_response():
    # -- Generate the response message. It has the following lines
    # Status line
    # header
    # blank line
    # Body (content to send)

    body = "Hello from my first web server!\n"

    # -- Status line: We respond that everything is ok (200 code)
    status_line = "HTTP/1.1 200 OK\n"
    # -- Add the Content-Type header
    header = "Content-Type: text/plain\n"
    header += f"Content-Length: {len(body)}\n"

    # -- Build the message by joining together all the parts
    return status_line + header + "\n" + body


def process_client(s):
    # -- Receive the request message
    req_raw = s.recv(2048)
    req = req_raw.decode()

    print("Message FROM CLIENT: ")
    request_line = get_request_line(req)
    termcolor.cprint(request_line, "green")

    response_msg = build_response()
    cs.send(response_msg.encode())


# -------------- MAIN PROGRAM
# ------ Configure the server
# -- Listening socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Setup up the socket's IP and PORT
ls.bind((IP, PORT))

# -- Become a listening socket
ls.listen()

print("Echo server configured!")

# --- MAIN LOOP
while True:
    print("Waiting for clients....")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped!")
        ls.close()
        exit()
    else:

        # Service the client
        process_client(cs)

        # -- Close the socket
        cs.close()
