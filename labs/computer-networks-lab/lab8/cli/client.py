# Name: YASHVANTH S | Roll: CS24I1029
# CLI practice: server sends questions and checks the answers.
import socket

HOST, PORT = "127.0.0.1", 18080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("r")


def send(text):
    client.sendall((text + "\n").encode())


while True:
    send(input("Username: ").strip())
    reply = reader.readline().strip()
    print(reply)
    if reply.startswith("OK "):
        break

while True:
    count = int(reader.readline().split()[1])  # QUESTIONS 5
    answers = []
    for number in range(1, count + 1):
        question, *options = reader.readline().strip().split("|")
        print(f"\nQ{number}. {question}")
        for letter, option in zip("ABCD", options):
            print(f"{letter}. {option}")
        while True:
            choice = input("Answer A/B/C/D, or - to skip: ").strip().upper()
            if choice in ("A", "B", "C", "D", "-"):
                answers.append(choice)
                break
    send("ANSWERS " + ",".join(answers))
    print(reader.readline().strip())  # SCORE comes from the server
    again = input("Replay? (y/n): ").strip().lower() == "y"
    send("REPLAY" if again else "EXIT")
    if not again:
        break
client.close()
