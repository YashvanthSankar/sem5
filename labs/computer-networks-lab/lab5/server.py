# Name: YASHVANTH S | Roll: CS24I1029
import queue
import socket
import threading
import tkinter as tk
from datetime import datetime

HOST = "127.0.0.1"  # exam: your real IPv4
PORT = 18080
clients = {}              # socket -> username
lock = threading.Lock()
events = queue.Queue()    # server threads -> GUI

def send(conn, text):
    conn.sendall((text + "\n").encode())

def log(text):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] : {text}"
    with lock:
        with open("log.txt", "a") as file:
            file.write(line + "\n")
    events.put(line)

def show_users():
    with lock:
        lines = [f"Active users = {len(clients)}"]
        lines += [f"{sock.getpeername()} : {name}" for sock, name in clients.items()]
    text = "\n".join(lines)
    print(text)
    events.put(text)


def handle(conn, addr):
    reader = conn.makefile("r")
    address = f"{addr[0]}:{addr[1]}"
    name = None
    try:
        # Login: reject duplicate names until this client chooses a free one.
        while name is None:
            proposed = reader.readline().strip()
            if not proposed:
                return
            with lock:
                if proposed not in clients.values():
                    clients[conn] = proposed
                    name = proposed
            if name is None:
                send(conn, "TAKEN Username already in use")
                log(f"{address}, AttemptedUsername: {proposed}, "
                    "Status: Rejected (Username already in use)")

        joined = datetime.now()
        send(conn, f"OK Welcome {name}")
        log(f"{address}, Username: {name}, Activity: joined")
        show_users()

        # Chat: one line is one request.
        for raw in reader:
            line = raw.strip()
            if line == "/exit":
                break
            if line == "/users":
                with lock:
                    names = ", ".join(clients.values())
                send(conn, "USERS " + names)
                continue
            if ":" not in line:
                send(conn, "ERROR Use /users, name:msg, broadcast:msg or /exit")
                continue

            target, message = line.split(":", 1)
            target = target.strip("<> ")
            size = len(message.encode())
            with lock:
                receivers = [(sock, user) for sock, user in clients.items()
                             if sock != conn and (target == "broadcast" or user == target)]
            if not receivers and target != "broadcast":
                send(conn, "ERROR User Not Online")
                log(f"From: {name} ({address}), To: {target}, Size: {size}Bytes, "
                    "Status: Failed (User Not Online)")
            for other, other_name in receivers:
                try:
                    send(other, f"MSG {name}: {message}")
                    log(f"From: {name} ({address}), To: {other_name} "
                        f"({other.getpeername()}), Size: {size}Bytes, Status: Sent")
                except OSError:
                    log(f"From: {name} ({address}), To: {other_name}, "
                        f"Size: {size}Bytes, Status: Failed (Disconnected)")
    except OSError:
        pass
    finally:
        if name is not None:
            with lock:
                clients.pop(conn, None)
            duration = str(datetime.now() - joined).split(".")[0]
            log(f"{address}, Username: {name}, Activity: left, session_duration: [{duration}]")
            show_users()
        conn.close()


def accept_clients():
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()


def refresh():
    while not events.empty():
        output.insert("end", events.get() + "\n")
        output.see("end")
    root.after(100, refresh)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print("Server listening on", server.getsockname())
root = tk.Tk()
root.title("Lab 5 Server - CS24I1029")
output = tk.Text(root, width=85, height=22)
output.pack()
threading.Thread(target=accept_clients, daemon=True).start()
refresh()
root.mainloop()
