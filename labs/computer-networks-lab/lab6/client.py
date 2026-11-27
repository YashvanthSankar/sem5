# Name: YASHVANTH S | Roll: CS24I1029
# The listener receives videos while a separate thread sends your video.
import os
import queue
import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog, ttk

HOST, PORT = "127.0.0.1", 18080  # change HOST to the server's IPv4
client, reader, my_name = None, None, ""
updates = queue.Queue()             # network threads -> Tkinter window
send_lock = threading.RLock()       # keep a whole outgoing video together


def send(text):
    with send_lock:
        client.sendall((text + "\n").encode())


def line():
    return reader.readline().decode().strip()


def receive(header):
    _, sender, packet, total, size, filename = header.split(" ", 5)
    packet, total, size = int(packet), int(total), int(size)
    saved = f"received_from_{sender}_{os.path.basename(filename)}"
    received = 0
    with open(saved, "wb") as file:
        for number in range(total):
            data = reader.read(min(packet, size - received))
            if not data:
                break
            file.write(data)
            received += len(data)
            updates.put(("receive", (number + 1) * 100 / total))
    got = (received + packet - 1) // packet
    updates.put(("text", f"{sender}: {filename} saved as {saved}; original {size} bytes, "
                         f"received {received} bytes, packets {got}/{total}, loss {total - got}"))


def listen():
    while True:
        message = line()
        if not message:
            updates.put(("text", "Disconnected"))
            break
        if message.startswith("VIDEO "):
            receive(message)
        elif message.startswith("USERS "):
            updates.put(("users", message[6:].split(",")))
        else:
            updates.put(("text", message))


def send_video(to, path, packet, delay):
    size = os.path.getsize(path)
    total = (size + packet - 1) // packet
    started = time.time()
    with send_lock, open(path, "rb") as file:
        send(f"VIDEO {my_name} {to} {packet} {total} {size} {delay} {path}")
        for number in range(total):
            client.sendall(file.read(packet))
            updates.put(("send", (number + 1) * 100 / total))
            time.sleep(delay)
    updates.put(("text", f"Sent {total} packets in {time.time() - started:.2f}s"))


def connect():
    global client, reader, my_name
    if client is None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        reader = client.makefile("rb")
        show(f"Client {client.getsockname()} | Server {client.getpeername()}")
    send(name_entry.get().strip())
    answer = line()
    show(answer)
    if answer.startswith("OK"):
        my_name = name_entry.get().strip()
        connect_button.config(state="disabled")
        threading.Thread(target=listen, daemon=True).start()
        send("/users")


def browse():
    path = filedialog.askopenfilename(filetypes=[("MP4 videos", "*.mp4")])
    if path:
        file_label.config(text=path)  # show the complete selected path


def start_send():
    if not my_name:
        return show("Connect first")
    path, to = file_label.cget("text"), users.get()
    try:
        packet, delay = int(packet_box.get()), float(delay_box.get())
        if (packet <= 0 or delay < 0 or not path.endswith(".mp4")
                or not os.path.isfile(path) or not to):
            raise ValueError
    except ValueError:
        return show("Choose a user, an .mp4 file, a positive packet size and a nonnegative delay")
    threading.Thread(target=send_video, args=(to, path, packet, delay), daemon=True).start()


def show(message):
    output.insert("end", message + "\n")
    output.see("end")


def refresh():
    while not updates.empty():
        kind, value = updates.get()
        if kind == "text":
            show(value)
        elif kind == "users":
            users["values"] = value
        elif kind == "send":
            send_bar["value"] = value
        elif kind == "receive":
            receive_bar["value"] = value
    root.after(100, refresh)


def leave():
    if client:
        send("/exit")
        client.close()
    root.destroy()


def refresh_users():
    if my_name:
        send("/users")
    else:
        show("Connect first")


root = tk.Tk()
root.title("Lab 6 Video Share - CS24I1029")
tk.Label(root, text="Username").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)
connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.grid(row=0, column=2)
tk.Label(root, text="Send to").grid(row=1, column=0)
users = ttk.Combobox(root)
users.grid(row=1, column=1)
tk.Button(root, text="Refresh users", command=refresh_users).grid(row=1, column=2)
tk.Button(root, text="Browse video", command=browse).grid(row=2, column=0)
file_label = tk.Label(root, text="No file selected", width=45)
file_label.grid(row=2, column=1, columnspan=2)
tk.Label(root, text="Packet size").grid(row=3, column=0)
packet_box = ttk.Combobox(root, values=[1024, 4096, 8192, 16384, 65536])
packet_box.set("4096")
packet_box.grid(row=3, column=1)
tk.Label(root, text="Delay (seconds)").grid(row=4, column=0)
delay_box = ttk.Combobox(root, values=[0, 0.001, 0.005, 0.01, 0.05])
delay_box.set("0.001")
delay_box.grid(row=4, column=1)
tk.Button(root, text="Send video", command=start_send).grid(row=4, column=2)
tk.Label(root, text="Sending").grid(row=5, column=0)
send_bar = ttk.Progressbar(root)
send_bar.grid(row=5, column=1, columnspan=2, sticky="ew")
tk.Label(root, text="Receiving").grid(row=6, column=0)
receive_bar = ttk.Progressbar(root)
receive_bar.grid(row=6, column=1, columnspan=2, sticky="ew")
output = tk.Text(root, width=65, height=10)
output.grid(row=7, column=0, columnspan=3)
tk.Button(root, text="Disconnect", command=leave).grid(row=8, column=0, columnspan=3)
root.protocol("WM_DELETE_WINDOW", leave)
refresh()
root.mainloop()
