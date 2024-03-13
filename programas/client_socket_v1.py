import socket

# SERVER IP, PORT
# Write here the correct parameter for connecting to the
# Local host
PORT = 8081
IP = "127.0.0.1"


# First, create the socket
# We will always use these parameters: AF_INET y SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish the connection to the Server (IP, PORT)
s.connect((IP, PORT))

# Send data. No strings can be sent, only bytes
# It necesary to encode the string into bytes
s.send(str.encode("HELLO FROM LEGANES!!!"))

# We receive the answer from the server.
# recv is blocked until a message is received
# from server.
msg = s.recv(2048).decode("utf-8")
print("Message from server: {}".format(msg))

# Close the socket to free resources and to let
# the server know that the communication is stopped
s.close()
