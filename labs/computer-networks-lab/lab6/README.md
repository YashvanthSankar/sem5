# Lab 6: Video relay through the server + DNS

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): send .mp4 from client to client via the server

For a shorter terminal-only learning version, see [cli/README.md](cli/README.md).

Use `client.py` (Tkinter): enter a username, choose a receiver and `.mp4` file, select packet size and delay, then click Send Video.

The protocol, which is the important part:
```
sender → server : VIDEO alice bob 8192 62 500000 0.001 clip.mp4  (from, to, packet size, total, size, delay, name)
sender → server : <8192 bytes><8192 bytes> ... <last 288 bytes>
server → bob    : VIDEO alice 8192 62 500000 clip.mp4    (same metadata, but with the SENDER's name)
                  + the same file bytes, forwarded one packet at a time
server → sender : INFO Server got 62/62 packets (loss 0)  or  ERROR User Not Online
```
- `total packets = ceil(file size / packet size)` (`math.ceil`).
- The receiver knows how many bytes to read from the file size and packet size in the header.
- Receiver saves `received_from_alice_clip.mp4` and prints original size, received size, packets, loss, time.
- **Send and receive at the same time** = listener thread receives videos while a sending thread sends packets.
- Server uses a **lock per receiver socket** for the whole video, so two videos to the same person never mix.
- If the receiver is offline, the server still reads (and drops) the bytes, then replies "User Not Online".

**About packet loss (viva favourite):** we use **TCP**, which guarantees delivery and order, so
loss is always **0** and received size = original size, whatever the packet size/delay.
What changes is **time**: bigger packets → fewer packets → faster; bigger `sleep` → slower.
With **UDP** (`SOCK_DGRAM`, `sendto`), large packets + no delay **would** overflow buffers and lose packets.
That's the trade-off TCP vs UDP.

**GUI:** `client.py` has every widget the question lists: username + Connect, users dropdown + Refresh,
Browse Video, file label, packet size + delay dropdowns, Send, sending/receiving progress bars, status box, Disconnect.
Sending runs in its own thread so the window stays responsive.
Use `experiments.csv` and `make_graphs.py` for the five required graphs; no extra Python package is needed.

## Q2 (Packet Tracer): DNS + Web server

**A. One LAN:** switch + 3 PCs + **DNS server** + **Web server**, all 192.168.1.x /24.
1. Web server: static IP 192.168.1.10. Services → **HTTP**: ON, edit `index.html` (your name/roll).
2. DNS server: static IP 192.168.1.20, display name `dns.iiitdm.ac.in`. Services → **DNS**: ON →
   Name `www.iiitdm.ac.in`, Type **A Record**, Address `192.168.1.10` → Add.
3. Every PC: IP Configuration → static IP + **DNS Server = 192.168.1.20**.
4. PC → Desktop → **Web Browser** → `www.iiitdm.ac.in` → page loads. Also `ping www.iiitdm.ac.in`.

**B. Two LANs (L512, L509) + router:**
- L512: 192.168.12.0/24 (5 PCs + DNS server + web server), L509: 192.168.9.0/24 (5 PCs).
- Router g0/0 = 192.168.12.1, g0/1 = 192.168.9.1 (`ip address`, `no shutdown`, see lab 2). PCs' gateway = router IP on their side.
- DNS: A records `moodle.com`, `google.com`, `iiitdm.ac.in` → web server IP. All PCs' DNS = DNS server IP.
- Simulation mode, filter **DNS** + HTTP: from an L509 PC open `google.com`, and watch the **DNS query** go to the
  server and the **DNS response** come back with the IP, *then* HTTP starts.

**Viva:** DNS = name → IP, runs on **UDP port 53**; A record = name→IPv4; HTTP port 80; the
browser asks DNS first, then connects to the IP.

## Recording the required experiments

Run the same video nine times: five packet sizes (1024, 4096, 8192, 16384, 65536) at delay 0.001 seconds, and five delays (0, 0.001, 0.005, 0.01, 0.05) at packet size 4096. The 4096/0.001 run is shared. The server writes `video_log.csv`; record the sender and receiver counts in `experiments.csv`, then run `python3 make_graphs.py` to create the five graphs. Use real measurements; TCP transfers normally show zero application-level loss.
