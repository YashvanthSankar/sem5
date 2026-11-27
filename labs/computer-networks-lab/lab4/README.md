# Lab 4: File upload server + VLANs

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): multi-client file upload with log

The conversation for one client:
```
client → NEW            (or its old username, e.g. "user1", to keep it after reconnecting)
server → user1
client → notes.txt
server → READY          or  "File already exists"  (client may try another name)
client → 11             (file size in bytes, one line)
client → <11 raw bytes, sent in chunks with time.sleep()>
server → Upload Complete for user1_notes.txt
(connection closes, line added to server_log.txt)
```

Key ideas:
- **Send size first, then bytes.** The server reads and saves up to 1024 bytes at a time until it has received that size.
  (Without the size, the server can't tell "file finished" from "still coming".)
- `makefile("rb")` (binary), because files like .pdf/.mp4/.docx are **not text**. Works for all 4 file types.
- `os.path.basename()` strips folders, so a client can't send `../../etc/passwd`.
- `time.sleep(DELAY)` between chunks makes uploads slow enough that 3 clients clearly overlap (the threads interleave).
- Logging = `open("server_log.txt", "a")` (append) + timestamp from `datetime.now().strftime(...)`.
- Saved files go in `uploads/`.

Test: 3 terminals of `client.py`, upload .txt/.docx/.pdf/.mp4, then upload one again to see **Rejected**.

## Q2 (Packet Tracer): VLANs

A **VLAN** splits ONE physical switch into several separate logical networks (separate broadcast domains).
PCs in different VLANs can't talk, even with IPs in the same subnet, unless a router does inter-VLAN routing.

**Part A: one switch**, 4 PCs: 10.10.10.1–.4 /24:
```
Switch> enable
Switch# configure terminal
Switch(config)# vlan 10
Switch(config-vlan)# name SALES
Switch(config-vlan)# vlan 11
Switch(config-vlan)# vlan 12
Switch(config-vlan)# exit
Switch(config)# interface fa0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config-if)# interface fa0/2
Switch(config-if)# switchport access vlan 10
Switch(config-if)# interface fa0/3
Switch(config-if)# switchport access vlan 11
Switch(config-if)# interface fa0/4
Switch(config-if)# switchport access vlan 12
Switch# show vlan brief
```
Ping .1→.2 ✅ (same VLAN), .1→.3 ❌ (different VLAN).

**Part B: two switches**: same VLANs on both switches, and the link between the switches must be a **trunk**
(carries all VLANs, frames tagged with **802.1Q**):
```
Switch(config)# interface g0/1          (the port connecting to the other switch)
Switch(config-if)# switchport mode trunk
```
Do it on both switches. Now VLAN 10 on switch1 ↔ VLAN 10 on switch2 works ✅, VLAN 10 ↔ VLAN 11 ❌.

**Viva:** access port = one VLAN (to a PC); trunk port = many VLANs (switch↔switch); native VLAN = 1 (untagged);
why VLANs: security, smaller broadcast domains, group users by department not by location.
