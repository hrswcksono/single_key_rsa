import socket
import select
import sys
from threading import Thread
from des import *
from rsa import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 8081)) #138.91.38.180
name = "hh"

d = des()
r = RSA()

p, q = 631, 311
encrypt = 78899
decrypt = r.getPrivateKey(r.totient(p, q), encrypt)
n = r.n(p,q)
publicKey = str(encrypt) + " " + str(n)
privateKey = str(decrypt) + " " + str(n)
counterRecv = 0

friendKey = ""

# print(privateKey, publicKey)

def send_msg(sock):
	while True:
		data = input()
		if(data == "start"):
			sock.send(publicKey.encode())
		else:
			sock.send((name + ' ' + d.encrypt(data, friendKey, 1)).encode())
		sys.stdout.flush()

def recv_msg(sock):
	
	while True:
		global counterRecv
		global friendPublicKey
		global friendKey
		if(counterRecv == 0):
			data = sock.recv(2048).decode()
			# print(data)
			friendKey = r.receive(data, privateKey)
			# print(friendKey)
			counterRecv = 1
		else:
			data = sock.recv(2048).decode().partition(' ')
			name = data[0]
			message = data[2]
			sys.stdout.write(name + ' : ' + d.encrypt(message, friendKey, 2) + '\n')

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