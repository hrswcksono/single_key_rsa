import socket
import select
import sys
from threading import Thread
from des import *
from rsa import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 8081))
name = "ii"

d = des()
r = RSA()

counterRecv = 0

myKey = "AABB09182736CCDD"
friendPublicKey = ""

# print(privateKey, publicKey)

def send_msg(sock):
	while True:
		data = input()
		if(data == "send"):
			sock.send(r.send(myKey, friendPublicKey).encode())
		else:
			sock.send((name + ' ' + d.encrypt(data, myKey, 1)).encode())
		sys.stdout.flush()

def recv_msg(sock):
	
	while True:
		global counterRecv
		global friendPublicKey
		global friendKey
		if(counterRecv == 0):
			data = sock.recv(2048).decode()
			sys.stdout.write(data + '\n')
			counterRecv = 1
			friendPublicKey = data
			# print(friendPublicKey)
		else:
			data = sock.recv(2048).decode().partition(' ')
			name = data[0]
			message = data[2]
			sys.stdout.write(name + ' : ' + d.encrypt(message, myKey, 2) + '\n')

Thread(target=send_msg, args=(server,)).start()
# Thread(target=recv_msg, args=(server,)).start()

while True:
	sockets_list = [server]
	read_socket, write_socket, error_socket = select.select(sockets_list, [], [])
	for socks in read_socket:
		if socks == server:
			recv_msg(socks)
		else:
			send_msg(socks)

server.close()