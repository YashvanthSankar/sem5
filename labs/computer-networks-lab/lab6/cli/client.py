# Name: YASHVANTH S | Roll: CS24I1029
# CLI practice: send/receive MP4 files through the Lab 6 server.
import os
import socket
import threading
import time

HOST, PORT = "127.0.0.1", 18080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("rb")  # text headers and raw video bytes


def send(text):
    client.sendall((text + "\n").encode())


def receive(header):
    _, sender, packet, total, size, filename = header.split(" ", 5)
    packet, total, size = int(packet), int(total), int(size)
    path = f"received_from_{sender}_{os.path.basename(filename)}"
    received = 0
    with open(path, "wb") as file:
        for _ in range(total):
            data = reader.read(min(packet, size - received))
            if not data:
                break
            file.write(data)
            received += len(data)
    got = (received + packet - 1) // packet
    print(f"\nSaved {path}: {received}/{size} bytes, {got}/{total} packets")


def listen():
    while True:
        header = reader.readline().decode().strip()
        if not header:
            print("\nServer disconnected")
            return
        if header.startswith("VIDEO "):
            receive(header)
        else:
            print("\n" + header)


while True:
    name = input("Username: ").strip()
    send(name)
    answer = reader.readline().decode().strip()
    print(answer)
    if answer.startswith("OK "):
        break

threading.Thread(target=listen, daemon=True).start()
print("Commands: users, send, exit")
while True:
    command = input("> ").strip().lower()
    if command == "users":
        send("/users")
    elif command == "send":
        to = input("Receiver: ").strip()
        path = input("MP4 path: ").strip()
        try:
            packet = int(input("Packet size (e.g. 4096): "))
            delay = float(input("Delay in seconds (e.g. 0.001): "))
            if not path.lower().endswith(".mp4") or packet <= 0 or delay < 0:
                raise ValueError
            size = os.path.getsize(path)
        except (ValueError, OSError):
            print("Choose an existing MP4, positive packet size and nonnegative delay")
            continue
        total = (size + packet - 1) // packet
        send(f"VIDEO {name} {to} {packet} {total} {size} {delay} {path}")
        with open(path, "rb") as file:
            for _ in range(total):
                client.sendall(file.read(packet))
                time.sleep(delay)
        print(f"Sent {total} packets; wait for server result")
    elif command == "exit":
        send("/exit")
        break
    else:
        print("Type users, send or exit")
client.close()
