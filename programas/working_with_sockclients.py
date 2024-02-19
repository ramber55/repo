import my_sockets

IP = my_sockets.LOCAL_IP
PORT = 8080

s = my_sockets.CLIENTSOCKET(my_sockets.get_current_ip(), PORT)
print("Socket Info:", s)

answer = s.talk("hola desde el cliente")
print("respuesta:", answer)

