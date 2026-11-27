import socket
import threading
from datetime import datetime

SERVER_IP = "172.16.14.28"
PORT = 5000

# socket : username
users = {}

users_lock = threading.Lock()
log_lock = threading.Lock()


def log(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with log_lock:
        with open("log.txt", "a") as file:
            file.write(f"[{time}] : {message}\n")

def show_users():
    with users_lock:
        print("\n" + "=" * 55)
        print(f"ACTIVE CLIENTS : {len(users)}")
        print("=" * 55)

        if not users:
            print("No active users.")
        else:
            for sock, name in users.items():
                try:
                    address = sock.getpeername()
                    print(f"{address}  ->  {name}")
                except:
                    print(f"Disconnected -> {name}")

        print("=" * 55)

def send_message(sock, message):
    try:
        sock.sendall(message.encode())
        return True
    except:
        return False

def handle_client(conn, address):

    username = None
    join_time = None

    ip = address[0]
    port = address[1]
    client_address = f"{ip}:{port}"

    try:
        while True:

            send_message(conn, "USERNAME")

            name = conn.recv(1024).decode().strip()

            if not name:
                continue

            with users_lock:
                username_available = name not in users.values()

                if username_available:
                    users[conn] = name

            if username_available:
                username = name
                join_time = datetime.now()

                send_message(
                    conn,
                    f"SUCCESS|Welcome {username}"
                )

                log(
                    f"{client_address}, Username: {username}, "
                    f"Activity: joined"
                )

                print(
                    f"\n[+] {username} connected from "
                    f"{client_address}"
                )

                show_users()
                break

            else:
                send_message(
                    conn,
                    "RETRY|Username already in use"
                )

                log(
                    f"{client_address}, "
                    f"AttemptedUsername: {name}, "
                    f"Status: Rejected "
                    f"(Username already in use)"
                )

        while True:

            data = conn.recv(4096).decode()

            if not data:
                break

            data = data.strip()

            if data == "/users":

                with users_lock:
                    active_users = list(users.values())

                if active_users:
                    message = (
                        "[SERVER] Active Users: "
                        + ", ".join(active_users)
                    )
                else:
                    message = "[SERVER] No active users."

                send_message(conn, message)

            elif data == "/exit":
                break

            elif data.startswith("<broadcast>:"):

                message = data.split(":", 1)[1].strip()

                if not message:
                    send_message(
                        conn,
                        "[SERVER] Empty message."
                    )
                    continue

                with users_lock:
                    recipients = [
                        (sock, name)
                        for sock, name in users.items()
                        if sock != conn
                    ]

                for target_sock, target_name in recipients:

                    try:
                        target_address = target_sock.getpeername()
                        target_addr = (
                            f"{target_address[0]}:"
                            f"{target_address[1]}"
                        )

                        target_sock.sendall(
                            f"{username}: {message}".encode()
                        )

                        log(
                            f"From: {username}({client_address}), "
                            f"To: {target_name}({target_addr}), "
                            f"Size: {len(message.encode())}Bytes, "
                            f"Status: Sent"
                        )

                    except Exception as e:

                        log(
                            f"From: {username}({client_address}), "
                            f"To: {target_name}, "
                            f"Size: {len(message.encode())}Bytes, "
                            f"Status: Failed ({e})"
                        )

            elif ":" in data:

                target_name, message = data.split(":", 1)

                target_name = target_name.strip()
                message = message.strip()

                target_name = target_name.strip("<>")

                if not target_name or not message:
                    send_message(
                        conn,
                        "[SERVER] Invalid message format."
                    )
                    continue

                with users_lock:
                    target_sock = None

                    for sock, name in users.items():
                        if name == target_name:
                            target_sock = sock
                            break

                if target_sock:

                    try:

                        target_address = target_sock.getpeername()

                        target_addr = (
                            f"{target_address[0]}:"
                            f"{target_address[1]}"
                        )

                        target_sock.sendall(
                            f"{username}: {message}".encode()
                        )

                        log(
                            f"From: {username}({client_address}), "
                            f"To: {target_name}({target_addr}), "
                            f"Size: {len(message.encode())}Bytes, "
                            f"Status: Sent"
                        )

                    except Exception as e:

                        send_message(
                            conn,
                            "[SERVER] User Not Online"
                        )

                        log(
                            f"From: {username}({client_address}), "
                            f"To: {target_name}, "
                            f"Size: {len(message.encode())}Bytes, "
                            f"Status: Failed ({e})"
                        )

                else:

                    send_message(
                        conn,
                        "[SERVER] User Not Online"
                    )

                    log(
                        f"From: {username}({client_address}), "
                        f"To: {target_name}, "
                        f"Size: {len(message.encode())}Bytes, "
                        f"Status: Failed (User Not Online)"
                    )

            else:

                send_message(
                    conn,
                    "[SERVER] Invalid command."
                )

    except Exception as e:

        print(
            f"[!] Connection error "
            f"{client_address}: {e}"
        )

    finally:

        if username:

            with users_lock:
                users.pop(conn, None)

            session_time = datetime.now() - join_time
            total_seconds = int(
                session_time.total_seconds()
            )

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            duration = (
                f"{hours:02}:{minutes:02}:{seconds:02}"
            )

            log(
                f"{client_address}, Username: {username}, "
                f"Activity: left, "
                f"session_duration: [{duration}]"
            )

            print(
                f"\n[-] {username} disconnected "
                f"from {client_address}"
            )

            show_users()

        try:
            conn.close()
        except:
            pass

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((SERVER_IP, PORT))
server.listen(10)

print("\n" + "=" * 60)
print("             MULTI CLIENT CHAT SERVER")
print("=" * 60)
print(f"Server IPv4 Address : {SERVER_IP}")
print(f"Server Port         : {PORT}")
print(f"Server Socket       : {server.getsockname()}")
print("=" * 60)
print("Waiting for clients...\n")

while True:

    try:
        conn, address = server.accept()

        print(
            f"[NEW CONNECTION] {address}"
        )

        thread = threading.Thread(
            target=handle_client,
            args=(conn, address),
            daemon=True
        )

        thread.start()

    except KeyboardInterrupt:

        print("\nServer stopped.")
        break

    except Exception as e:

        print(f"Server error: {e}")


server.close()
