import socket

LOCAL_IP = "127.0.0.1"
MAX_OPEN_REQUESTS = 5


class CLIENTSOCKET:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"Connection to SERVER at {self.ip}, PORT: {self.port}"

    def talk(self, message_to_send):
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # establishes the connection to the remote side (IP, PORT)
        clientsock.connect((self.ip, self.port))

        # Sends data (after encoding).+
        clientsock.send(str.encode(message_to_send))

        # Waits for an answer:
        received_msg = clientsock.recv(2048).decode("utf-8")

        clientsock.close()

        return received_msg


def get_current_ip():
    return socket.gethostbyname(socket.gethostname())



