# Name: YASHVANTH S | Roll: CS24I1029
# Connect, send one short message, receive one reply.
import socket

HOST = "127.0.0.1"  # server's IPv4 in the exam
PORT = 18080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Client:", client.getsockname(), "Server:", client.getpeername())

client.sendall(input("Message: ").encode())
reply = client.recv(1024).decode()
print("Server replied:", reply)
client.close()
