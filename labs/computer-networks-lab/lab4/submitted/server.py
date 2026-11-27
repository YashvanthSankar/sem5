# CS24I1029
# YASHVANTH S

import socket
import threading
import os
from datetime import datetime

SERVER_IP = "172.16.14.28"
PORT = 5000

user_names = {}
active_clients = 0
lock = threading.Lock()


def save_log(client, username, filename, action, size=0):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("server_log.txt", "a") as log:
        log.write(f"[{time}] ServerSocket: {SERVER_IP}:{PORT}, "
                  f"ClientSocket: {client[0]}:{client[1]}, "
                  f"Username: {username}, File: {filename}, "
                  f"Action: {action}")
        if size:
            log.write(f", Size: {size} bytes")
        log.write("\n")


def handle_client(conn, client):
    global active_clients

    with lock:
        active_clients += 1
        username = user_names.setdefault(
            client[0], "user" + str(len(user_names) + 1)
        )

    conn.send(username.encode())
    print(f"\nConnected: {client} | Username: {username}")
    print("Active clients:", active_clients)

    try:
        filename = conn.recv(1024).decode()
        saved_file = username + "_" + os.path.basename(filename)

        print("Requested file:", filename)

        if os.path.exists(saved_file):
            conn.send(b"File already exists")
            save_log(client, username, saved_file, "Rejected")
            print("Status: File already exists")
            return

        conn.send(b"READY")
        print("Status: READY")

        size = 0
        with open(saved_file, "wb") as file:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                file.write(data)
                size += len(data)

        message = "Upload Complete for " + saved_file
        conn.send(message.encode())

        save_log(client, username, saved_file, "Accepted", size)
        print(message)

    finally:
        conn.close()
        with lock:
            active_clients -= 1
        print(f"Disconnected: {client}")
        print("Active clients:", active_clients)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))
server.listen(5)

print(f"Server running at {SERVER_IP}:{PORT}")

while True:
    conn, client = server.accept()
    threading.Thread(target=handle_client, args=(conn, client)).start()
