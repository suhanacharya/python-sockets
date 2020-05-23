# write your code here

import sys
import socket
args = sys.argv

hostname, port, message = args[1], int(args[2]), args[3]

new_socket = socket.socket()

address = hostname, port
new_socket.connect(address)
message = message.encode()
new_socket.send(message)
response = new_socket.recv(1024)
response = response.decode()
print(response)

new_socket.close()
