import sys
import socket
import threading

# Global Constants
IP = "127.0.0.1"
MAX_OPEN_REQUESTS = 5


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
            print(f"Waiting for connections at {local_port}")
            # waiting for new connections:
            (clientsocket, address) = serversocket.accept()

            # Read the message from the client, if any
            msg = clientsocket.recv(2048).decode("utf-8")
            print("Recived Message> {}".format(msg))
            clientsocket.close()
    except socket.error:
        print("Problems using port {}. Do you have permission?".format(local_port))

    except KeyboardInterrupt:
        print("User Interruption. Message Listener exiting.")
        serversocket.close()


def message_sender(remote_port):
    try:
        while True:
            message_to_send = input("Your Message>")
            if message_to_send != "":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # establish the connection to the remote side (IP, PORT)
                s.connect((IP, remote_port))

                # Send data. No strings can be sent, only bytes
                # It necesary to encode the string into bytes
                s.send(str.encode(message_to_send))

                # Close the socket
                s.close()
    except socket.error:
        print("Problems using port {}.".format(remote_port))

    except KeyboardInterrupt:
        print("User Interruption. Message Sender exiting.")
        s.close()


# MAIN PROGRAM
LOCAL_PORT, REMOTE_PORT = get_ports_from_args()
print(f"Listening at {LOCAL_PORT} Messages to be sent to {REMOTE_PORT} ...")

receiver_thread = threading.Thread(name='receiver', target=message_receiver, args=(LOCAL_PORT,))
sender_thread = threading.Thread(name='sender', target=message_sender, args=(REMOTE_PORT,))








