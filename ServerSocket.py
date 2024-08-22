# Program to create a server to handle multiple clients.

import threading
import socket

host = 'localhost' #You should specify the IP of the server
port = 3690
server = socket.socket()
server.bind((host, port))
server.listen()
clients = []
names = []

def broadcast(message, name):
	for client in clients:
		client.send(f'{name}: {message}'.encode('utf-8'))

def handle_client(client):
	while True:
		try:
			message = client.recv(1024).decode('utf-8')
			broadcast(message, names[clients.index(client)])
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			name = names[index]
			broadcast(bytes(f'{name} has left!', 'utf-8'), 'Server')
			names.remove(name)
			break

def receive():
	while True:
		print('Server is running...')
		client, address = server.accept()
		print(f'Connection is established with {str(address)}')
		name = client.recv(1024).decode('utf-8')
		names.append(name)
		clients.append(client)
		print(f'The name of this client is {name}')
		client.send(('You are now Connected').encode('utf-8'))
		client_thread = threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
	receive()
