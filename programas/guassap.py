import sys
import socket
import threading
import termcolor

# Global Constants
IP = "127.0.0.1"
MAX_OPEN_REQUESTS = 5


class BCOLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_ports_from_args():
    try:
        local_port = 0
        if sys.argv[1] == "-l":
            local_port = int(sys.argv[2])
        elif sys.argv[3] == "-l":
            local_port = int(sys.argv[4])

        remote_port = 0
        if sys.argv[1] == "-r":
            remote_port = int(sys.argv[2])
        elif sys.argv[3] == "-r":
            remote_port = int(sys.argv[4])

        if local_port == 0 or remote_port == 0:
            print("Some port missing. Exiting.")
            exit()
    except ValueError:
        print(f"Ports must be integers: [{sys.argv[2]}] [{sys.argv[4]}]. Exiting", )
        exit(1)

    return local_port, remote_port


def message_receiver(local_port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Establishing Listening server at LOCAL_PORT:
        serversocket.bind((IP, local_port))
        serversocket.listen(MAX_OPEN_REQUESTS)

        while True:
            # accept connections from outside
            # print(f"Waiting for connections at {local_port}")
            # waiting for new connections:
            (clientsocket, address) = serversocket.accept()

            # Read the message from the client, if any
            msg = clientsocket.recv(2048).decode("utf-8")
            print("\nReceived Message> ", end=" ")
            print(BCOLORS.OKBLUE + msg + BCOLORS.ENDC)
            # termcolor.cprint(msg, "green")

            print("\nYour Message> ", end=" ")
            clientsocket.close()
    except socket.error:
        print("Problems using port {}. Do you have permission?".format(local_port))

    except KeyboardInterrupt:
        print("User Interruption. Message Listener exiting.")
        serversocket.close()
        exit()


def message_sender(remote_port):
    s = None
    try:
        while True:
            message_to_send = input("\nYour Message>")
            if message_to_send != "":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    # establish the connection to the remote side (IP, PORT)
                    s.connect((IP, remote_port))

                    # Send data. No strings can be sent, only bytes
                    # It necesary to encode the string into bytes
                    s.send(str.encode(message_to_send))

                    # Close the socket
                    s.close()
                except socket.error:
                    print("Problems using port {}. Probbably nobody is hearing. Message not sent.".format(remote_port))
                    s.close()

    except (EOFError, UnicodeDecodeError, KeyboardInterrupt):
        print("User Interruption. Message Sender exiting.")
        if s is not None:
            s.close()
        exit()


# MAIN PROGRAM

try:
    LOCAL_PORT, REMOTE_PORT = get_ports_from_args()
    print(f"Listening at {LOCAL_PORT} Messages to be sent to {REMOTE_PORT} ...")

    print("Creating Message Receiver")
    receiver_thread = threading.Thread(name='receiver', target=message_receiver, args=(LOCAL_PORT,))
    print("Starting Message Receiver")
    receiver_thread.start()

    print("Creating Message Sender")
    sender_thread = threading.Thread(name='sender', target=message_sender, args=(REMOTE_PORT,))
    print("Starting Message Receiver")
    sender_thread.start()

except KeyboardInterrupt:
    print("User Interruption. Exiting.")
    exit()
