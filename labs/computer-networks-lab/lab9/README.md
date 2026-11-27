# Lab 9: Role-based file access + FTP & Email servers

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): role-based access control

For a shorter terminal-only learning version, see [cli/README.md](cli/README.md).

Test accounts (in `USERS` in server.py): `stud1/s123` Student, `fac1/f123` Faculty, `admin1/a123` Administrator.

**GUI:** `client.py`: login fields, file list (click one, then READ), category dropdown + UPLOAD/UPDATE
(opens a file picker), output box, EXIT. No thread needed (one request → one reply per button).

The GUI buttons send `LIST`, `READ category filename`, `UPLOAD category filename size`, `UPDATE category filename size`, or `EXIT` to the server.

The heart of the program, 3 lines:
```python
STUDENT = {("academic", "READ")}
FACULTY = STUDENT | {("academic", "UPLOAD"), ("academic", "UPDATE"), ("administrative", "READ")}
ADMIN   = FACULTY | {("administrative", "UPLOAD"), ("administrative", "UPDATE")}
```
`|` is set union, so each role literally **contains** the lower role's permissions (hierarchy/inheritance).
Every request checks `if (category, op) not in PERMISSIONS[role]: DENIED`. That check is **on the server**,
because a modified client could send anything. Never trust the client.

Other ideas:
- Login → server replies `OK Faculty READ:academic READ:administrative ...` (the operations you're allowed).
- READ reply = `OK <size>` + bytes (like lab 4, in the other direction). UPLOAD/UPDATE = header with size + bytes.
- On UPLOAD the server **reads the bytes even if it will deny**; otherwise those bytes would be read as the next command.
- Log line per request: user, role, operation, file, timestamp, Allowed/Denied, modifications, disconnect.
- Preloaded files are created in `server_files/academic` and `server_files/administrative` on first run.

Demo: student read academic ✅ / read administrative ❌ / upload ❌; faculty read administrative ✅,
upload academic ✅, update administrative ❌; admin update administrative ✅.

## Q2 (Packet Tracer): FTP server + Email server

**Topology (both parts):** server LAN 192.168.1.0/24 (server = 192.168.1.10, router g0/0 = .1) ↔ router ↔
client LAN 192.168.2.0/24 (2 PCs, gateway 192.168.2.1). Configure router like lab 2.

**FTP:**
1. Server → Services → **FTP** → ON. Add user: username `yash`, password `123`, tick Write/Read/Delete/Rename/List → Add.
2. PC → Command Prompt:
   ```
   ftp 192.168.1.10
   Username: yash
   Password: 123
   ftp> dir                     (list files on server)
   ftp> get sample.txt          (download)
   ftp> put myfile.txt          (upload: first create it in PC → Desktop → Text Editor)
   ftp> delete myfile.txt
   ftp> quit
   ```
3. Simulation, filter FTP/TCP: see the TCP handshake, then FTP commands (USER, PASS, RETR, STOR).
   FTP uses **TCP 21** (control) and **20** (data).

**Email:**
1. Server → Services → **EMAIL** → SMTP ON, POP3 ON, domain `iiitdm.com` → Set.
   Add users: `alice/123`, `bob/123`.
   (Optional: DNS service on the same server, A record `mail.iiitdm.com` → 192.168.1.10.)
2. PC0 → Desktop → **Email** → Configure: Name Alice, Email `alice@iiitdm.com`,
   Incoming (POP3) server `192.168.1.10`, Outgoing (SMTP) `192.168.1.10`, username `alice`, password `123` → Save.
   Same on PC1 for bob.
3. Alice: Compose → to `bob@iiitdm.com` → Send. Bob: **Receive** → open → **Reply**. Alice: Receive.
4. Simulation, filter SMTP + POP3: **SMTP** (TCP **25**) carries the mail from client to server when *sending*;
   **POP3** (TCP **110**) is used by the client to *download* mail from the server when you press Receive.
