import socket
import threading

global_string = ""
lock = threading.Lock()
active_connections = 0


def handle_client(client_connection, client_address):
    global global_string
    global active_connections

    with lock:
        active_connections += 1
        print(f"Client joined: {client_address}")
        print(f"Active connections: {active_connections}")

    try:
        while True:
            data = client_connection.recv(1024)

            if not data:
                break

            word = data.decode().strip()

            if word.lower() == "exit":
                break

            with lock:
                words = global_string.split(",")

                if global_string == "":
                    global_string = word
                elif word not in words:
                    global_string += "," + word

                client_connection.send(global_string.encode())

    except ConnectionResetError:
        print(f"Client disconnected: {client_address}")

    finally:
        client_connection.close()
        with lock:
            active_connections -= 1
            print(f"Client left: {client_address}")
            print(f"Active connections: {active_connections}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("172.16.14.28", 8080))
server_socket.listen(5)

print("Server running on 172.16.14.28:8080")
print("Waiting for clients...")

while True:
    client_connection, client_address = server_socket.accept()
    thread = threading.Thread(
        target=handle_client,
        args=(client_connection, client_address),
        daemon=True
    )

    thread.start()

