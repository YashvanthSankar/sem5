# Lab 8 questions

Edited for readability from the original
[socket question](submitted/q_st.txt) and
[Packet Tracer question](submitted/q_cpt.txt).

## Q1 — GUI quiz scored by the server

Write `server.py` and `client.py` with Tkinter GUIs. The server stores a
preloaded set of multiple-choice questions, each with four options and a
correct answer.

1. The client chooses a username. If it is in use, ask for another.
2. The server sends questions and receives answers. **Only the server**

   checks answers and calculates the final score.
3. The client GUI displays the question and options and offers Save Choice,

   Reset Choice, and navigation as designed. Display the final score.
4. After the quiz, offer **REPLAY** and **EXIT**.
5. The server GUI logs joining/leaving, username, socket address, quiz

   start/end, answers, score, and duration.

Test in both roles: your server with a friend's client and your client with
a friend's server. Capture GUI screenshots for connection, questions, score,
completion, replay, and exit. Put name and roll comments in both programs;
submit `server.py`, `client.py`, and `Quiz_Screenshots.pdf` separately. Put
name and roll on every PDF page.

## Q2 — Routed LANs and a tunnel

Create two LANs with at least one end device each. Connect them through
**at least five intermediate routers**. Configure addresses and routing so
end devices communicate.

1. Before the tunnel, run `tracert` from one end device to the other and

   record the path.
2. Configure a tunnel between the routers attached to the end LANs. Route

   the required LAN traffic through it and verify ping/connectivity.
3. Run `tracert` again. Compare both paths and explain the tunnel's effect.

The question supplies this CLI pattern (replace interfaces and addresses
with those in your topology):

```text
interface tunnel 0
ip address 192.168.1.1 255.255.255.0
tunnel source Gig0/0
tunnel destination <remote-router-interface-IP>
ip route <destination-network> <mask> <other-tunnel-IP>
```

The submitted text calls this a “VPN”; the listed commands create a GRE
tunnel and do not by themselves provide encryption. See [README.md](README.md)
for a seven-router study topology that satisfies the five-*intermediate*-
router count.

Submit one combined `.pkz` and a PDF with observations, ping, both
traceroutes, realtime, and Simulation-mode screenshots. Put name and roll
in the Packet Tracer scene before screenshots. Submit individually.
