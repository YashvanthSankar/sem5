# Name: YASHVANTH S | Roll: CS24I1029
# Lab 9 Client (Tkinter GUI). Same protocol as client.py, same server.py.
# No thread needed: every button sends one request and reads one reply.
# Test users: stud1/s123 (Student), fac1/f123 (Faculty), admin1/a123 (Administrator)
import os
import socket
import tkinter as tk
from tkinter import filedialog, ttk

HOST = "127.0.0.1"  # the SERVER's IPv4
PORT = 18080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("rb")
logged_in = False


def send(text):
    client.sendall((text + "\n").encode())


def reply():
    return reader.readline().decode().strip()


def show(text):
    output.insert("end", text + "\n")
    output.see("end")


# ---------- button actions ----------
def login():
    global logged_in
    send(f"LOGIN {user_entry.get().strip()} {pass_entry.get().strip()}")
    r = reply()
    show(r)
    if r.startswith("OK"):
        logged_in = True
        role_label.config(text="Role: " + r.split()[1] + "   Allowed: " + " ".join(r.split()[2:]))
        list_files()


def list_files():
    if not logged_in:
        return show("Log in first")
    send("LIST")
    files = reply().removeprefix("FILES ").split(", ")    # ["academic/syllabus.txt", ...]
    file_list.delete(0, "end")
    for f in files:
        file_list.insert("end", f)


def read_file():
    if not logged_in:
        return show("Log in first")
    if not file_list.curselection():
        return show("Select a file first")
    category, name = file_list.get(file_list.curselection()).split("/")
    send(f"READ {category} {name}")
    r = reply()
    if r.startswith("OK"):
        content = reader.read(int(r.split()[1]))
        with open("downloaded_" + name, "wb") as f:
            f.write(content)
        show(f"--- {name} (saved as downloaded_{name}) ---\n{content.decode(errors='replace')}")
    else:
        show(r)                                      # DENIED / ERROR


def send_file(op):                                   # op = "UPLOAD" or "UPDATE"
    if not logged_in:
        return show("Log in first")
    path = filedialog.askopenfilename()
    if not path:
        return
    with open(path, "rb") as f:
        data = f.read()
    send(f"{op} {category_box.get()} {os.path.basename(path)} {len(data)}")
    client.sendall(data)
    show(reply())
    list_files()


def exit_app():
    send("EXIT")
    client.close()
    root.destroy()


# ---------- window ----------
root = tk.Tk()
root.title("File Access - CS24I1029")

top = tk.Frame(root)
top.pack(pady=4)
tk.Label(top, text="Username").pack(side="left")
user_entry = tk.Entry(top, width=12)
user_entry.pack(side="left")
tk.Label(top, text="Password").pack(side="left")
pass_entry = tk.Entry(top, width=12, show="*")
pass_entry.pack(side="left")
tk.Button(top, text="Login", command=login).pack(side="left")

role_label = tk.Label(root, text="Not logged in")
role_label.pack()

file_list = tk.Listbox(root, height=8, width=50)
file_list.pack(padx=8)

buttons = tk.Frame(root)
buttons.pack(pady=4)
tk.Button(buttons, text="LIST", command=list_files).pack(side="left", padx=2)
tk.Button(buttons, text="READ / DOWNLOAD", command=read_file).pack(side="left", padx=2)
tk.Label(buttons, text="  Category:").pack(side="left")
category_box = ttk.Combobox(buttons, values=["academic", "administrative"],
                            width=14, state="readonly")
category_box.set("academic")
category_box.pack(side="left")
tk.Button(buttons, text="UPLOAD", command=lambda: send_file("UPLOAD")).pack(side="left", padx=2)
tk.Button(buttons, text="UPDATE", command=lambda: send_file("UPDATE")).pack(side="left", padx=2)

output = tk.Text(root, height=12, width=70)
output.pack(padx=8, pady=4)
tk.Button(root, text="EXIT", command=exit_app).pack(pady=4)

root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()
