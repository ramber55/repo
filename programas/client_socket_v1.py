import socket

# SERVER IP, PORT
# Write here the correct parameter for connecting to the
# Local host
PORT = 999
IP = "127.0.0.1"


# First, create the socket
# We will always use these parameters: AF_INET y SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish the connection to the Server (IP, PORT)
s.connect((IP, PORT))

# Send data. No strings can be sent, only bytes
# It necesary to encode the string into bytes
s.send(str.encode("HELLO FROM THE CLIENT!!!"))

msg = s.recv(2048).decode("utf-8")
print("Message from server: {}".format(msg))

# Close the socket
s.close()
