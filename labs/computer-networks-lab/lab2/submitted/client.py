# CS24I1029
# YASHVANTH S

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_IP = input("Enter server's IP address: ")
SERVER_PORT = int(input("Enter server's port number: "))
client_socket.connect((SERVER_IP, SERVER_PORT))

print("Connected to the server!")

text = input("Enter some text: ")
client_socket.send(text.encode('utf-8'))
print("Text sent to server: ", text)

response = client_socket.recv(1024).decode('utf-8')
print("Server Response: ", response)
print("Client socket address: ",  client_socket.getsockname())

client_socket.close()
print("Client closed.")
