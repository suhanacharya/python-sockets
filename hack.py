# write your code here
import sys
import socket
import itertools

args = sys.argv


# hostname, port, message = args[1], int(args[2]), args[3]
# Collect arguments from command-line
hostname, port = args[1], int(args[2])


def socket_connect():
	new_socket = socket.socket()
	address = hostname, port
	new_socket.connect(address)
	return new_socket


def generate_alphanumeric_list():
	letters = list(map(lambda x: chr(x), list(range(ord('a'), ord('z') + 1))))
	numbers = list(map(lambda x: str(x), list(range(0, 10))))
	return letters + numbers


def send_message(sock, message):
	message = message.encode(encoding="utf-8")
	sock.send(message)


def generate_combinations(string):
	# length = len(string)
	# string += string.upper()
	# string = list(string)
	# for item in itertools.combinations(string, length):
	# 	yield "".join(item)
	string = string.lower()
	mx = 2 ** len(string)

	# Using all subsequences and permuting them
	for i in range(mx):
		combination = [k for k in string]
		for j in range(len(string)):
			if ((i >> j) & 1) == 1:
				combination[j] = string[j].upper()

		yield "".join(combination)


def main():
	# passwords = []
	flag = 0
	new_socket = socket_connect()
	# with open("passwords.txt", "r", encoding="utf-8") as password_file:
	# 	for line in password_file:
			# passwords.append(line.rstrip("\n"))
	for password in passwords:
		#password = line.rstrip("\n")
		next_permutation = generate_combinations(password)
		for item in next_permutation:
			send_message(new_socket, item)
			response = new_socket.recv(1024).decode()
			if response == "Connection success!":
				if response == "Connection success!":
					flag = 1
					print(item)
					break
		if flag:
			break

	new_socket.close()
	# passwords.append(password_file.readline())
	# print(passwords)
	# new_socket = socket_connect()
	# flag = 0
	# alphanumeric = generate_alphanumeric_list()
	#
	# for x in range(1, len(alphanumeric) + 1):
	#     # password_gen = itertools.combinations_with_replacement(alphanumeric, x)
	#     for item in itertools.combinations_with_replacement(alphanumeric, x):
	#         password = "".join(item)
	#         send_message(new_socket, password)
	#         response = new_socket.recv(1024).decode()
	#         if response == "Connection success!":
	#             flag = 1
	#             print(password)
	#             break
	#     if flag:
	#         break
	#
	# new_socket.close()


main()
