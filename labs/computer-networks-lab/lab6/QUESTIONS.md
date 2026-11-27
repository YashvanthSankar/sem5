# Lab 6 questions

Edited for readability from the original
[socket question](submitted/q_st.txt) and
[Packet Tracer question](submitted/q_cpt.txt).

## Q1 — GUI video transfer through one server

Write `client.py` and `server.py`. The server handles each client in a
separate thread. A client joins with a username; reject duplicates and allow
another choice. Clients must be able to **send and receive `.mp4` files at
the same time** through the server.

The client GUI needs: username field and Connect button; active-user list
and Refresh button; video Browse button and selected full-path label;
packet-size and transmission-delay controls; Send Video button; separate
sending and receiving progress bars; status/output area; Disconnect button.

Before transfer, send metadata: sender and receiver usernames, full video
filename, original byte size, packet size, and number of packets. Split the
video into packets, relay each through the server, reconstruct and save it
at the receiver. Show sender name, video name, original and received sizes.
If the recipient is unavailable, show `User Not Online`.

The server maintains a dynamic `socket → username` list and prints addresses,
names, and active count on joins/leaves. Calculate packet loss at the server
and receiver. Vary packet size and `time.sleep()` delay and record packets
sent, packets received at both points, **server, receiver, and overall loss**,
received file size, and time.
Analyse their effects and create these five graphs:

1. Packet size vs packet loss.
2. Delay vs packet loss.
3. Packet size vs received file size.
4. Delay vs received file size.
5. Packet size vs transmission time.

Test one server with at least two clients, a successful `.mp4` transfer,
duplicate names, active-user refresh, and an offline recipient. Use **4–5
packet sizes and 4–5 delays**. Capture sender GUI, receiver GUI, and server
terminal screenshots. Submit the two programs, screenshots, result tables,
and graphs, with name and roll comments in both programs.

## Q2 — DNS and web server

**A. One LAN:** use one switch, at least three PCs/laptops, a DNS server
named `dns.iiitdm.ac.in`, and a web server. Map a domain name to the web
server's IP and access its hosted page by name from every end device.

**B. Two LANs:** build L512 and L509 with at least five end devices and a
switch in each, joined by a router. Configure a DNS server to resolve
`moodle.com`, `google.com`, and `iiitdm.ac.in` to the server IP. Ensure all
devices use DNS and can communicate across the router. Observe DNS queries
and replies in Simulation mode.

Submit a combined `.pkz` and a PDF with comments, ping, realtime, and
Simulation-mode screenshots. Put name and roll in the Packet Tracer scene
before taking screenshots. Submit individually.
