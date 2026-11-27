# Lab 7: Rock–Paper–Scissors + DHCP

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): Rock–Paper–Scissors for 2 players

For a shorter terminal-only learning version, see [cli/README.md](cli/README.md).

The question allows any multiplayer game. Rock–Paper–Scissors keeps the same
network requirements with fewer rules to memorize. Use the `client.py` window:
Join or Random name, choose rock/paper/scissors, chat, then REPLAY or EXIT.

Protocol:
```
client: NAME ann  | RANDOM             server: OK ann  | TAKEN ...
server: WAIT ...                       (1st/3rd/5th player waits)
server: START bob                      (two players paired)
client: CHOICE rock                    server: WAIT for opponent
other:  CHOICE scissors                server → both: RESULT ann wins!
client: CHAT hi                        server → opponent: CHAT ann: hi
client: REPLAY  (back into queue)       or EXIT
```

Key ideas:
1. **FIFO pairing**: `waiting` is a list; `append` on join, and when it has 2 players `pop(0)` twice and start a `Game`.
   1st+2nd play, 3rd waits for 4th. REPLAY just calls `join_queue` again.
2. **The server chooses the winner** after both choices arrive; the client only sends a choice.
3. **Opponent leaves** → the remaining player receives a win message.
4. Each player's thread changes the shared waiting list and pair, so commands run inside `with lock:`.
5. Client = listener thread (queues game/chat messages) + Tkinter buttons. Same as lab 5.

**GUI:** `client.py`: Join / Random name, three choice buttons, chat box,
REPLAY / EXIT. Listener thread → queue → `refresh()`, same as lab 5.

The old `submitted/q1.pdf` was captured for the earlier game; take new screenshots
of this code if using it for an assessment.

## Q2 (Packet Tracer): DHCP

**A. One LAN:** switch + 6 PCs + "IIITDM DHCP Server" + Web server.
1. DHCP server: static IP **192.168.1.2**, mask 255.255.255.0, gateway 192.168.1.1.
   Services → **DHCP** → ON → Default gateway 192.168.1.1, DNS 0.0.0.0 (or web server IP),
   **Start IP 192.168.1.12**, mask 255.255.255.0, max users 50 → **Save**.
2. Web server: static **192.168.1.5**, HTTP on, edit index.html (name, roll).
3. Each PC: IP Configuration → **DHCP** → gets 192.168.1.12, .13, ... automatically.
4. Browser on PC → `192.168.1.5`.
5. Simulation, filter DHCP: you'll see **D-O-R-A**:
   **Discover** (PC broadcasts "any DHCP server?") → **Offer** (server offers an IP) →
   **Request** (PC: "I'll take that one") → **Acknowledge** (server confirms; IP is leased).

**B. Two LANs + router, DHCP server on the L512 side:**
- L512 192.168.12.0/24, router g0/0 = 192.168.12.1; L509 192.168.9.0/24, router g0/1 = 192.168.9.1.
- DHCP server static 192.168.12.100, gateway 192.168.12.1. Two pools in Services → DHCP:
  - `L512`: gateway 192.168.12.1, start **192.168.12.15**, mask /24
  - `L509`: gateway 192.168.9.1, start **192.168.9.115**, mask /24
- **DHCP Discover is a broadcast and routers don't forward broadcasts**, so on the router's L509 interface:
  ```
  Router(config)# interface g0/1
  Router(config-if)# ip helper-address 192.168.12.100
  ```
  The router relays L509's DHCP requests to the server (as unicast). The pool is picked by the gateway address.
- Set all PCs to DHCP, check IPs, ping within and across LANs.

**Viva:** DHCP ports UDP **67** (server) / **68** (client); DORA; lease time; advantages: no manual config,
no duplicate IPs, easy to change gateway/DNS for everyone; `ip helper-address` = DHCP relay agent.
