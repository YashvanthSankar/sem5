# Name: YASHVANTH S | Roll: CS24I1029
# Lab 8 Server: multiple-choice quiz. Server sends questions, client sends answers,
# SERVER checks them and calculates the score.
#
# client -> server : <username>               server -> client: OK / TAKEN
# server -> client : QUESTIONS <n>, then n lines "question|A|B|C|D"
# client -> server : ANSWERS A,C,-,B,...      ("-" = not answered)
# server -> client : SCORE <score>/<n> | <per-question result>
# client -> server : REPLAY  (questions are sent again)  or  EXIT
import socket
import threading
import time

HOST = "127.0.0.1"  # exam: your IPv4
PORT = 18080

QUESTIONS = [
    # (question, options A-D, correct letter)
    ("Which layer does TCP belong to?", ["Network", "Transport", "Session", "Data Link"], "B"),
    ("Default port of HTTP?", ["21", "25", "80", "443"], "C"),
    ("Which protocol gives IP addresses automatically?", ["DNS", "ARP", "DHCP", "FTP"], "C"),
    ("Which device works at layer 2?", ["Hub", "Switch", "Router", "Repeater"], "B"),
    ("What does DNS convert?", ["IP to MAC", "Name to IP", "MAC to IP", "Port to IP"], "B"),
]

names = set()
lock = threading.Lock()


def send(conn, text):
    conn.sendall((text + "\n").encode())


def run_quiz(conn, reader, name):
    display(f"[START] {name} started the quiz")
    start = time.time()
    send(conn, f"QUESTIONS {len(QUESTIONS)}")
    for q, options, _ in QUESTIONS:
        send(conn, q + "|" + "|".join(options))

    line = reader.readline().strip()               # "ANSWERS B,C,-,..."
    if not line:
        raise ConnectionError("player left during the quiz")
    answers = line.removeprefix("ANSWERS ").split(",")
    score, results = 0, []
    for i, (_, _, correct) in enumerate(QUESTIONS):
        given = answers[i] if i < len(answers) else "-"
        if given == correct:
            score += 1
            results.append(f"Q{i + 1} correct")
        else:
            results.append(f"Q{i + 1} wrong (answer {correct})")
    duration = time.time() - start
    display(f"[END] {name} answers={answers} score={score}/{len(QUESTIONS)} time={duration:.1f}s")
    send(conn, f"SCORE {score}/{len(QUESTIONS)} | " + ", ".join(results))


def handle(conn, addr):
    reader = conn.makefile("r")
    name = None
    try:
        for line in reader:                         # pick a free username
            line = line.strip()
            with lock:
                ok = line and line not in names
                if ok:
                    names.add(line)
            if ok:
                name = line
                break
            send(conn, "TAKEN Username exists, choose another")
        if not name:
            return
        send(conn, f"OK Welcome {name}")
        display(f"[JOIN] {name} {addr}")

        while True:
            run_quiz(conn, reader, name)
            if reader.readline().strip() != "REPLAY":
                break
    except (ConnectionError, OSError):
        pass
    finally:
        with lock:
            names.discard(name)
        conn.close()
        if name:
            display(f"[LEAVE] {name} {addr}")



def display(message):
    print(message)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
display(f"Server listening on {server.getsockname()}")
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
