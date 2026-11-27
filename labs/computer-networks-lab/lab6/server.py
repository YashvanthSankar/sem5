# Name: YASHVANTH S | Roll: CS24I1029
# Send each video from one client to another, a packet at a time.
import csv
import os
import socket
import threading
import time

HOST, PORT = "127.0.0.1", 18080  # use your real IPv4 for the exam network
clients = {}                       # username -> socket
addresses = {}                     # username -> socket address
send_locks = {}                    # keep messages/files on one socket in order
lock = threading.Lock()


def send(conn, text):
    with send_locks[conn]:
        conn.sendall((text + "\n").encode())


def show_users():
    with lock:
        print("Active users =", len(clients))
        for name in clients:
            print(addresses[name], name)


def transfer(name, conn, reader, line):
    # Header: VIDEO sender receiver packet_size packet_count file_size delay filename
    _, _, to, packet, total, size, delay, filename = line.split(" ", 7)
    packet, total, size = int(packet), int(total), int(size)
    with lock:
        receiver = clients.get(to)
    started = time.time()
    got = 0
    if receiver:
        send_locks[receiver].acquire()       # one complete video at a time
        send(receiver, f"VIDEO {name} {packet} {total} {size} {filename}")
    try:
        for _ in range(total):
            data = reader.read(min(packet, size - got * packet))
            if not data:
                break
            got += 1
            if receiver:
                receiver.sendall(data)  # offline packets are simply discarded
    finally:
        if receiver:
            send_locks[receiver].release()

    seconds = round(time.time() - started, 3)
    loss = total - got
    print(f"{name} -> {to}: {filename}, server {got}/{total} packets, loss {loss}, {seconds}s")
    with lock, open("video_log.csv", "a", newline="") as file:
        new_file = file.tell() == 0
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["sender", "receiver", "file", "packet_size", "delay_s",
                             "packets_sent", "packets_server", "server_loss", "seconds"])
        writer.writerow([name, to, filename, packet, delay, total, got, loss, seconds])
    send(conn, f"INFO Server got {got}/{total} packets (loss {loss})" if receiver
         else f"ERROR User Not Online ({to})")


def handle(conn, addr):
    send_locks[conn] = threading.RLock()
    reader = conn.makefile("rb")   # bytes mode: text commands plus video bytes
    name = ""
    try:
        while not name:
            wanted = reader.readline().decode().strip()
            if not wanted:
                return
            with lock:
                if wanted not in clients:
                    clients[wanted], addresses[wanted] = conn, addr
                    name = wanted
            if not name:
                send(conn, "TAKEN Choose another username")
        send(conn, f"OK Welcome {name}")
        print("JOIN", name, addr)
        show_users()
        while True:
            line = reader.readline().decode().strip()
            if not line or line == "/exit":
                break
            if line == "/users":
                with lock:
                    users = ",".join(clients)
                send(conn, "USERS " + users)
            elif line.startswith("VIDEO "):
                transfer(name, conn, reader, line)
    except (OSError, ValueError):
        pass
    finally:
        if name:
            with lock:
                clients.pop(name, None)
                addresses.pop(name, None)
            print("LEAVE", name, addr)
            show_users()
        conn.close()
        send_locks.pop(conn, None)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print("Listening on", server.getsockname())
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
