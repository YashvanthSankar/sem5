# CS24I1029
# YASHVANTH S

import socket
import time
import os

SERVER_IP = "172.16.14.26"
PORT = 6000

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    print("\nServer address:", client.getpeername())
    print("Client address:", client.getsockname())

    username = client.recv(1024).decode()
    print("Assigned username:", username)

    filename = input("Enter file name: ")

    if not os.path.isfile(filename):
        print("File not found.")
        client.close()
        continue

    client.send(filename.encode())

    status = client.recv(1024).decode()
    print("Server status:", status)

    if status == "File already exists":
        client.close()
        choice = input("Try another file? (y/n): ")
        if choice.lower() == "y":
            continue
        break

    with open(filename, "rb") as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            client.sendall(data)
            time.sleep(0.05)

    client.shutdown(socket.SHUT_WR)

    confirmation = client.recv(1024).decode()
    print("Server confirmation:", confirmation)

    client.close()
    break

