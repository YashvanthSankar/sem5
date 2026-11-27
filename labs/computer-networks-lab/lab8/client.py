# Name: YASHVANTH S | Roll: CS24I1029
# Lab 8 Client (Tkinter GUI quiz). Same protocol as client.py, same server.py.
# No thread needed: we only read from the server right after we ask for something.
import socket
import tkinter as tk

HOST = "127.0.0.1"  # the SERVER's IPv4
PORT = 18080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("r")

questions = []        # list of [question, A, B, C, D]
answers = []          # saved choice per question: "A".."D" or "-"
current = 0           # index of the question on screen
finished = False


def send(text):
    client.sendall((text + "\n").encode())


def load_questions():
    global questions, answers, current
    count = int(reader.readline().split()[1])          # "QUESTIONS 5"
    questions = [reader.readline().strip().split("|") for _ in range(count)]
    answers = ["-"] * count
    current = 0
    show_question()


def show_question():
    q = questions[current]
    q_label.config(text=f"Q{current + 1}/{len(questions)}. {q[0]}")
    for i, letter in enumerate("ABCD"):
        radios[i].config(text=f"{letter}) {q[i + 1]}")
    choice.set("" if answers[current] == "-" else answers[current])
    saved_label.config(text=f"Saved: {answers[current]}")


# ---------- button actions ----------
def login():
    send(name_entry.get().strip())
    reply = reader.readline().strip()
    result.config(text=reply)
    if reply.startswith("OK"):
        login_row.destroy()
        load_questions()


def save_choice():
    answers[current] = choice.get() or "-"
    saved_label.config(text=f"Saved: {answers[current]}")


def reset_choice():
    choice.set("")
    save_choice()


def move(step):                    # Prev = -1, Next = +1 (autosaves first)
    global current
    save_choice()
    current = max(0, min(len(questions) - 1, current + step))
    show_question()


def submit():
    global finished
    if finished or not questions:
        return
    save_choice()
    send("ANSWERS " + ",".join(answers))
    result.config(text=reader.readline().strip())     # server's score
    finished = True


def replay():
    global finished
    if not finished:
        return
    send("REPLAY")
    result.config(text="")
    load_questions()
    finished = False


def exit_quiz():
    send("EXIT")
    client.close()
    root.destroy()


# ---------- window ----------
root = tk.Tk()
root.title("Quiz - CS24I1029")

login_row = tk.Frame(root)
login_row.pack(pady=4)
tk.Label(login_row, text="Username").pack(side="left")
name_entry = tk.Entry(login_row)
name_entry.pack(side="left")
tk.Button(login_row, text="Start", command=login).pack(side="left")

q_label = tk.Label(root, text="Enter a username to start", font=("Arial", 14), wraplength=450)
q_label.pack(padx=10, pady=10)

choice = tk.StringVar()            # all 4 radio buttons share this, so only one can be picked
radios = []
for letter in "ABCD":
    r = tk.Radiobutton(root, text=letter, variable=choice, value=letter, anchor="w")
    r.pack(fill="x", padx=20)
    radios.append(r)
saved_label = tk.Label(root, text="")
saved_label.pack()

row = tk.Frame(root)
row.pack(pady=6)
for text, cmd in [("< Prev", lambda: move(-1)), ("Save choice", save_choice),
                  ("Reset choice", reset_choice), ("Next >", lambda: move(1)), ("Submit", submit)]:
    tk.Button(row, text=text, command=cmd).pack(side="left", padx=2)

result = tk.Label(root, text="", wraplength=450, fg="blue")
result.pack(pady=6)

end_row = tk.Frame(root)
end_row.pack(pady=4)
tk.Button(end_row, text="REPLAY", command=replay).pack(side="left", padx=4)
tk.Button(end_row, text="EXIT", command=exit_quiz).pack(side="left", padx=4)

root.protocol("WM_DELETE_WINDOW", exit_quiz)
root.mainloop()
