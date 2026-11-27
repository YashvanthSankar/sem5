# Start here: your short socket program

Read `echo_server.py` and `echo_client.py` first. They use the same simple
pattern you wrote in chat: **one client, one short message, one reply**.

Run the server in one terminal and the client in another:

```text
python3 echo_server.py
python3 echo_client.py
```

The server ends after that client. Start it again for another try. Once you
can write both files without looking, change only one line in the server:
`("echo: " + message)` → `message.lower()`. That is Lab 2.

## The seven calls

| Server | Client | Meaning |
|---|---|---|
| `socket.socket(AF_INET, SOCK_STREAM)` | same | create an IPv4 TCP socket |
| `bind((HOST, PORT))` | — | choose the server's address |
| `listen(1)` | — | wait for connections |
| `accept()` | `connect((HOST, PORT))` | establish the connection |
| `recv(1024)` | `sendall(...)` | receive/send bytes |
| `sendall(...)` | `recv(1024)` | send/receive the reply |
| `close()` | `close()` | finish |

`encode()` changes a Python string to bytes; `decode()` changes bytes back to
a string. `accept()` returns a **new connected socket** (`conn`) and the
client's address. `server` remains the listening socket.

## Three additions you need later

**Repeated messages (Lab 3 onward):** TCP is a stream, so one `recv(1024)`
does not always equal one message. End each text message with `"\n"` and read
one line at a time:

```python
conn.sendall((text + "\n").encode())
reader = conn.makefile("r")
line = reader.readline().strip()
```

**Several clients (Labs 3–9):** leave `accept()` in a loop. Start one thread
for each new `conn` so the server can accept the next client. Use a lock for
shared lists, usernames, counters, or game state.

```python
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
```

**Files (Labs 4, 6, 9):** send the byte count before the bytes. A receiver
cannot find the end of a file from `recv()` alone. With
`reader = conn.makefile("rb")`, read the length line and then the exact bytes:

```python
size = int(reader.readline())
data = reader.read(size)
```

Once you make a reader, do all reads through that reader. Do not mix its
`readline()` with `conn.recv()` on the same socket.

## What changes for the real exam

`127.0.0.1` is only for practising on one computer. Several lab questions
require your actual LAN IPv4 and a friend's server IPv4. Replace `HOST` in
the server with your IPv4 and in the client with the server's IPv4. Keep the
same port on both sides. These files use port `18080` because port `5000` is
occupied on this Mac.

Then study Lab 2, Lab 3, and Lab 4 in that order. The root `README.md` gives
the path for the remaining labs and Packet Tracer work.
