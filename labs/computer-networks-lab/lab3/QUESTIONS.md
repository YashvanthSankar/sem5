# Lab 3 questions

Edited for readability from the original
[socket question](submitted/q_st.txt) and
[Packet Tracer question](submitted/q_cpt.txt).

## Q1 — One server, multiple threaded clients

Write a Python server that starts **one thread per client**. Maintain one
shared, comma-separated string of words on the server.

For each word a client sends:

1. If the word already exists, leave the string unchanged.
2. Otherwise, append the word, separated by a comma.
3. Return the latest full string, even when nothing changed.

Close that client's connection when it sends `exit`. Print the active
connection count whenever a client joins or leaves.

## Q2 — Network topologies in Packet Tracer

Design and simulate **bus, star, ring, mesh, tree, and hybrid** topologies.
For the topology demonstrations, include ping and Simulation-mode
screenshots with comments.

Submit a PDF showing your name and roll number in the Packet Tracer scene
before screenshots. Submit a ZIP with the `.pkz` file(s); the topologies may
be separate or combined. Submit individually before the deadline.
