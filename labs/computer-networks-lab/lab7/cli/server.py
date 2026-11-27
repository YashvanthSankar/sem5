# Name: YASHVANTH S | Roll: CS24I1029
# Two-player Rock–Paper–Scissors. One server thread handles each player.
import random
import socket
import threading
from datetime import datetime

HOST, PORT = "127.0.0.1", 18080  # use your real IPv4 for the exam network
names, waiting = set(), []        # used names; players waiting in FIFO order
lock = threading.Lock()


def show(message):
    print(message)


class Player:
    def __init__(self, conn, addr):
        self.conn, self.addr = conn, addr
        self.name, self.peer, self.choice = "", None, ""

    def send(self, text):
        self.conn.sendall((text + "\n").encode())


def pair(player):
    waiting.append(player)
    if len(waiting) == 1:
        player.send("WAIT Waiting for another player")
    else:
        a, b = waiting.pop(0), waiting.pop(0)
        a.peer, b.peer = b, a
        a.choice = b.choice = ""
        a.send(f"START {b.name}")
        b.send(f"START {a.name}")
        show(f"[GAME] {a.name} vs {b.name}")


def play(player, choice):
    if not player.peer or choice not in ("rock", "paper", "scissors") or player.choice:
        return
    player.choice = choice
    other = player.peer
    if not other.choice:
        player.send("WAIT Waiting for opponent's choice")
        return
    if choice == other.choice:
        result = "Draw"
    elif (choice, other.choice) in (("rock", "scissors"), ("paper", "rock"),
                                    ("scissors", "paper")):
        result = f"{player.name} wins"
    else:
        result = f"{other.name} wins"
    for p in (player, other):
        p.send(f"RESULT {player.name} chose {choice}; {other.name} chose "
               f"{other.choice}. {result}! REPLAY or EXIT")
        p.peer = None
    show(f"[END] {result}: {player.name}={choice}, {other.name}={other.choice}")


def handle(conn, addr):
    p = Player(conn, addr)
    reader = conn.makefile("r")     # readline() reads one complete command
    joined = None
    try:
        for line in reader:          # keep asking until the name is free
            line = line.strip()
            with lock:
                if line == "RANDOM":
                    name = f"player{random.randint(100, 999)}"
                else:
                    name = line.removeprefix("NAME ").strip()
                while line == "RANDOM" and name in names:
                    name = f"player{random.randint(100, 999)}"
                if name and name not in names:
                    names.add(name)
                    p.name = name
                    break
            p.send("TAKEN Choose another name or type random")
        if not p.name:
            return
        joined = datetime.now()
        p.send(f"OK {p.name}")
        show(f"[JOIN] {p.name} {addr}")
        with lock:
            pair(p)
        for line in reader:
            command, _, value = line.strip().partition(" ")
            with lock:             # shared waiting list and pairs
                if command == "CHOICE":
                    play(p, value)
                elif command == "CHAT" and p.peer:
                    p.peer.send(f"CHAT {p.name}: {value}")
                elif command == "REPLAY" and not p.peer and p not in waiting:
                    pair(p)
                elif command == "EXIT":
                    break
    except OSError:
        pass
    finally:
        with lock:
            names.discard(p.name)
            if p in waiting:
                waiting.remove(p)
            if p.peer:              # leaving during a game makes the other player win
                try:
                    p.peer.send(f"RESULT {p.name} left; {p.peer.name} wins! REPLAY or EXIT")
                except OSError:
                    pass
                p.peer.peer = None
        conn.close()
        if joined:
            show(f"[LEAVE] {p.name} {addr} | duration {datetime.now() - joined}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
show(f"Listening on {server.getsockname()}")
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
