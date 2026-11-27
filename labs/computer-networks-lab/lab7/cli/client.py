# Name: YASHVANTH S | Roll: CS24I1029
# CLI practice for the two-player Rock–Paper–Scissors game.
import socket
import threading

HOST, PORT = "127.0.0.1", 18080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("r")


def send(text):
    client.sendall((text + "\n").encode())


def listen():
    for line in reader:              # game/chat messages arrive at any time
        print("\n" + line.strip())


while True:
    name = input("Username (or 'random'): ").strip()
    send("RANDOM" if name.lower() == "random" else "NAME " + name)
    reply = reader.readline().strip()
    print(reply)
    if reply.startswith("OK "):
        break

threading.Thread(target=listen, daemon=True).start()
print("Commands: rock, paper, scissors, chat, replay, exit")
while True:
    command = input("> ").strip().lower()
    if command in ("rock", "paper", "scissors"):
        send("CHOICE " + command)
    elif command == "chat":
        send("CHAT " + input("Message: "))
    elif command == "replay":
        send("REPLAY")
    elif command == "exit":
        send("EXIT")
        break
    else:
        print("Choose rock/paper/scissors, chat, replay or exit")
client.close()
