# Name: YASHVANTH S | Roll: CS24I1029
# Lab 3 Client: send one word at a time, print the server's latest string. "exit" quits.
import socket

HOST = "127.0.0.1"  # the SERVER's IPv4
PORT = 18080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Client:", client.getsockname(), "| Server:", client.getpeername())

reader = client.makefile("r")
while True:
    word = input("Word (exit to quit): ").strip()
    client.sendall((word + "\n").encode())
    if word == "exit":
        break
    print("Server string:", reader.readline().strip())

client.close()
