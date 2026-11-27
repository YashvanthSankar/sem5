# Lab 8: Quiz app + VPN tunnel

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): quiz, scored by the server

For a shorter terminal-only learning version, see [cli/README.md](cli/README.md).

Protocol (strict ask → answer, so the client needs **no thread**):
```
client: yash                          server: OK Welcome yash   (or TAKEN)
server: QUESTIONS 5
server: Which layer does TCP belong to?|Network|Transport|Session|Data Link     (×5)
client: ANSWERS B,C,-,B,B             ("-" = skipped)
server: SCORE 4/5 | Q1 correct, Q2 correct, Q3 wrong (answer C), ...
client: REPLAY  (server sends the questions again)  |  EXIT
```

Key ideas:
- Questions + correct answers exist **only on the server**. The client never sees the answer key.
  Checking and scoring = the loop in `run_quiz`. (This is the point of the question.)
- Splitting a line: `"q|A|B|C|D".split("|")` → `[q, A, B, C, D]`; `q, *options = parts` unpacks it.
- Duration = `time.time()` at start and end; server prints join/leave/start/end/answers/score/time.

**GUI:** `client.py` does exactly this: a Label for the question, 4 `tk.Radiobutton`s sharing one `tk.StringVar`
(that's "save choice"), a Reset button doing `var.set("")`, Next/Prev buttons changing an index,
Submit sending `ANSWERS ...`. No thread needed here either.

## Q2 (Packet Tracer): GRE tunnel with five intermediate routers

Use **seven routers total**: `PC0 — R1 — R2 — R3 — R4 — R5 — R6 — R7 — PC1`.
R2–R6 are the **five intermediate routers** required by the question. R1 and
R7 connect to the end LANs and form the tunnel.

| Link | Network and example addresses |
|---|---|
| PC0 LAN | 10.0.0.0/24; R1 g0/0 = 10.0.0.1, PC0 = 10.0.0.2 |
| R1–R2 | 20.0.0.0/24; R1 g0/1 = 20.0.0.1, R2 g0/0 = 20.0.0.2 |
| R2–R3 | 30.0.0.0/24 |
| R3–R4 | 40.0.0.0/24 |
| R4–R5 | 50.0.0.0/24 |
| R5–R6 | 60.0.0.0/24 |
| R6–R7 | 70.0.0.0/24; R6 = 70.0.0.1, R7 g0/0 = 70.0.0.2 |
| PC1 LAN | 80.0.0.0/24; R7 g0/1 = 80.0.0.1, PC1 = 80.0.0.2 |

1. Assign both ends of every router link different addresses in its listed
   /24, then use `no shutdown`. Set the PC gateways to 10.0.0.1 and 80.0.0.1.
2. Establish ordinary routing first. On each router, enable RIPv2 and list
   its directly connected networks. For R2, for example:
   ```
   router rip
   version 2
   no auto-summary
   network 20.0.0.0
   network 30.0.0.0
   ```
   Check that PC0 can ping PC1 **before** adding a tunnel.
3. From PC0, run `tracert 80.0.0.2` and save the result. It should show
   the edge and intermediate router hops.
4. On R1, configure the tunnel towards R7 and route PC1's LAN through it:
   ```
   interface tunnel 0
   ip address 192.168.1.1 255.255.255.0
   tunnel source g0/1
   tunnel destination 70.0.0.2
   exit
   ip route 80.0.0.0 255.255.255.0 192.168.1.2
   ```
5. On R7, configure the reverse tunnel and route PC0's LAN through it:
   ```
   interface tunnel 0
   ip address 192.168.1.2 255.255.255.0
   tunnel source g0/0
   tunnel destination 20.0.0.1
   exit
   ip route 10.0.0.0 255.255.255.0 192.168.1.1
   ```
6. Ping again, then run `tracert 80.0.0.2` again. The inner packet crosses
   the GRE tunnel, so the trace normally shows the tunnel endpoint instead
   of listing R2–R6 separately. Those routers still carry the *outer* packet.

The static LAN routes beat RIPv2 routes (administrative distance 1 vs 120).
GRE provides encapsulation, **not encryption**; IPsec would be needed for
an encrypted VPN. Take the required realtime, simulation, ping, and both
traceroute screenshots with your name and roll number visible.
