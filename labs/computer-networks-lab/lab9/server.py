# Name: YASHVANTH S | Roll: CS24I1029
# Lab 9 Server: role-based file access. The SERVER decides what each role may do.
#
# client -> server : LOGIN <user> <password>        -> OK <role> <allowed ops> | DENIED
#                    LIST                           -> FILES <cat/file, ...>
#                    READ <category> <file>         -> OK <n> + n bytes | DENIED <why>
#                    UPLOAD <category> <file> <n> + n bytes   (new file)
#                    UPDATE <category> <file> <n> + n bytes   (existing file)
#                    EXIT
import os
import queue
import socket
import tkinter as tk
import threading
from datetime import datetime

HOST = "127.0.0.1"  # exam: your IPv4
PORT = 18080
ROOT = "server_files"

USERS = {                       # username: (password, role)
    "stud1": ("s123", "Student"),
    "fac1": ("f123", "Faculty"),
    "admin1": ("a123", "Administrator"),
}

# Each higher role = everything the lower role can do + more (set union |)
STUDENT = {("academic", "READ")}
FACULTY = STUDENT | {("academic", "UPLOAD"), ("academic", "UPDATE"), ("administrative", "READ")}
ADMIN = FACULTY | {("administrative", "UPLOAD"), ("administrative", "UPDATE")}
PERMISSIONS = {"Student": STUDENT, "Faculty": FACULTY, "Administrator": ADMIN}

lock = threading.Lock()

# preloaded files
for cat, files in {"academic": ["syllabus.txt", "timetable.txt"],
                   "administrative": ["budget.txt", "staff_list.txt"]}.items():
    os.makedirs(os.path.join(ROOT, cat), exist_ok=True)
    for f in files:
        path = os.path.join(ROOT, cat, f)
        if not os.path.exists(path):
            with open(path, "w") as fh:
                fh.write(f"This is {f} in the {cat} category.\n")


def log(user, role, op, target, result):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (f"[{stamp}] User: {user}, Role: {role}, Operation: {op}, "
            f"File: {target}, Result: {result}")
    display(line)
    with lock:
        with open("file_access_log.txt", "a") as f:
            f.write(line + "\n")


def send(conn, text):
    conn.sendall((text + "\n").encode())


def list_files(role):
    readable = {cat for cat, op in PERMISSIONS[role] if op == "READ"}
    return [f"{cat}/{f}" for cat in sorted(readable)
            for f in sorted(os.listdir(os.path.join(ROOT, cat)))]


def handle(conn, addr):
    reader = conn.makefile("rb")
    user, role = None, None
    display(f"[CONNECT] {addr}")

    # 1. login
    while not user:
        parts = reader.readline().decode().split()
        if not parts:
            conn.close()
            return
        if len(parts) == 3 and parts[0] == "LOGIN" and USERS.get(parts[1], (None,))[0] == parts[2]:
            user, role = parts[1], USERS[parts[1]][1]
            ops = sorted(f"{op}:{cat}" for cat, op in PERMISSIONS[role])
            send(conn, f"OK {role} " + " ".join(ops))
            log(user, role, "LOGIN", "-", "Allowed")
        else:
            send(conn, "DENIED Wrong username or password")
            log(parts[1] if len(parts) > 1 else "?", "-", "LOGIN", "-", "Denied")

    # 2. requests
    try:
        while True:
            parts = reader.readline().decode().split()
            if not parts or parts[0] == "EXIT":
                break
            op = parts[0]

            if op == "LIST":
                send(conn, "FILES " + ", ".join(list_files(role)))
                log(user, role, op, "-", "Allowed")
                continue
            if len(parts) < 3:
                send(conn, "ERROR Bad command")
                continue

            cat, name = parts[1], os.path.basename(parts[2])
            path = os.path.join(ROOT, cat, name)
            data = b""
            if op in ("UPLOAD", "UPDATE"):
                if len(parts) != 4 or not parts[3].isdigit():
                    send(conn, "ERROR Bad file size")
                    continue
                size = int(parts[3])
                data = reader.read(size)  # read even when access will be denied
                if len(data) != size:
                    log(user, role, op, f"{cat}/{name}", "Denied (incomplete file)")
                    break

            if (cat, op) not in PERMISSIONS[role]:      # <- the access-control check
                send(conn, f"DENIED {role} cannot {op} in {cat}")
                log(user, role, op, f"{cat}/{name}", "Denied")
            elif op == "READ":
                if os.path.isfile(path):
                    with open(path, "rb") as f:
                        content = f.read()
                    send(conn, f"OK {len(content)}")
                    conn.sendall(content)
                    log(user, role, op, f"{cat}/{name}", "Allowed")
                else:
                    send(conn, "ERROR No such file")
                    log(user, role, op, f"{cat}/{name}", "Denied (file missing)")
            elif op == "UPLOAD" and os.path.exists(path):
                send(conn, "ERROR File exists, use UPDATE")
                log(user, role, op, f"{cat}/{name}", "Denied (file exists)")
            elif op == "UPDATE" and not os.path.exists(path):
                send(conn, "ERROR No such file, use UPLOAD")
                log(user, role, op, f"{cat}/{name}", "Denied (file missing)")
            else:                                       # allowed UPLOAD / UPDATE
                with open(path, "wb") as f:
                    f.write(data)
                send(conn, f"OK {op} done: {cat}/{name} ({len(data)} bytes)")
                log(user, role, op, f"{cat}/{name}", f"Allowed (file modified, {len(data)} bytes)")
    except ConnectionError:
        pass

    log(user, role, "DISCONNECT", "-", "-")
    conn.close()



# All server threads send display text to the Tk main thread.
events = queue.Queue()

def display(message):
    print(message)
    events.put(message)

def refresh():
    while not events.empty():
        output.insert("end", events.get() + "\n")
        output.see("end")
    root.after(100, refresh)

def accept_clients():
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
display(f"Server listening on {server.getsockname()}")

threading.Thread(target=accept_clients, daemon=True).start()
root = tk.Tk()
root.title("Lab 9 Server - CS24I1029")
output = tk.Text(root, width=85, height=22)
output.pack(padx=8, pady=8)
refresh()
root.mainloop()
