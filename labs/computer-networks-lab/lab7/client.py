# Name: YASHVANTH S | Roll: CS24I1029
# Choose rock, paper or scissors after the server pairs two players.
import queue
import socket
import threading
import tkinter as tk

HOST, PORT = "127.0.0.1", 18080  # change HOST to the server's IPv4
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("r")
inbox = queue.Queue()


def send(text):
    client.sendall((text + "\n").encode())


def listen():
    for line in reader:              # messages can arrive without a button click
        inbox.put(line.strip())


def refresh():
    while not inbox.empty():
        message = inbox.get()
        if message.startswith("CHAT "):
            chat.insert("end", message[5:] + "\n")
        else:
            status.config(text=message)
    root.after(100, refresh)


def join(random_name=False):
    send("RANDOM" if random_name else "NAME " + name_entry.get().strip())
    reply = reader.readline().strip()
    status.config(text=reply)
    if reply.startswith("OK "):
        login.pack_forget()
        threading.Thread(target=listen, daemon=True).start()


def chat_now():
    message = chat_entry.get().strip()
    if message:
        send("CHAT " + message)
        chat.insert("end", "me: " + message + "\n")
        chat_entry.delete(0, "end")


def leave():
    send("EXIT")
    client.close()
    root.destroy()


root = tk.Tk()
root.title("Rock Paper Scissors - CS24I1029")
login = tk.Frame(root)
login.pack()
name_entry = tk.Entry(login)
name_entry.pack(side="left")
tk.Button(login, text="Join", command=join).pack(side="left")
tk.Button(login, text="Random name", command=lambda: join(True)).pack(side="left")
status = tk.Label(root, text="Enter a username", wraplength=400)
status.pack(pady=8)
main = tk.Frame(root)
main.pack()
game = tk.Frame(main)
game.pack(side="left")
for choice in ("rock", "paper", "scissors"):
    tk.Button(game, text=choice.title(), command=lambda c=choice: send("CHOICE " + c)).pack()
side = tk.Frame(main)
side.pack(side="left")
tk.Label(side, text="Chat with your opponent").pack()
chat = tk.Text(side, width=45, height=10)
chat.pack()
chat_entry = tk.Entry(side, width=45)
chat_entry.pack()
tk.Button(side, text="Send chat", command=chat_now).pack()
tk.Button(root, text="REPLAY", command=lambda: send("REPLAY")).pack()
tk.Button(root, text="EXIT", command=leave).pack()
root.protocol("WM_DELETE_WINDOW", leave)
refresh()
root.mainloop()
