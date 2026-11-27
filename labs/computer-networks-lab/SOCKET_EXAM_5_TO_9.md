# Socket exam: Labs 5–9

Read each `QUESTIONS.md` first, then `server.py`, then `client.py`. The server
contains the real rules. The client mostly draws the window and sends commands.

| Lab | What to remember | One important server job |
|---|---|---|
| 5 | Chat | Find the recipient socket and forward a message. |
| 6 | Video | Read and forward file bytes in chunks. |
| 7 | Rock–Paper–Scissors | Pair players FIFO; decide winner after two choices. |
| 8 | Quiz | Keep answers secret and calculate the score. |
| 9 | File access | Check the role **on the server** before every file operation. |

## The small pattern repeated in every lab

```python
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
```

`accept()` waits for a client. `handle()` serves that one client. A thread
allows other clients to connect while the first is still using the server.

```python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
reader = client.makefile("r")
client.sendall((message + "\n").encode())
reply = reader.readline().strip()
```

`\n` marks the end of one text command. `readline()` reads through that marker.
For Lab 6 and 9, the reader uses `"rb"` because file bytes follow the text
header. `reader.read(size)` then reads exactly that many file bytes.

## Why some clients use a listener thread

In Labs 5, 6 and 7, a message may arrive at any time. A listener thread reads
the socket and puts messages into a `queue.Queue`. The Tkinter main thread
checks the queue with `root.after(100, refresh)` and updates the window.
Labs 8 and 9 simply send a request and read its reply, so their clients do
not need listener threads.

## Learn these five ideas, not every GUI line

1. **Lab 5:** `clients = {socket: username}`. `/users` lists names; `name:msg`
   sends to one socket; `broadcast:msg` sends to all other sockets. `/exit`
   removes the client. The log records names, addresses, times, sizes and
   outcomes.
2. **Lab 6:** `total = (file_size + packet_size - 1) // packet_size`.
   The sender sends a header and then `total` chunks. The receiver uses the
   known file size and packet size to read them. TCP normally gives zero
   application-level packet loss; delay mainly changes transfer time.
3. **Lab 7:** `waiting.append(player)` and `waiting.pop(0)` make FIFO pairs.
   Once both players choose, the server checks who wins. If one leaves during
   a game, the other wins. `REPLAY` adds the player to the waiting list again.
4. **Lab 8:** Server sends questions without answers. Client sends saved
   letters such as `ANSWERS B,C,-,A`. Server checks and replies with `SCORE`.
5. **Lab 9:** Login chooses a role. A set of `(category, operation)` pairs
   holds that role's permissions. Before `READ`, `UPLOAD` or `UPDATE`, the
   server checks membership in that set. `READ` sends bytes to the client;
   `UPLOAD` and `UPDATE` send bytes to the server.

## What the code alone cannot finish

- Lab 5 explicitly requires a **real network IPv4** in `HOST` for assessed
  runs. Replace `127.0.0.1` in both programs with the server machine's
  current IPv4, and capture separate local and friend-network logs.
- Labs 5, 7 and 8 require testing with friends. Their programs must use the
  same text-command format on both machines; another student's unrelated
  program is not automatically compatible.
- Lab 6 needs **real** transfer measurements for 4–5 packet sizes and 4–5
  delays. Fill `lab6/experiments.csv`, then run `lab6/make_graphs.py`.
- Lab 7 now uses Rock–Paper–Scissors. The older submitted screenshot PDF
  shows the previous game, so take fresh screenshots of the new code.
- All five labs require the screenshots/PDFs named in their questions. These
  must show your actual exam run; the Python files cannot create that evidence.
