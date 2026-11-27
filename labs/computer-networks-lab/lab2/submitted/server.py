import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST="0.0.0.0"
PORT=5000
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is waiting for a connection...")

client_socket, client_address =  server_socket.accept()

print("Client connected")
print("Client socket address: ", client_address)

text = client_socket.recv(1024).decode('utf-8')

print("Text received: ", text)
text_lowercase = text.lower()
print("Lowercase text: ", text_lowercase)

client_socket.send(text_lowercase.encode('utf-8'))
print("Text sent to client:", text_lowercase)

client_socket.close()
server_socket.close()

print("Server closed.")

