import socket

# Configure the Server's IP and PORT
PORT = 8080
# IP = "127.0.0.1"  # This local host. With this IP, the socket is visible just locally.
# On the other hand, setting IP this way, in most platforms make to
# bypass some protocol stack layers.
IP = socket.gethostbyname(socket.gethostname())  # Using this way, remote connections are accepted (and this
# socket server is visible from the outside world) but not the local ones

MAX_OPEN_REQUESTS = 5

# Counting the number of connections
number_con = 0

print("hostname:", socket.gethostname())

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    # become a server socket. server socket mission is just listening incoming connection
    # requests. It is not used to send or receive data. Once a connection request is
    # accepted (see bellow) a client socket is created for the message interchange with
    # the other side.
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print("Waiting for connections at {}, {} ".format(IP, PORT))
        # When a connection is created, a new socket (called clientsocket) is created to
        # handle the just established connection! (meanwhile our serverconnection is still
        # waiting for new connection requests):
        (clientsocket, address) = serversocket.accept()

        # Another connection!e
        number_con += 1

        # Print the conection number
        print("CONNECTION: {}. From the IP: {}".format(number_con, address))

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        # Send the messag
        message = "Hello from the uncle's server\n"
        send_bytes = str.encode(message)
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()

except socket.error:
    print("Problems using port {}. Do you have permission?".format(PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()
