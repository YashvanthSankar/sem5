# Computer Networks lab exam — full study context

This is a self-contained recap of our preparation conversation. It is a study note, not a replacement for the exact question sheets in each `labN/QUESTIONS.md`. The original submissions are in each `submitted/` folder and the sibling `../lab/` folder. The readable preparation programs are directly under `lab2/`–`lab9/`. Labs 6–9 also have shorter terminal practice programs under `cli/`.

## How you want to study

- Learn the logic first, then short code you can explain and write in an exam. Avoid unnecessary Tkinter or logging detail while learning the core.
- For each socket question, identify **who connects, what message is sent, what the server checks, what reply is sent, and when the connection closes**.
- For Packet Tracer, build and verify the physical path first, then addresses, routing, services, and screenshots.
- For a paper answer, draw the architecture and give message format, algorithm, code, tests, and conclusion. Use the exact question wording to decide what details earn marks.

## All nine labs at a glance

| Lab | Socket / other Q1 | Packet Tracer Q2 |
| --- | --- | --- |
| 1 | Linux networking commands; no socket program | Straight-through/crossover cables, same/different IP networks |
| 2 | TCP server returns lowercase text | Hub, switch, router, repeater, bridge |
| 3 | Thread per client; shared comma-separated word list | Bus, star, ring, mesh, tree, hybrid |
| 4 | Threaded upload, unique/reused username, file log | VLAN access ports and trunks |
| 5 | Tkinter multi-client chat, private/broadcast, logs | WLAN and combined wired/wireless LAN |
| 6 | Tkinter video relay through server, chunk size/delay, measurements | DNS and web server in one/two LANs |
| 7 | Tkinter two-player Rock–Paper–Scissors, FIFO pairing, chat/replay | DHCP, two pools, DHCP relay |
| 8 | Tkinter quiz; server owns answer key and scores | RIP/routing, GRE tunnel, before/after `tracert` |
| 9 | Tkinter role-based file access | FTP and email |

Read each `QUESTIONS.md` for required screenshots, local-versus-friend demonstrations, precise strings, and submission details. Some Q2 prompts were reconstructed from submitted PDFs; those files say so explicitly.

## Socket fundamentals

### TCP versus UDP

- `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` creates an IPv4 **TCP** socket. All the basic lab socket programs we studied use TCP.
- `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)` creates an IPv4 **UDP** socket.
- TCP server: `bind → listen → accept → recv/send`. TCP client: `connect → send/recv`.
- UDP server: `bind → recvfrom/sendto`. UDP client: `sendto/recvfrom`. UDP has no `listen`, `accept`, or per-client connection.
- TCP gives an ordered, reliable **byte stream**. UDP sends individual datagrams without built-in delivery guarantees. UDP is not automatically faster in every situation and does not automatically create congestion; compare performance under a defined workload.

### Tiny TCP template to memorize

`server.py`:

```python
import socket
import threading

def handle(conn, addr):
    with conn:
        reader = conn.makefile("r")
        for line in reader:
            message = line.strip()
            if message == "exit":
                break
            reply = message.upper()  # Replace with the question's logic.
            conn.sendall((reply + "\n").encode())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
```

`client.py`:

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))
reader = client.makefile("r")
while True:
    message = input("You: ")
    client.sendall((message + "\n").encode())
    if message == "exit":
        break
    print("Server:", reader.readline().strip())
client.close()
```

The `"\n"` is essential because `readline()` waits for a newline. `127.0.0.1` is only for one-computer practice; assessed friend-to-friend lab runs often require actual LAN IPs.

### Functions and values you asked about

| Expression | Meaning |
| --- | --- |
| `b"hello"` | Literal bytes, suitable for `sendall`; variable text uses `.encode()` |
| `data.decode()` | Convert received bytes into text |
| `sendall(data)` | Keep sending until all bytes have been handed to TCP or an error occurs |
| `send(data)` | May send only part; return value is number of bytes sent |
| `recv(1024)` | Receive **up to** 1024 bytes; one call is not guaranteed to equal one message |
| `conn.makefile("r")` | Text reader over a socket; `readline()` reads through `\n` |
| `conn.makefile("rb")` | Binary reader; `readline()` returns bytes, so decode if needed |
| `reader.read(size)` | Read a known number of bytes, useful for files |
| `socket.create_connection((host, port))` | TCP client shortcut for `socket()` plus `connect()` |
| `conn, addr = server.accept()` | `conn` is the new socket for that client; `addr` is `(client_ip, client_port)` |
| `conn.getsockname()` | This connection's local/server-side IP and port |
| `daemon=True` | Worker thread will not keep Python running after main thread exits |
| `threading.Lock()` | Protect shared dictionaries/counters from simultaneous threads |
| `threading.RLock()` | Lock the same thread may acquire again; used for nested sending in Lab 6 |
| `clients.pop(conn, None)` | Remove connection key if present; `None` avoids an error if absent |
| `server.close()` | Close listening socket when the entire server shuts down |
| `conn.close()` | Close one accepted client connection |
| `try/except Exception/finally` | Handle an error; `finally` runs cleanup on success or failure |

`socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` is a useful restart option, not the core of the algorithm. Never confuse `client` (outgoing socket in client code) and `conn` (accepted socket in server code); both represent one end of the same connection.

### Text and files

- `line.split(":", 1)` splits only at the first colon; good for `username:message` when the message may contain other colons.
- `"/".join(parts)` inserts `/` between strings. It is called on the separator string.
- `.strip()` removes surrounding whitespace/newline; `.strip("<>")` removes leading/trailing angle brackets only.
- `os.path.basename(path)` keeps only the filename. `os.path.join(folder, filename)` builds a path. `os.makedirs(folder, exist_ok=True)` creates the folder if missing.
- For file transfer, send a **header containing filename and size**, then send exactly `size` bytes in chunks. The receiver reads exactly that size. For `packet_count = ceil(file_size / packet_size)`, integer-only form is `(file_size + packet_size - 1) // packet_size`.
- `time.sleep(delay)` pauses for `delay` seconds; e.g. `0.1` means 100 ms.

### Threads, queues, and Tkinter

- A threaded server calls `threading.Thread(target=handle, args=(conn, addr), daemon=True).start()` for each accepted client.
- A chat/game/video client often needs a **listener thread** because the server may send messages at any time.
- Tkinter widgets should be updated from the main GUI thread. Listener thread puts received messages into `queue.Queue`; GUI polls with `window.after(100, check_queue)`.
- `send_lock` prevents two threads from mixing bytes on one socket. `with lock:` protects shared state.
- Basic Tkinter: `window = tk.Tk()`, `Label`, `Entry`, `Button(command=function_name)`, `Text`, `.grid()`/`.pack()`, `.get()`, `.insert(tk.END, text)`, `.delete(0, tk.END)`, `window.mainloop()`.
- `tk.END` means the end of the widget content. The callback is written `command=send_message`, without `()`; clicking invokes it later.

## Socket logic by lab

- **Lab 2:** accept text, lowercase it, send it back. Print sent/received text and socket addresses for both friend-to-friend roles.
- **Lab 3:** accept multiple clients in threads, protect a shared word list/string with a lock, append only new words, reply with the complete current list, handle `exit`.
- **Lab 4:** server assigns/reuses username; client proposes filename; server says `READY` or `File already exists`; after `READY`, send size and chunks; save and log accepted/rejected transfer. The server must know exact byte count.
- **Lab 5:** login username (`OK`/`TAKEN`); maintain online clients; `/users`, private `username:message`, broadcast, `/exit`; server routes messages and logs them. Client listener receives asynchronous messages.
- **Lab 6:** login; sender sends metadata (sender, receiver, filename, byte size, packet size/count, delay), then file chunks; server relays to recipient; receiver reconstructs file. Record transfer time, size and measured packet counts. TCP itself normally prevents application-visible packet loss during a successful transfer; report real measurements rather than inventing loss.
- **Lab 7:** server queues players FIFO and pairs 1–2, 3–4; receives RPS moves and chat; decides winner, peer-leave outcome, replay/exit. Client listener updates GUI.
- **Lab 8:** server stores questions and correct answers; client submits answers; only server calculates score. Strict request/reply order needs no listener thread in the basic version.
- **Lab 9:** server authenticates user, determines Student/Faculty/Admin role, checks **every requested operation on the server**, performs allowed LIST/READ/UPLOAD/UPDATE, denies forbidden requests, and logs outcome. Student: read Academic; Faculty additionally upload/update Academic and read Administrative; Admin additionally upload/update Administrative. A GUI hiding a forbidden button is not sufficient authorization.

## Proxy-server exam questions from the two photos

### What a proxy is

`Client → Proxy → Destination server`. The client connects to the proxy. The proxy `bind/listen/accept`s that connection, then creates **another socket and connects** to the destination. It reads client request, optionally filters/changes it, forwards, reads destination reply, and returns that reply to the original client. The two socket connections are separate.

### Campus gateway, speed/reliability activity

- Ten clients need ten applications on remote Server A; all access must pass through an Intermediate Server on campus.
- One defensible design: client-to-gateway TCP; gateway-to-Server-A UDP for a speed-priority mode, TCP for a reliability-priority mode. State that these are chosen strategies, not properties required by the prompt.
- Show access-node, gateway, and Server A code/algorithms. Define a message format and framing. Use timeouts for UDP.
- The outbound bottleneck can become congested. UDP has no built-in congestion control; an offered overload can cause loss/timeouts. TCP can also experience queueing/delay. Add an aggregate rate limiter or bounded queue at the gateway and compare measurements under a deliberately limited link.
- In the paper: diagram, protocol rationale, algorithm, code, tests, measured/theoretical analysis, congestion mitigation. Do not claim localhost proves real Internet congestion.

### Content-filtering proxy activity

- Multithreaded proxy accepts client, connects to intended destination, and relays allowed complete messages.
- Maintain forbidden keyword list, `warnings[ip]`, `blocked` IP set, and lock for shared data.
- On forbidden message: **drop it**, warn original client, increment that client's count; at threshold (e.g. 3), block future connections. Allowed message is forwarded, and destination reply returned.
- Use newline-delimited messages or another framing method. TCP `recv()` boundaries do not equal message/packet boundaries.
- Question inconsistently mentions counting by IP, adding MAC to blocklist, and rejecting future IPs. Ordinary routed TCP accept exposes peer IP, not generally peer MAC; explicitly state an IP blocklist assumption. A truly transparent proxy needs network redirection; ordinary clients connecting to the proxy implement an explicit proxy.

## Packet Tracer foundations

- Device link green means physical link up, not full IP/service correctness.
- PC fields: IP identifies host, subnet mask decides local versus remote, default gateway is the router IP on that PC's LAN, DNS server resolves names.
- Same-subnet traffic uses ARP to learn destination MAC, then switches forward by MAC. Cross-subnet traffic goes first to the default gateway, then routers forward by destination IP.
- A switch forwards known unicast to the learned port but floods broadcast and initially unknown unicast. A hub repeats to all ports. A repeater regenerates signal/bits. A bridge filters by MAC. A router separates IP networks and broadcast domains.
- `/24 = 255.255.255.0`; `/8 = 255.0.0.0`; `/30 = 255.255.255.252`.
- In `3.1.252.248/30`: `.248` network, `.249`/`.250` usable, `.251` broadcast. Last block in `3.1.252.x` is `.252` network, `.253`/`.254` usable, `.255` broadcast. Two tunnel ends must use the same `/30` block.

## Packet Tracer by lab

- **Lab 1 cables:** traditional rule: PC↔switch straight-through, PC↔PC and switch↔switch crossover. A green link between PCs in different IP subnets does not replace a router. CAT6 contains four twisted pairs/eight conductors.
- **Lab 2 devices:** hub broadcasts/repeats to all ports; switch learns MACs; router routes by IP; bridge is an older two-segment MAC-learning device; repeater extends signal.
- **Lab 3 topologies:** demonstrate bus, star, ring, mesh, tree, hybrid, ping and Simulation mode. A switch ring may show an orange blocked STP link to prevent loops.
- **Lab 4 VLANs:** access port carries one VLAN to PC; trunk carries multiple VLANs between switches using 802.1Q. Make the VLAN and assign access ports on **both** switches. Same VLAN across trunk works; different VLANs require inter-VLAN routing if they should communicate.
- **Lab 5 WLAN:** configure SSID and WPA2 key on WRT300N; ensure PC/laptop has Wi-Fi adapter; join SSID, obtain IP, ping. For wired and wireless devices in **one network**, connect the wired switch to a router **LAN** port, not its Internet/WAN port.
- **Lab 6 DNS/HTTP:** static IP on DNS and web servers; DNS `A` records map `moodle.com`, etc. to web-server IP; every PC's DNS field points to DNS server. Test gateway → DNS IP → web IP → webpage by IP → webpage by name. DNS lookup occurs before HTTP.
- **Lab 7 DHCP:** DORA = Discover, Offer, Request, Acknowledge. Server has static IP and pools with start IP, mask, gateway, DNS. For a DHCP server on another LAN, use `ip helper-address <server-IP>` on the router interface facing the remote clients. Exact starts from question: one-LAN `192.168.1.12`, L512 `192.168.12.15`, L509 `192.168.9.115`.
- **Lab 8 RIP/GRE:** ordinary routing first; before-tunnel PC `tracert`; GRE between edge routers; static routes direct end-LAN traffic to opposite tunnel IP; ping/tracert after. Exact question requires **at least five intermediate routers**, i.e. seven total if using exactly five. GRE encapsulates but does not encrypt. Middle routers still carry the outer packet although inner `tracert` can show fewer logical hops.
- **Lab 9 FTP/email:** configure addresses/gateways first. FTP server on; account/permissions; PC `ftp <server-IP>`, `dir`, `get`, `put`, `delete`. Email server enables SMTP and POP3, domain and users; PC Email app has address, credentials, incoming/outgoing server. SMTP sends, POP3 receives.

### Fast troubleshooting order

1. Confirm cable/port labels and green link.
2. Check interface `up/up`, correct IP and mask **on the port the cable actually uses**.
3. Ping own gateway, then neighbouring router interface, then remote router, then destination IP.
4. Check `show ip route` for remote network and return path.
5. Check service is ON. If IP works but domain fails, check DNS.

### Most useful IOS commands

```text
enable
configure terminal
interface GigabitEthernet0/0/1
ip address 20.0.0.2 255.0.0.0
no shutdown
exit
router rip
version 2
no auto-summary
network 20.0.0.0
end
show ip interface brief
show ip route
show running-config
show ip protocols
ping 20.0.0.1
copy running-config startup-config
```

Other important commands: `show vlan brief`, `show interfaces trunk`, `show mac address-table` on switches; `ip helper-address <DHCP-IP>` on remote-client-facing router interface; `no ip address` removes a mistaken interface IP; `no ip route ...` removes a mistaken static route. PC Command Prompt uses `ipconfig`, `ping`, and `tracert`.

## The specific Packet Tracer topology we debugged

This was a **three-router practice** topology, not yet the final seven-router Lab 8 requirement:

```text
PC0 1.0.0.1/8 ─ Router0 ─ Router1 ─ Router2 ─ PC1 2.0.0.1/8
gateway 1.0.0.10  10.0.0.1/10.0.0.2  20.0.0.1/20.0.0.2  gateway 2.0.0.10
```

The first failure was that **Router2's interface IPs were on the wrong cable ports**. Workspace List showed PC1 was cabled to Router2 `GigabitEthernet0/0/0`, while Router1 was cabled to Router2 `GigabitEthernet0/0/1`. We corrected Router2 to:

```text
GigabitEthernet0/0/0 → 2.0.0.10/8   (PC1 side)
GigabitEthernet0/0/1 → 20.0.0.2/8  (Router1 side)
```

After that Router2→Router1 ping was 5/5, RIP learned remote networks, and PC0→PC1 ping was **4/4, 0% loss**. RIP entries had been fine; the port/IP mismatch was the actual cause.

The tunnel then used `3.0.0.1` on Router0 and `3.0.0.2` on Router2, both currently `/8`. Router0's tunnel was initially `up/down` because `tunnel source gigabitEthernet0/0` named a nonexistent interface. The valid source was `GigabitEthernet0/0/1`. After correcting it, Tunnel0 became **up/up**, route `S 2.0.0.0/8 via 3.0.0.2` appeared, and Router0 could ping `3.0.0.2` (4 of 5 initial replies; first packet lost while learning).

Working three-router tunnel configuration:

```text
! Router0, left edge
interface tunnel 0
ip address 3.0.0.1 255.0.0.0
tunnel source GigabitEthernet0/0/1
tunnel destination 20.0.0.2
no shutdown
exit
ip route 2.0.0.0 255.0.0.0 3.0.0.2

! Router2, right edge
interface tunnel 0
ip address 3.0.0.2 255.0.0.0
tunnel source GigabitEthernet0/0/1
tunnel destination 10.0.0.1
no shutdown
exit
ip route 1.0.0.0 255.0.0.0 3.0.0.1
```

`tunnel destination` is the far **physical** IP; `ip route` next hop is the far **tunnel** IP. `ip route` destination is the **remote LAN network** with host bits zero. The tunnel network is directly connected; no separate static route to it is needed. A `/30` would be more address-efficient for the tunnel but must be applied to both ends; the working practice topology currently uses `/8`.

## Additional campus-design question from photo

The other photographed tutorial asks for a four-building, two-floor-per-building campus, department isolation, redundant links, DNS names, and capacity for CSAI 2000, CSE 1200, ECE 600, Mechanical 230 PCs (4030 total). It explicitly says **not to show every end-node connection**.

- Hierarchy: Type 1 (64 × 1G, 2 × 10G uplinks) at access; Type 2 (24 × 10G, 2 × 40G uplinks) at building distribution; Type 3 (8 × 40G) at core.
- With approximately even distribution: 4030/8 ≈ 504 PCs per floor; 8 Type 1 access switches per floor, 64 total. Two distribution switches per building give dual uplinks/fallback. Real floor counts may differ, so resize locally when known.
- Separate department VLAN/subnet on each floor (32 logical groups). Department blocks example: CSAI `10.0.0.0/21` as eight `/24`s; CSE `10.0.8.0/21` as eight `/24`s; ECE `10.0.16.0/22` as eight `/25`s; Mech `10.0.20.0/23` as eight `/26`s. This is VLSM; enough room under the even-distribution assumption.
- VLANs isolate Layer 2. To prevent routed traffic crossing departments, use gateway ACLs. Permit required shared services such as DNS/DHCP.
- Department domain is a suffix; each PC needs a unique name such as `pc001.csai.iiitdm.ac.in`, not one identical hostname for every PC.
- In Packet Tracer, demonstrate a representative small subset, including allowed same-department traffic, denied cross-department traffic, DNS resolution, and failover by disabling one uplink.

## Exam writing checklist

For a 1-hour written design question followed by 45-minute implementation, use this structure: **requirements/assumptions → diagram → addresses and protocol choices → message format or VLAN/routing plan → algorithm → code/configuration → tests → technical conclusion**. In the practical, prove the core path first and capture clear evidence. For Packet Tracer submissions, include name/roll in the scene before screenshots when the question asks for it.
