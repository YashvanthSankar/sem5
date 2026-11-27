# Name: YASHVANTH S | Roll: CS24I1029
import queue
import socket
import threading
import tkinter as tk

HOST = "127.0.0.1"  # exam: server's real IPv4
PORT = 18080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("r")
inbox = queue.Queue()
joined = False


def send(text):
    client.sendall((text + "\n").encode())


def show(text):
    output.insert("end", text + "\n")
    output.see("end")


def listen():
    for line in reader:
        inbox.put(line.strip())
        print(line.strip())


def refresh():
    while not inbox.empty():
        show(inbox.get())
    root.after(100, refresh)


def join():
    global joined
    name = name_entry.get().strip()
    if not name:
        return show("Enter a username")
    send(name)
    reply = reader.readline().strip()
    show(reply)
    if reply.startswith("OK"):
        joined = True
        join_button.config(state="disabled")
        threading.Thread(target=listen, daemon=True).start()


def message(to):
    text = msg_entry.get()
    if not joined or not to or not text:
        return show("Join, then enter a recipient and message")
    send(f"{to}:{text}")
    show(f"me -> {to}: {text}")
    msg_entry.delete(0, "end")


def users():
    if joined:
        send("/users")
    else:
        show("Join first")


def close():
    if joined:
        send("/exit")
    client.close()
    root.destroy()


root = tk.Tk()
root.title("Lab 5 Chat - CS24I1029")
login_row = tk.Frame(root)
login_row.pack()
tk.Label(login_row, text="Username").pack(side="left")
name_entry = tk.Entry(login_row)
name_entry.pack(side="left")
join_button = tk.Button(login_row, text="Join", command=join)
join_button.pack(side="left")

output = tk.Text(root, width=60, height=18)
output.pack()
row = tk.Frame(root)
row.pack()
tk.Label(row, text="To").pack(side="left")
to_entry = tk.Entry(row, width=12)
to_entry.pack(side="left")
tk.Label(row, text="Message").pack(side="left")
msg_entry = tk.Entry(row, width=30)
msg_entry.pack(side="left")

tk.Button(root, text="Users", command=users).pack()
tk.Button(root, text="Send", command=lambda: message(to_entry.get().strip())).pack()
tk.Button(root, text="Broadcast", command=lambda: message("broadcast")).pack()
tk.Button(root, text="Exit", command=close).pack()

addresses = f"Client socket: {client.getsockname()} | Server socket: {client.getpeername()}"
print(addresses)
show(addresses)
root.protocol("WM_DELETE_WINDOW", close)
refresh()
root.mainloop()
