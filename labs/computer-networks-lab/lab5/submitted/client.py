import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

SERVER_IP = "172.16.14.28"
PORT = 5000

class ChatClient:

    def __init__(self, root):

        self.root = root
        self.username = ""
        self.connected = False

        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:
            self.sock.connect(
                (SERVER_IP, PORT)
            )

        except Exception as e:

            messagebox.showerror(
                "Connection Error",
                f"Cannot connect to server.\n\n{e}"
            )

            root.destroy()
            return

        self.client_address = self.sock.getsockname()
        self.server_address = self.sock.getpeername()

        print("=" * 60)
        print("CLIENT CONNECTED")
        print("=" * 60)
        print("Client Socket :", self.client_address)
        print("Server Socket :", self.server_address)
        print("=" * 60)

        self.create_gui()
        self.login()

        threading.Thread(
            target=self.receive_messages,
            daemon=True
        ).start()

    def create_gui(self):

        self.root.title("LAN Chat")
        self.root.geometry("720x560")
        self.root.minsize(650, 500)

        self.root.configure(
            bg="#171a21"
        )
        
        header = tk.Frame(
            self.root,
            bg="#20242c"
        )

        header.pack(
            fill="x"
        )

        self.title_label = tk.Label(
            header,
            text="LAN CHAT",
            font=("Arial", 20, "bold"),
            bg="#20242c",
            fg="white"
        )

        self.title_label.pack(
            pady=(12, 2)
        )

        self.user_label = tk.Label(
            header,
            text="Not logged in",
            font=("Arial", 10),
            bg="#20242c",
            fg="#61dafb"
        )

        self.user_label.pack(
            pady=(0, 10)
        )

        chat_frame = tk.Frame(
            self.root,
            bg="#171a21"
        )

        chat_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.chat = scrolledtext.ScrolledText(
            chat_frame,
            font=("Arial", 11),
            bg="#252a33",
            fg="white",
            insertbackground="white",
            wrap=tk.WORD,
            relief="flat"
        )

        self.chat.pack(
            fill="both",
            expand=True
        )
        self.info_label = tk.Label(
            self.root,
            text=(
                f"Client: {self.client_address[0]}:"
                f"{self.client_address[1]}   |   "
                f"Server: {SERVER_IP}:{PORT}"
            ),
            font=("Arial", 9),
            bg="#171a21",
            fg="#8f98a8"
        )

        self.info_label.pack(
            pady=2
        )

        input_frame = tk.Frame(
            self.root,
            bg="#171a21"
        )

        input_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Label(
            input_frame,
            text="To:",
            font=("Arial", 11, "bold"),
            bg="#171a21",
            fg="white"
        ).pack(
            side="left"
        )

        self.to_entry = tk.Entry(
            input_frame,
            width=13,
            font=("Arial", 11),
            bg="#252a33",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.to_entry.pack(
            side="left",
            padx=7,
            ipady=6
        )

        self.to_entry.insert(
            0,
            "user2"
        )

        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg="#252a33",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            ipady=6
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_private()
        )

        tk.Button(
            input_frame,
            text="SEND",
            command=self.send_private,
            bg="#00a86b",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            width=9
        ).pack(
            side="right",
            padx=5,
            ipady=4
        )

        button_frame = tk.Frame(
            self.root,
            bg="#171a21"
        )

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="👥 USERS",
            command=self.show_users,
            bg="#1976d2",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            width=13
        ).pack(
            side="left",
            padx=6,
            ipady=5
        )

        tk.Button(
            button_frame,
            text="📢 BROADCAST",
            command=self.broadcast,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            width=13
        ).pack(
            side="left",
            padx=6,
            ipady=5
        )

        tk.Button(
            button_frame,
            text="❌ EXIT",
            command=self.exit_chat,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            width=13
        ).pack(
            side="left",
            padx=6,
            ipady=5
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit_chat
        )

        self.add_message(
            "[SYSTEM] Connected to server."
        )

        self.add_message(
            f"[SYSTEM] Server: {SERVER_IP}:{PORT}"
        )

    def login(self):

        name = simpledialog.askstring(
            "Login",
            "Enter your username:",
            parent=self.root
        )

        if not name:

            self.sock.close()
            self.root.destroy()
            return

        self.username = name.strip()

        try:

            # Send username directly
            self.sock.sendall(
                self.username.encode()
            )

            self.connected = True

            self.user_label.config(
                text=f"Logged in as: {self.username}"
            )

            self.title_label.config(
                text=f"💬 LAN CHAT  |  {self.username}"
            )

            self.add_message(
                f"[SYSTEM] Username: {self.username}"
            )

        except Exception as e:

            messagebox.showerror(
                "Login Error",
                str(e)
            )

            self.root.destroy()

    def receive_messages(self):

        while self.connected:

            try:

                data = self.sock.recv(
                    4096
                ).decode()

                if not data:
                    break

                # Ignore login prompt if friend's server
                # sends one
                if data == "USERNAME":
                    continue

                if data.startswith("SUCCESS|"):
                    data = data.split(
                        "|", 1
                    )[1]

                self.root.after(
                    0,
                    self.add_message,
                    data
                )

            except:
                break

    def add_message(self, message):

        self.chat.insert(
            tk.END,
            message + "\n"
        )

        self.chat.see(
            tk.END
        )

    def send_private(self):

        target = self.to_entry.get().strip()
        message = self.message_entry.get().strip()

        if not target:

            messagebox.showwarning(
                "Username Required",
                "Enter the receiver username."
            )

            return

        if not message:
            return

        try:

            self.sock.sendall(
                f"<{target}>:{message}".encode()
            )

            self.add_message(
                f"You → {target}: {message}"
            )

            self.message_entry.delete(
                0,
                tk.END
            )

        except Exception as e:

            self.add_message(
                f"[ERROR] {e}"
            )

    def broadcast(self):

        message = self.message_entry.get().strip()

        if not message:
            return

        try:

            self.sock.sendall(
                f"<broadcast>:{message}".encode()
            )

            self.add_message(
                f"You → ALL: {message}"
            )

            self.message_entry.delete(
                0,
                tk.END
            )

        except Exception as e:

            self.add_message(
                f"[ERROR] {e}"
            )

    def show_users(self):

        try:

            self.sock.sendall(
                b"/users"
            )

        except Exception as e:

            self.add_message(
                f"[ERROR] {e}"
            )

    def exit_chat(self):

        self.connected = False

        try:

            self.sock.sendall(
                b"/exit"
            )

        except:
            pass

        try:
            self.sock.close()
        except:
            pass

        self.root.destroy()

root = tk.Tk()

app = ChatClient(root)

root.mainloop()
