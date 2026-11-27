# Lab 2: First client/server + network devices

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): lowercase server

Run: `python3 server.py` then in another terminal `python3 client.py`.

The flow, the whole lab in 5 lines:
```
server: socket → bind(HOST, PORT) → listen → accept  (waits here)
client: socket → connect(HOST, PORT)                 (accept returns: connected!)
client: sendall("HeLLo")      → server: recv → .lower()
server: sendall("hello")      → client: recv → print
both:   close
```
Network test: friend runs server, you set `HOST` in client.py to the friend's IP. Then swap roles.

Here `recv(1024)` is fine because exactly one short message goes each way.
From lab 3 on, we use lines (`"\n"`), see [../00_basics/LESSON.md](../00_basics/LESSON.md).

**Viva:**
- *Why does the server have two sockets?* `server` only listens for new clients; `accept()` returns a new `conn` per client used for talking.
- *TCP vs UDP?* TCP (`SOCK_STREAM`): connection, reliable, ordered. UDP (`SOCK_DGRAM`): no connection, can lose packets, faster, uses `sendto/recvfrom`.
- *Why encode()?* Sockets carry bytes, not Python strings.
- *What's a socket address?* (IP, port) pair. The client's port is picked randomly by the OS (an "ephemeral port").

## Q2 (Packet Tracer): hub, switch, router, repeater, bridge

| Device | Layer | What it does with a frame/packet | Collision domain | Broadcast domain |
|---|---|---|---|---|
| **Repeater** | 1 Physical | regenerates bits; does not inspect addresses | does not split the collision domain | does not split the broadcast domain |
| **Hub** | 1 Physical | copies it to **every** port | one for all ports | one |
| **Bridge** | 2 Data link | learns MACs, forwards between 2 segments | one per side | one |
| **Switch** | 2 Data link | learns MACs; forwards known unicast to the right port, but floods broadcasts and unknown destinations | one **per port** | one |
| **Router** | 3 Network | forwards by **IP** between **different networks** | per port | **one per port** (stops broadcasts) |

Build the hub, switch, repeater, and bridge examples with PCs in the same subnet (for example, 192.168.1.x/24). The router example needs two different subnets:
1. **Hub**: PCs → Hub (straight cables). In **Simulation mode**, ping: the packet goes to *all* PCs, and the wrong ones drop it.
2. **Switch**: same with a 2960 switch. First ping: ARP broadcast to all; after that only to the target. Show `show mac address-table` in switch CLI.
3. **Repeater**: (Network Devices → Repeater) between two PCs/segments: just extends the cable.
4. **Bridge**: two hubs joined by a Bridge: traffic stays on its own side unless destination is across.
5. **Router**: 2 switches with different networks (192.168.1.0 and 192.168.2.0), router in the middle:
   ```
   Router> enable
   Router# configure terminal
   Router(config)# interface g0/0
   Router(config-if)# ip address 192.168.1.1 255.255.255.0
   Router(config-if)# no shutdown
   Router(config-if)# interface g0/1
   Router(config-if)# ip address 192.168.2.1 255.255.255.0
   Router(config-if)# no shutdown
   ```
   Set each PC's **Default Gateway** = router IP on its side (192.168.1.1 / 192.168.2.1). Ping across.

Simulation mode tip: click **Simulation** (bottom right) → Edit Filters → keep ICMP/ARP → send ping → **Capture/Forward** step by step.
