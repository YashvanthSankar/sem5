# Lab 5 questions

Edited for readability from the original
[socket question](submitted/q_st.txt) and
[Packet Tracer question](submitted/q_cpt.txt).

## Q1 — Multi-client GUI chat

Write a Python socket chat system with **one server thread per client** and
GUI interaction for both client and server in the local demonstration. A client proposes a username on connection; the server
accepts an unused name or asks for another. Names can change on reconnect.
Keep an active `socket → username` list and remove disconnected users.

The client GUI and server must support:

| Request | Required server response |
|---|---|
| `/users` | Return the names of currently active users. |
| `<username>:message` | Deliver the message with sender name, or return `User Not Online`. |
| `<broadcast>:message` | Deliver to every active user except the sender. |
| `/exit` | Disconnect and remove the user from the active list. |

The server must show the active count and list (socket address and username)
on every join/leave. `log.txt` must record username conflicts, join time,
leave time and session duration, and each message's sender, recipient, size,
and sent/failed status with reason.

**Demonstrate:** one server and three clients locally; duplicate username;
offline/nonexistent recipient; all four requests. Repeat with a friend's
server and another friend's client, then reverse roles and run your server
for two friends. For assessed runs, hardcode and display a real network IPv4;
do not use `gethostbyname()`, `0.0.0.0`, `localhost`, or `127.0.0.1`.
Show both socket addresses on the client and log local/network sessions
separately.

Put name and roll comments in both programs. Submit one screenshot PDF with
local and network runs, name and roll on every page, plus `client.py`,
`server.py`, `local_log.txt`, and `network_log.txt` as separate files.

## Q2 — WLAN and combined LAN/WLAN

**A.** Build a WLAN with a wireless router such as WRT300N and a mix of PCs
and laptops.

**B.** Build one IP network containing a switched LAN with **more than two**
end devices and a WLAN with **at least two** end devices, including PCs and
laptops. Connect the WLAN through a wireless router and verify communication
between every LAN and WLAN device.

Submit one combined `.pkz` and a PDF with comments, ping, realtime, and
Simulation-mode screenshots. Put name and roll in the Packet Tracer scene
before taking screenshots. Submit individually before the deadline.
