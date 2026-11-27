# Name: YASHVANTH S | Roll: CS24I1029
# Lab 4 Client: upload one file in small, delayed chunks.
import os
import socket
import time

HOST = "127.0.0.1"  # the SERVER's IPv4
PORT = 18080
CHUNK = 1024        # bytes per chunk
DELAY = 0.01        # seconds between chunks (shows several clients uploading together)


def send_line(sock, text):
    sock.sendall((text + "\n").encode())


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Client socket:", client.getsockname(), "| Server socket:", client.getpeername())
reader = client.makefile("rb")

# 1. Get a new username, or reuse one from an earlier run.
old = input("Your old username (press Enter if first time): ").strip()
send_line(client, old or "NEW")
username = reader.readline().decode().strip()
print("Username assigned by server:", username)

# 2. Ask for a file until the server accepts it or you quit.
while True:
    path = input("File to upload (Enter to exit): ").strip()
    if not path:
        send_line(client, "")
        break
    if not os.path.isfile(path):
        print("No such file on this computer, try again.")
        continue

    send_line(client, os.path.basename(path))
    status = reader.readline().decode().strip()
    print("Server status:", status)
    if status != "READY":
        print("Rejected. Try a different file, or press Enter to exit.")
        continue

    # 3. Send the size first, then the actual file bytes.
    size = os.path.getsize(path)
    send_line(client, str(size))
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            client.sendall(chunk)
            time.sleep(DELAY)
    print(f"Sent {size} bytes")
    print("Server says:", reader.readline().decode().strip())
    break

client.close()
print("Disconnected")
