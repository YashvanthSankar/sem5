# Name: YASHVANTH S | Roll: CS24I1029
# CLI practice: server decides which files this role may access.
import os
import socket

HOST, PORT = "127.0.0.1", 18080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("rb")  # text commands plus raw file bytes


def send(text):
    client.sendall((text + "\n").encode())


def reply():
    return reader.readline().decode().strip()


while True:
    user = input("Username: ").strip()
    password = input("Password: ").strip()
    send(f"LOGIN {user} {password}")
    result = reply()
    print(result)
    if result.startswith("OK "):
        break

print("1 LIST, 2 READ/DOWNLOAD, 3 UPLOAD, 4 UPDATE, 5 EXIT")
while True:
    choice = input("> ").strip()
    if choice == "1":
        send("LIST")
        print(reply())
    elif choice == "2":
        category = input("Category (academic/administrative): ").strip().lower()
        filename = os.path.basename(input("Filename: ").strip())
        send(f"READ {category} {filename}")
        result = reply()
        if result.startswith("OK "):
            data = reader.read(int(result.split()[1]))
            with open("downloaded_" + filename, "wb") as file:
                file.write(data)
            print(f"Saved downloaded_{filename}: {len(data)} bytes")
            print(data.decode(errors="replace"))
        else:
            print(result)
    elif choice in ("3", "4"):
        operation = "UPLOAD" if choice == "3" else "UPDATE"
        category = input("Category (academic/administrative): ").strip().lower()
        path = input("Local file path: ").strip()
        try:
            with open(path, "rb") as file:
                data = file.read()
        except OSError as error:
            print(error)
            continue
        send(f"{operation} {category} {os.path.basename(path)} {len(data)}")
        client.sendall(data)
        print(reply())
    elif choice == "5":
        send("EXIT")
        break
    else:
        print("Choose 1 to 5")
client.close()
