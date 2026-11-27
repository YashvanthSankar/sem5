# Lab 4 questions

Q1 is edited for readability from [the original socket question](submitted/q_st.txt).
The [Q2 submitted PDF](submitted/q2.pdf) contains the VLAN work, but the
original Q2 question text was **not saved** (`submitted/q_cpt.txt` is empty).
The Q2 section below is a study prompt reconstructed from that PDF, not a
verbatim exam question.

## Q1 — Threaded file-upload server

Write `client.py` and `server.py` with **one server thread per client**.

1. On connection, assign and immediately send a unique username (`user1`,
   `user2`, …). A reconnecting client must keep its username.
2. The client sends a local filename. If the destination already exists,
   reply exactly `File already exists` and reject the transfer. Otherwise,
   reply `READY`.
3. After `READY`, the client sends file content in chunks with small
   `time.sleep()` delays. Save it as `clientusername_<filename>` (for the
   text-file example, `clientusername_<filename>.txt`).
4. Reply `Upload Complete for clientusername_<filename>` after a successful
   save, then close the connection. On rejection, let the client try another
   filename or exit.
5. Print the active client count on every connection and disconnection.
   Record each accepted/rejected transfer in `server_log.txt`: timestamp,
   server/client socket addresses, username, filename, action, and size when
   accepted.

**Required demonstrations:** upload `.txt`, `.docx`, `.pdf`, and `.mp4`; run
one server and three local clients simultaneously; then upload to a friend's
server. Hardcode a real network IPv4 (such as `192.168.x.x` or `172.16.x.x`)
for the assessed runs. Do not use `gethostbyname()`, `0.0.0.0`, `localhost`,
or `127.0.0.1`. Print addresses, username, filename, status, decision,
confirmation, and active count without printing file contents.

Put your name and roll number in both program files. Submit screenshots of
programs, outputs, and logs for **local and friend-network** runs in one PDF,
with name and roll on every page. Submit the PDF, `client.py`, `server.py`,
`local_server_log.txt`, and `network_server_log.txt` as separate files.

## Q2 — VLANs (reconstructed from the submitted PDF)

- **Part A:** Put four PCs on one switch: `10.10.10.1` and `.2` in VLAN 10,
  `.3` in VLAN 11, and `.4` in VLAN 12. Show that `.1 → .2` succeeds while
  `.1 → .3` fails.
- **Part B:** Use two switches joined by a trunk. Put corresponding VLANs
  10, 11, and 12 on both switches. Show communication across switches within
  VLAN 10 and failure across different VLANs.
- **Part C:** Explain the four combinations of same/different VLAN and
  same/different IP network, and when a router or Layer 3 switch is needed.

Use [the original Q2 PDF](submitted/q2.pdf) and [saved Packet Tracer
topology](submitted/q2.pkz) to compare your reconstruction.
