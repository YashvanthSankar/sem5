# Name: YASHVANTH S | Roll: CS24I1029
# Lab 3 Server: many clients (one thread each) add words to ONE shared string.
import socket
import threading

HOST = "127.0.0.1"  # exam: your IPv4
PORT = 18080

words = []                  # the "global string", kept as a list; shown joined with commas
active = 0                  # number of connected clients
lock = threading.Lock()     # protects words and active (shared by all threads)


def handle(conn, addr):
    global active
    with lock:
        active += 1
        print(f"[JOIN]  {addr} | active connections = {active}")

    try:
        reader = conn.makefile("r")
        for line in reader:
            word = line.strip()
            if word == "exit":
                break
            with lock:
                if word and word not in words:
                    words.append(word)
                reply = ",".join(words)
            print(f"{addr} sent '{word}' -> string is now '{reply}'")
            conn.sendall((reply + "\n").encode())
    finally:
        conn.close()
        with lock:
            active -= 1
            print(f"[LEAVE] {addr} | active connections = {active}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print("Server listening on", server.getsockname())

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
