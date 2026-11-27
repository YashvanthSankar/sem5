# Name: YASHVANTH S | Roll: CS24I1029
# First socket program: one client sends one short message.
import socket

HOST = "127.0.0.1"  # practice only; use your LAN IPv4 in the exam
PORT = 18080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # restart quickly
server.bind((HOST, PORT))
server.listen(1)
print("Server:", server.getsockname(), "waiting for a client")

conn, addr = server.accept()
print("Client:", addr)
message = conn.recv(1024).decode()
print("Received:", message)
conn.sendall(("echo: " + message).encode())

conn.close()
server.close()
