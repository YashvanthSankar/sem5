# Name: YASHVANTH S | Roll: CS24I1029
# Lab 4 Server: threaded file uploads with usernames and a log.
import os
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"  # exam: your IPv4
PORT = 18080
SAVE_DIR = "uploads"

USER_FILE = "usernames.txt"
try:
    with open(USER_FILE) as f:
        known_users = set(f.read().splitlines())
except FileNotFoundError:
    known_users = set()
active = 0
lock = threading.Lock()
os.makedirs(SAVE_DIR, exist_ok=True)


def send_line(conn, text):
    conn.sendall((text + "\n").encode())


def log(text):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with lock:
        with open("server_log.txt", "a") as f:
            f.write(f"[{stamp}] {text}\n")


def handle(conn, addr):
    global active
    reader = conn.makefile("rb")

    # 1. Identify this client.
    old = reader.readline().decode().strip()
    if not old:
        conn.close()
        return
    with lock:
        if old in known_users:
            username = old
        else:
            username = f"user{len(known_users) + 1}"
            known_users.add(username)
            with open(USER_FILE, "a") as f:
                f.write(username + "\n")
        active += 1
        print(f"[JOIN]  {addr} -> {username} | active connections = {active}")
    try:
        send_line(conn, username)
        # 2. Receive a filename. An empty line means quit.
        while True:
            filename = os.path.basename(reader.readline().decode().strip())
            if not filename:
                break
            saved_name = f"{username}_{filename}"
            path = os.path.join(SAVE_DIR, saved_name)
            info = (f"ServerSocket: {conn.getsockname()}, ClientSocket: {addr}, "
                    f"Username: {username}, File: {saved_name}")
            print(f"{username} requested '{filename}'")

            if os.path.exists(path):
                send_line(conn, "File already exists")
                print("  status: File already exists -> Rejected")
                log(info + ", Action: Rejected")
                continue

            # 3. Tell the client to send the file size and bytes.
            send_line(conn, "READY")
            print("  status: READY")
            size = int(reader.readline())
            remaining = size
            with open(path, "wb") as f:
                while remaining:
                    chunk = reader.read(min(1024, remaining))
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)

            if remaining:
                os.remove(path)
                log(info + ", Action: Rejected (incomplete upload)")
                break

            send_line(conn, f"Upload Complete for {saved_name}")
            print(f"  status: Accepted, {size} bytes saved as {saved_name}")
            log(info + f", Action: Accepted, Size: {size} bytes")
            break
    finally:
        conn.close()
        with lock:
            active -= 1
            print(f"[LEAVE] {addr} ({username}) | active connections = {active}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print("Server listening on", server.getsockname())

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
