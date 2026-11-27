# Lab 1: Linux network commands + cables in Packet Tracer

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1. Linux networking commands (know purpose + 2 options each)

| Command | What it tells you | Options to remember |
|---|---|---|
| `ifconfig` | your interfaces, IP, MAC, netmask | `ifconfig en0` (one interface), `-a` (all, even down) |
| `ip` | modern replacement for ifconfig/route (Linux) | `ip a` (addresses), `ip r` (routing table), `ip link` (interfaces) |
| `ping` | is a host reachable? round-trip time (uses **ICMP** echo) | `-c 4` (send 4 only), `-i 2` (interval), `-s 100` (packet size) |
| `traceroute` | every router (hop) on the path to a host | `-n` (no DNS names, faster), `-m 10` (max hops) |
| `tracepath` | like traceroute, no root needed, also shows **MTU** | `-n` |
| `netstat` | open connections / listening ports / routes | `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric, `-r` routing table → `netstat -tuln` |
| `ss` | faster netstat (socket statistics) | `ss -tuln`, `ss -s` (summary), `ss -tp` (with process) |
| `dig` | DNS lookup, detailed | `dig google.com`, `dig google.com MX`, `+short`, `dig @8.8.8.8 google.com` |
| `nslookup` | DNS lookup, simple | `nslookup google.com`, `nslookup -type=mx google.com` |
| `host` | DNS lookup, shortest output | `host google.com`, `host -t ns google.com`, `host 8.8.8.8` (reverse) |
| `arp` | IP → MAC table of your LAN | `arp -a`, `arp -n` |
| `hostname` | your computer's name | `hostname -I` (Linux: your IPs) |
| `curl` / `wget` | fetch a URL over HTTP | `curl -I url` (headers only), `curl -o f url` (save), `wget url` |
| `whois` | who registered a domain | `whois google.com` |
| `iftop` | live bandwidth per connection (needs sudo) | `sudo iftop -i en0`, `-n` |

Quick facts examiners like:
- `ping` uses **ICMP**, `traceroute` works by sending packets with increasing **TTL** (1, 2, 3…); each router that drops a TTL=0 packet replies, revealing itself.
- DNS record types: **A** (IPv4), **AAAA** (IPv6), **MX** (mail), **NS** (name server), **CNAME** (alias).
- `netstat -tuln` = TCP + UDP + listening + numeric: "which ports is my machine listening on?"

## Q2. Cables in Packet Tracer

**Rule of thumb:**
- **Straight-through**: connects *different* kinds of device: PC↔Switch, PC↔Hub, Switch↔Router.
- **Cross-over**: connects the *same* kind of device: PC↔PC, Switch↔Switch, Router↔Router, and also **PC↔Router**
  (PC and router are both "DTE" devices, so they're treated as the same kind).

Straight-through: both ends wired the same (T568B–T568B). Cross-over: one end T568A, the other T568B
(pins 1↔3 and 2↔6 swapped, so one side's transmit goes into the other side's receive).

**The 4 experiments (PC0 ↔ PC1 directly):**

| Cable | Same network (192.168.1.1 & .2, mask 255.255.255.0) | Different networks (192.168.1.1 & 192.168.2.1) |
|---|---|---|
| Straight | Link is **red** (wrong cable, no link). Ping fails | Fails |
| Cross-over | Link **green**, ping **succeeds** | Link green but ping **fails**: different networks need a **router** (no default gateway) |

How to do it: drag 2 PCs → pick the cable (Connections, the lightning icon) → click PC0 FastEthernet0 → PC1 FastEthernet0 →
PC → Desktop → IP Configuration → set IP + mask → Desktop → Command Prompt → `ping 192.168.1.2`.

(In real modern hardware **Auto-MDIX** fixes the wrong cable automatically. That's a good viva point.)

**CAT-6 cable**: Category 6 twisted pair, up to **1 Gbps (10 Gbps for ≤55 m)**, 250 MHz, 100 m max.
8 wires in 4 twisted pairs. T568B colours, pins 1→8:
white-orange, **orange**, white-green, **blue**, white-blue, **green**, white-brown, **brown**.
Pins 1,2 = transmit (TX+/TX-), 3,6 = receive (RX+/RX-), 4,5,7,8 = used for gigabit / PoE.
Twisting reduces crosstalk/interference.
