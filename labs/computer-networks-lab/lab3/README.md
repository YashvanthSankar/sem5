# Lab 3: Threads + network topologies

**Question sheet:** [QUESTIONS.md](QUESTIONS.md) — cleaned Q1 and Q2 wording.


## Q1 (socket): shared word list, many clients

New ideas compared to lab 2:
1. **Thread per client**: `threading.Thread(target=handle, args=(conn, addr)).start()` right after `accept()`.
   The main loop goes straight back to `accept()` for the next client.
2. **Shared data + Lock**: `words` and `active` are used by all threads, so we only change them inside `with lock:`.
   Without the lock, two clients adding at the same instant can corrupt the count/list (a **race condition**).
3. **Line messages**: `reader = conn.makefile("r")` and `for line in reader:` gives one message per loop,
   and the loop ends by itself when the client disconnects.

Test: 1 server + 3 clients in 3 terminals; send the same word from two clients to show "no change".

**Viva:**
- *Why `global` in handle?* We assign to `active` (`active += 1`), so Python needs to know it's the module variable.
  (`words.append` doesn't need `global` because it's not reassigning.)
- *What is `daemon=True`?* Thread dies when the main program stops (Ctrl+C works cleanly).
- *Alternative to threads?* `select()` / asyncio, one thread watching many sockets.

## Q2 (Packet Tracer): topologies

| Topology | How to build in PT | Pro | Con |
|---|---|---|---|
| **Bus** | PCs → each to its own switch, switches chained in a line (or PCs on hubs in a line) | cheap, simple | one break kills the line, collisions |
| **Star** | all PCs → one central switch | easy to add/fault-isolate | central device = single point of failure |
| **Ring** | switches connected in a closed loop, a PC on each | equal access | one break can disrupt (STP blocks one link in PT, so the link shows orange) |
| **Mesh** | every switch connected to every other (n(n-1)/2 links) | very reliable, redundant paths | many cables/ports |
| **Tree** | a root switch → child switches → PCs (hierarchy) | scalable, easy to manage | root failure cuts branches |
| **Hybrid** | mix, e.g. a star + a ring + a bus joined together | flexible | complex |

Use the same network (e.g. 10.0.0.1–10.0.0.20 /8 or 192.168.1.x /24) for all PCs so pings work without a router.
For each: ping between two far-away PCs, and show one ping in Simulation mode.
Switch-to-switch links use a **cross-over** cable (PT's automatic cable picks it for you).
