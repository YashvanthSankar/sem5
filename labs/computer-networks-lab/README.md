# Computer Networks lab exam preparation

Start with [00_basics/LESSON.md](00_basics/LESSON.md). Its two short programs
match the server/client pattern you wrote in chat. For a one-page map of Labs
5–9, use [SOCKET_EXAM_5_TO_9.md](SOCKET_EXAM_5_TO_9.md). Then read `lab2/server.py`
and `lab2/client.py`; Lab 2 changes the server reply to lowercase.

Labs 6–9 also have a `cli/` practice folder with terminal-only server and
client programs. Use those to learn the socket steps; the parent-folder GUI
programs cover the assessed GUI requirements.

The exam programs now live **directly in `lab2`–`lab9`**. Each folder has a
readable `QUESTIONS.md`. Labs 2–9 have one
`server.py`, one `client.py`, and a `README.md` covering its socket question,
Packet Tracer question, and viva points. Labs 5–9 use Tkinter clients because
their questions require a GUI. Labs 5, 7, 8, and 9 have server GUI logs as
required; Lab 6 asks for a server terminal. Your submitted work remains in
the sibling `../lab/` folder and each lab's `submitted/` folder.

| Lab | Q1 | Q2: Packet Tracer |
|---|---|---|
| [Lab 1](lab1/QUESTIONS.md) | Linux network commands | straight/crossover cable |
| [Lab 2](lab2/QUESTIONS.md) | lowercase server | hub, switch, router, repeater, bridge |
| [Lab 3](lab3/QUESTIONS.md) | threaded shared word string | bus, star, ring, mesh, tree, hybrid |
| [Lab 4](lab4/QUESTIONS.md) | threaded file upload and log | VLANs and trunk |
| [Lab 5](lab5/QUESTIONS.md) | GUI chat, private/broadcast, server log | WLAN |
| [Lab 6](lab6/QUESTIONS.md) | GUI video relay, packet measurements | DNS and web server |
| [Lab 7](lab7/QUESTIONS.md) | GUI Rock–Paper–Scissors and FIFO pairing | DHCP and relay |
| [Lab 8](lab8/QUESTIONS.md) | GUI quiz, scored by server | GRE tunnel and tracert |
| [Lab 9](lab9/QUESTIONS.md) | GUI role-based file access | FTP and email |

## How to practise writing

1. Write the two basics files from memory. Run them. Then write Lab 2 from
   memory, changing only the message processing and address prints.
2. Lab 3 adds `threading.Thread` and `with lock:`. Practise with three clients.
3. Lab 4 adds a filename, `READY`/rejection, byte count, delayed chunks, and
   a log. Upload txt, docx, pdf, and mp4 and check each saved file.
4. Labs 5–7 add a listener thread for messages that may arrive at any time.
   In a GUI, that thread puts messages in a queue; `root.after()` updates the
   window. Learn this pattern once, then see how each question uses it.
5. Labs 8–9 send a request and wait for a reply. Focus on the server's quiz
   score and role permission check; those are the ideas examiners will probe.
6. Rebuild each Packet Tracer topology without looking at the saved `.pkz`.
   Show ping and Simulation mode, then explain why the result occurs.

The only special correction to the earlier Packet Tracer notes is Lab 8:
the question asks for **five intermediate routers**, so use five in the
middle plus the two edge routers. GRE hides the intermediate hops from the
inner traceroute but does not encrypt traffic by itself.

## Running the programs

Run `server.py` first, then `client.py`. The programs use `127.0.0.1` for
one-computer practice and port `18080` because this Mac already uses port
`5000`. In the exam, set the server `HOST` to your actual LAN IPv4 and the
client `HOST` to the server computer's IPv4. Several questions explicitly
forbid loopback, `localhost`, and `0.0.0.0` for the network demonstration.
Use the same port in both files. On this Mac, `/usr/bin/python3` is a reliable
choice for Tkinter if the Homebrew Python GUI behaves differently.

Run `python3 verify.py` from this folder to check the server protocols on
one computer. Lab 6 has `experiments.csv` and `make_graphs.py`; the graphs
must use measurements from your own video transfers. Friend-to-friend tests,
GUI button demos, Packet Tracer simulation, and screenshots still require
hands-on practice.
