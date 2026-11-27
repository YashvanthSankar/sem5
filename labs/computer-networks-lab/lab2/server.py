# Name: YASHVANTH S | Roll: CS24I1029
# Lab 2 Server: receive text from a client, send it back in lowercase.
import socket

HOST = "127.0.0.1"  # exam: your IPv4, e.g. "172.16.14.28"
PORT = 18080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print("Server socket address:", server.getsockname())

while True:                                    # serve clients one after another
    conn, addr = server.accept()
    print("\nClient socket address:", addr)

    text = conn.recv(1024).decode()
    print("Received:", text)

    result = text.lower()
    print("Operation: lowercase ->", result)

    conn.sendall(result.encode())
    print("Sent back:", result)
    conn.close()
