# Lab 9 questions

Q1 is edited for readability from [the original socket question](submitted/q_st.txt).
The Q2 text file is empty, so Q2 below is taken from the submitted
[Q2 PDF](submitted/q2.pdf), which includes the full question wording.

## Q1 — GUI role-based file access

Build `server.py` and `client.py` using Python sockets and Tkinter. The
server starts with files in categories such as **Academic** and
**Administrative**, and has users with credentials and hierarchical roles:

| Role | Allowed file operations |
|---|---|
| Student | View/download Academic files. |
| Faculty | All Student rights; upload/update Academic files; view/download Administrative files. |
| Administrator | All Faculty rights; upload/update Administrative files. |

- Validate username and credentials before access. Send the client the
  operations available to its role and relevant files.
- Support **LIST, READ/DOWNLOAD, UPLOAD, UPDATE, EXIT**. The **server** must
  enforce all permissions; do not trust the client to decide access.
- Deny out-of-role requests with an explanatory response.
- Log username, role, requested file, operation, timestamp, allowed/denied
  result, file modifications, and disconnects.
- The client GUI shows files, available operations, server responses, and
  access status, and provides a safe EXIT action.

Demonstrate one server and one client using all three roles, including
inheritance, allowed access, denied access, and modification. Capture both
GUIs and server logs in one PDF with name and roll on every page. Put name
and roll comments in both programs; submit `server.py`, `client.py`, and
`FileAccess_Screenshots.pdf` separately.

## Q2 — FTP and email in Packet Tracer

**FTP:** configure an FTP server with a static IP, username, and password.
Put at least two PCs in a different LAN and connect the LANs through a
router. Configure addresses/routing, log in to FTP from the PCs, and verify
`dir`, `get`, `put`, and `delete`. Capture command output and FTP packets in
Simulation mode.

**Email:** configure an Email Server with required services, domain, and
user accounts. Put at least two PCs in another LAN connected through a
router. Configure each email client with address, username/password,
incoming server, and outgoing server. Send, receive, and reply to a message.
Verify SMTP and POP3 activity in Simulation mode.

Submit one combined `.pkz` and a PDF with comments, ping, realtime, and
Simulation-mode screenshots. Put name and roll in the Packet Tracer scene
before screenshots. Submit individually.
