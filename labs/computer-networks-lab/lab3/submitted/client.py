import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = input("Enter host:").strip()
PORT = int(input("Enter port:"))


client_socket.connect((HOST, PORT))

print("Connected to server.")
print("Enter a single word.")
print("Enter 'exit' to disconnect.")

try:
    while True:
        word = input("Enter word: ").strip()

        if not word:
            print("Please enter a word.")
            continue

        client_socket.send(word.encode())
        if word.lower() == "exit":
            break

        response = client_socket.recv(1024).decode()

        print("Server:", response)

finally:
    client_socket.close()
    print("Connection closed.")

