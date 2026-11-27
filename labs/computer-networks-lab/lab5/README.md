# Lab 5: Chat server (+ Tkinter) + Wireless LAN

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): chat between clients

Files: `server.py` and `client.py` (Tkinter). The server window shows joins, leaves, messages, and logs.

Commands a client sends (one line each):
| Send | Server does |
|---|---|
| `/users` | replies `USERS alice, bob` |
| `bob:hi` (or `<bob>:hi`) | forwards `MSG alice: hi` to bob, or replies `ERROR User Not Online` |
| `broadcast:hello` | sends to everyone except the sender |
| `/exit` | removes you from `clients`, logs session duration |

Key ideas:
1. **`clients = {conn: username}`** is the "socket:user_name" list. Join = add, leave = `pop`. Always inside `with lock:`.
2. **Forwarding** = the server finds the target's `conn` and calls `send_line(target_conn, ...)` *from the sender's thread*.
3. **Client needs a listener thread**, because a message can arrive at any time.
   Button actions send; the listener thread receives and queues messages for Tkinter. (Lesson section 4.)
4. Username check loop: send name → `TAKEN` → ask again → `OK`.
5. Session time = `datetime.now() - joined` at leave.

**Tkinter in 60 seconds** (`client.py`):
```python
root = tk.Tk()                                # the window
box = tk.Text(root); box.pack()              # widget, then pack() to place it
entry = tk.Entry(root); entry.pack()         # entry.get() reads what's typed
tk.Button(root, text="Send", command=fn).pack()   # fn() runs on click
root.mainloop()                              # starts the window (blocks forever)
```
The only tricky rule: **don't touch widgets from your socket thread**. Thread → `queue.put(line)`;
`root.after(100, check_queue)` → main thread takes lines from the queue and inserts them in the Text box.

## Q2 (Packet Tracer): WLAN

**A. Wireless LAN with WRT300N:**
1. Add **Wireless Router WRT300N** (Network Devices → Wireless Devices), 2 PCs + 2 Laptops.
2. Router → GUI → Wireless: set **SSID** (e.g. `IIITDM_CS24I1029`); Wireless Security: **WPA2 Personal**, passphrase.
   Setup tab: the router's LAN IP 192.168.0.1 and **DHCP enabled** by default.
3. For each laptop/PC: power off (click power button in Physical tab) → drag out the Ethernet card →
   drag in **WPC300N** (wireless card) → power on.
4. Each device: Desktop → **PC Wireless** → Connect → pick SSID → enter passphrase. (Or Config → Wireless0 → SSID + WPA2 key.)
5. Desktop → IP Configuration → **DHCP**: gets 192.168.0.100+. Ping between devices; show in Simulation.

**B. LAN + WLAN in ONE network:**
- Switch with 3+ PCs, wireless router with 2+ wireless devices, connect **switch ↔ one of the router's LAN ports
  (Ethernet 1–4, not the Internet port)**.
- Then everything is one network: the router's DHCP gives the wired PCs IPs too (set them to DHCP),
  or give all devices static IPs in 192.168.0.x /24.
- Ping wired ↔ wireless both ways to prove they're one network.

**Viva:** SSID = network name; WPA2 = encryption; wireless = IEEE **802.11**, wired = **802.3**;
the router's LAN ports are just a built-in switch, which is why B is "one network".
