# Name: YASHVANTH S | Roll: CS24I1029
# Lab 2 Client: send text, print the lowercase reply.
import socket

HOST = "127.0.0.1"  # the SERVER's IPv4 (your friend's IP for the network test)
PORT = 18080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Client socket address:", client.getsockname())
print("Server socket address:", client.getpeername())

text = input("Enter text: ")
client.sendall(text.encode())
print("Sent:", text)

reply = client.recv(1024).decode()
print("Received:", reply)
client.close()
