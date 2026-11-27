# CN Endsem Portions

Prepared on 23 November 2026 from the materials in `ambika_slides/` and `sanjeet_slides/`.

This is a combined study checklist of the supplied teaching material. The folders identify the two professors' sets; several files in Ambika's folder retain Dr Noor Mahammad Sk's name on their slides. Common topics are listed once below, with differences identified separately.

**Scope:** No separate endsem exclusion notice or midsem cutoff was supplied in these folders. Therefore, this checklist includes the full supplied material, including introductory topics. It does not claim that every topic has been independently confirmed for the exam.

## 1. Source inventory

Page numbers below refer to PDF pages; slide numbers refer to PPTX slides.

### Ambika's set

| File | Pages / slides | Actual coverage |
| --- | ---: | --- |
| `ambika_slides/cn01_noor.pptx` | 110 slides | Network requirements, resource sharing, services, reliability, architecture, layering, encapsulation, OSI and Internet architecture |
| `ambika_slides/cn02_noor.pptx.pdf` | 70 pages | Socket programming, protocol implementation, process models, message buffers, network performance |
| `ambika_slides/cn03_noor.pptx.pdf` | 179 pages | Direct links, Shannon capacity, encoding, framing, SONET, error detection, reliable transmission, Ethernet, token rings, FDDI, wireless LANs |
| `ambika_slides/cn05_noor.pptx.pdf` | 80 pages | IPv4, subnetting, CIDR, forwarding, ARP, DHCP, ICMP, routing, IPv6, multicast, Mobile IP |
| `ambika_slides/cn06_noor.pptx` | 62 slides | UDP, TCP, flow control, retransmission, RPC with BLAST, CHAN and SELECT |
| `ambika_slides/congestion_control.pptx` | 26 slides | TCP congestion control: AIMD, slow start, fast retransmit and fast recovery |
| `ambika_slides/Spanning Tree Protocol.pdf` | 7 pages | STP initialization, BPDUs, comparison rules, root selection, port roles and reconvergence |
| `ambika_slides/Internetworking - practice questions.pdf` | 2 pages | Six questions on subnetting, longest prefix matching, fragmentation and forwarding |

### Sanjeet sir's set

| File | Pages | Actual coverage |
| --- | ---: | --- |
| `sanjeet_slides/cn01-Final-Upload-2026.pdf` | 206 | Network evolution, topologies, requirements, architecture, sockets, implementation and performance; also contains course administration pages |
| `sanjeet_slides/cn02-Final-2026-Upload.pdf` | 142 | Direct links, encoding, framing, parity, checksum, CRC, reliable transmission, Ethernet and wireless LANs |
| `sanjeet_slides/cn03-2026-Upload.pdf` | 62 | Packet switching, datagrams, virtual circuits, source routing, learning bridges and spanning tree |
| `sanjeet_slides/cn04-2026-Upload.pdf` | 61 | Internetworking, IPv4, subnetting, CIDR, ARP, DHCP, ICMP, distance vector, link state, RIP, OSPF and IPv6 |
| `sanjeet_slides/cn05-2026-Upload.pdf` | 46 | UDP and TCP through adaptive retransmission; no detailed RPC section |
| `sanjeet_slides/cn06-2026-Upload.pdf` | 122 | Resource allocation, queues, TCP congestion control, congestion avoidance, QoS, IntServ, RSVP and DiffServ |

**Total supplied material: 14 files, 1,175 pages/slides.** The two professors use different file numbering: for example, Ambika's `cn05` corresponds largely to Sanjeet sir's `cn04`.

## 2. Foundations and network architecture

**Sources:** Ambika `cn01`; Sanjeet `cn01`, especially pp. 24-134. Sanjeet's history is on pp. 2-7 and topologies on p. 31.

### Network fundamentals

- [ ] Evolution of networks: telephone networks, stand-alone computers, ARPA/ARPANET and the Internet.
- [ ] Internet versus intranet; heterogeneous systems and why they need communication standards.
- [ ] Transmission media: twisted pair, coaxial cable, optical fibre and wireless.
- [ ] Bus, ring, mesh, star, tree and hybrid topologies.
- [ ] Nodes and links; point-to-point versus multiple-access links.
- [ ] Direct and indirect connectivity; scalability limitations of direct links.
- [ ] Switches, routers/gateways and interconnection of networks.
- [ ] Circuit switching versus packet switching; store-and-forward operation.
- [ ] Addressing and routing; unicast, broadcast and multicast.

### Network requirements and services

- [ ] Connectivity, cost-effective resource sharing and support for common services.
- [ ] Multiplexing and demultiplexing.
- [ ] Synchronous time division multiplexing (STDM), frequency division multiplexing (FDM) and their limitations.
- [ ] Statistical multiplexing: demand-based sharing, packets, fairness and congestion.
- [ ] FIFO and round-robin scheduling as introductory sharing examples.
- [ ] Logical process-to-process channels versus host-to-host connectivity.
- [ ] Request/reply channels and message-stream channels; file access and video examples.
- [ ] Reliability requirements: bit errors, lost packets, delayed packets, node failures and link failures.
- [ ] The bit-pipe abstraction and the responsibilities of end hosts.

### Architecture

- [ ] Abstraction, layering, modularity and multiple protocols at one layer.
- [ ] Protocols: service interface versus peer interface.
- [ ] Protocol specification versus implementation/module.
- [ ] Protocol graphs and dependencies; trace the example protocol graph.
- [ ] Encapsulation and decapsulation; headers, payloads and trailers.
- [ ] Multiplexing/demultiplexing keys in protocol headers.
- [ ] OSI's seven layers and the purpose of each layer.
- [ ] Internet/TCP-IP architecture and its layers.
- [ ] OSI versus Internet architecture; IP's central role and the hourglass model.
- [ ] Internet architecture features and the role of IETF standards.

## 3. Network software and performance

**Sources:** Ambika `cn02`, pp. 1-68; Sanjeet `cn01`, pp. 137-204.

### Sockets and application communication

- [ ] Network API and the Berkeley/UNIX socket interface.
- [ ] Programs versus processes; client and server processes.
- [ ] Client-server versus peer-to-peer communication.
- [ ] Host identification with IP addresses; process/service identification with ports.
- [ ] Well-known ports versus temporary client ports; identify a communication flow using addresses, ports and transport protocol.
- [ ] Socket creation: `socket(domain,type,protocol)`, protocol families, `SOCK_STREAM` and `SOCK_DGRAM`.
- [ ] Client sequence: create socket, determine server address, `connect`, send/receive and `close`.
- [ ] Server sequence: `socket`, `bind`, `listen`, `accept`, send/receive and `close`.
- [ ] Active versus passive open; blocking operations and listen backlog.
- [ ] Listening socket versus the new connected socket returned by `accept`.
- [ ] Meaning of `send`, `recv`, `read`, `write` and their return values.
- [ ] Name/service lookup examples: `gethostbyname` and `getservbyname`.
- [ ] Concurrent service using processes/threads or nonblocking I/O.
- [ ] Little endian versus big endian; network byte order.
- [ ] `htons`, `htonl`, `ntohs` and `ntohl`.

### Protocol implementation

- [ ] Interaction between adjacent protocol layers.
- [ ] Process-per-protocol versus process-per-message.
- [ ] Context switches versus procedure calls and their overhead.
- [ ] Application buffers versus network buffers; why copying costs time.
- [ ] Shared message abstractions, buffer lists and manipulation without copying.
- [ ] Adding/removing headers, fragmentation and reassembly in message buffers.

### Performance and numericals

- [ ] Bandwidth, latency, RTT, throughput and jitter.
- [ ] Propagation delay, transmission delay and queuing delay.
- [ ] Latency-bound versus bandwidth-bound applications.
- [ ] Delay-bandwidth product and the pipe analogy.
- [ ] Required in-flight data/window to keep a link busy.
- [ ] File transfer time and throughput calculations.
- [ ] Correct conversions between bytes/bits, Mbps/Gbps and ms/us.

Useful formulas from this part:

| Quantity | Formula / interpretation |
| --- | --- |
| Transmission delay | Packet size in bits / link rate in bits per second |
| Propagation delay | Distance / propagation speed |
| Latency in the slides' model | Propagation + transmission + queuing |
| Delay-bandwidth product | Bandwidth × chosen delay; state whether the delay is one-way or RTT |
| Window needed for continuous sending | Approximately bandwidth × RTT, expressed in consistent units |
| Transfer time in the slides' simplified model | RTT + transfer size / bandwidth |
| Throughput | Transfer size / transfer time |

## 4. Direct-link networks and reliable transmission

**Sources:** Ambika `cn03`, pp. 1-87; Sanjeet `cn02`, pp. 1-79.

### Hardware, links and encoding

- [ ] Host/network-adaptor architecture and control/status registers (CSR).
- [ ] Link media, electromagnetic signals, frequency and wavelength.
- [ ] Encoding versus modulation.
- [ ] Shannon-Hartley capacity: `C=B log2(1+S/N)`; convert `SNR_dB=10 log10(S/N)` before substitution. This is explicitly in Ambika's deck, p. 8.
- [ ] NRZ encoding and its baseline-wander/clock-recovery problems.
- [ ] NRZI encoding: operation and limitations.
- [ ] Manchester encoding: combining clock and data; transition-rate overhead.
- [ ] 4B/5B encoding: mapping, redundancy, restrictions on consecutive zeros and unused codewords.
- [ ] Draw and compare encoding waveforms for an input bit string.

### Framing

- [ ] Why frames need boundaries; bits between adaptors versus frames between hosts.
- [ ] Byte-oriented protocols: sentinel/escape approach and byte counting.
- [ ] BISYNC: SYN, SOH, STX, ETX and DLE.
- [ ] PPP frame format, flag, protocol field, payload and checksum.
- [ ] DDCMP frame format and corruption of the count field.
- [ ] HDLC framing and the `01111110` flag.
- [ ] Bit stuffing after five consecutive ones; receiver destuffing and error cases.
- [ ] Clock-based framing with SONET: STS-1 structure, overhead, synchronization and STS-N multiplexing. This section is in Ambika's deck, pp. 35-38.

### Error detection

- [ ] Error detection versus error correction and retransmission.
- [ ] Redundant bits and detection overhead.
- [ ] One-dimensional parity, odd/even parity, VRC and LRC; VRC/LRC are explicitly named in Sanjeet's p. 34.
- [ ] Two-dimensional parity: row/column calculation and detectable/undetectable error patterns.
- [ ] Internet checksum: 16-bit words, one's-complement addition, end-around carry and complementing the sum.
- [ ] Checksum strengths, computational cost and undetected-error examples.
- [ ] CRC: bit strings as polynomials, generator polynomial and modulo-2/XOR division.
- [ ] CRC sender calculation and receiver verification; remainder interpretation.
- [ ] Generator properties and detection of single-bit, multiple-bit, odd-bit and burst errors.
- [ ] Recognize the standard CRC generator examples listed in the slides.

### Reliable transmission

- [ ] ACKs, timeouts and automatic repeat request (ARQ).
- [ ] Stop-and-wait: normal exchange, frame loss, ACK loss and timeout/retransmission timelines.
- [ ] Duplicate detection using a one-bit sequence number.
- [ ] Stop-and-wait performance limits and link-utilization calculations.
- [ ] Sliding window: multiple outstanding frames and pipelining.
- [ ] Sender variables SWS, LAR and LFS; invariant `LFS-LAR <= SWS`.
- [ ] Receiver variables RWS, LFR and LAF; acceptable-frame interval.
- [ ] Cumulative ACKs and buffering of out-of-order frames; trace the slides' frame 6/7/8 example.
- [ ] NAKs, duplicate/additional ACKs and selective acknowledgments.
- [ ] Selecting sender/receiver window sizes using the delay-bandwidth product.
- [ ] Finite sequence numbers, wraparound and distinguishing old frames from new frames.
- [ ] Sequence-space requirements when `RWS=1` and when `RWS=SWS`.
- [ ] Three roles of sliding windows: reliability, in-order delivery and flow control.

## 5. Ethernet, token rings and wireless

### Ethernet / IEEE 802.3

**Sources:** Ambika `cn03`, pp. 88-116; Sanjeet `cn02`, pp. 80-108.

- [ ] Shared Ethernet, ALOHA background and CSMA/CD.
- [ ] Ethernet segments, transceivers, adaptors, repeaters and hubs.
- [ ] Coaxial Ethernet, 10Base2 and 10BaseT examples in the slides.
- [ ] Ethernet frame format and the role of each field.
- [ ] 48-bit MAC addresses; unicast, broadcast and multicast reception.
- [ ] Address allocation to manufacturers and adaptor filtering.
- [ ] Transmitter algorithm: idle/busy medium, collision detection, jam and retransmission.
- [ ] Worst-case collision timeline: why a sender must still be transmitting when a collision returns.
- [ ] Minimum 512-bit frame, propagation time, slot time and the classical Ethernet length limits used in the slides.
- [ ] Binary exponential backoff and its random waiting range.
- [ ] Performance under light versus heavy load.

### Token rings / IEEE 802.5 and FDDI

**Source:** Ambika `cn03`, pp. 117-141. This detailed section is absent from Sanjeet's supplied direct-link deck.

- [ ] Ring topology, upstream/downstream forwarding and token circulation.
- [ ] Capturing a token, sending data, destination copying, sender removal and token reinsertion.
- [ ] Round-robin access and token holding time (THT).
- [ ] Token rotation time (TRT) and `TRT <= active nodes × THT + ring latency`.
- [ ] Link/node failure; bypass relays and multistation access units (MSAU).
- [ ] IEEE 802.5 characteristics, differential Manchester encoding and token/frame structure.
- [ ] Token priority, reservation and monitor fields.
- [ ] A and C status bits and their use for delivery feedback.
- [ ] Early versus delayed token release; fairness and utilization.
- [ ] Monitor election, missing tokens, orphaned/corrupted frames and beaconing.
- [ ] FDDI dual rings, single/dual attachment, physical limits and 4B/5B encoding; CDDI mention.

### Wireless / IEEE 802.11

**Sources:** Ambika `cn03`, pp. 142-177; Sanjeet `cn02`, pp. 109-140.

- [ ] Wireless media, licensed/unlicensed spectrum and operating restrictions.
- [ ] Spread spectrum: frequency hopping versus direct sequence; chipping sequence example.
- [ ] Wireless technology comparisons in the slides: range, bandwidth and mobility.
- [ ] Base-station networks versus ad-hoc/mesh networks.
- [ ] Wi-Fi / IEEE 802.11 physical-layer overview.
- [ ] Hidden-node and exposed-node problems; explain each with a diagram.
- [ ] Collision avoidance using MACA, RTS and CTS; why nodes defer.
- [ ] MACAW's ACK addition and retransmission/backoff.
- [ ] Distribution systems, access points, association and movement between cells.
- [ ] Active scanning with probe/response and passive scanning with beacons.
- [ ] 802.11 frame format, four address fields and ToDS/FromDS interpretation.
- [ ] Bluetooth: personal-area use, short range, low power, protocol profiles and piconet organization.
- [ ] Bluetooth master/slave communication, up to seven active slaves and parked devices; piconet diagram.
- [ ] ZigBee / IEEE 802.15.4 overview: low bandwidth, very low power, long battery life and inexpensive control/sensor devices.

The detailed Bluetooth/ZigBee ending is in Ambika's deck, pp. 174-177; Sanjeet's deck ends after 802.11 and its summary.

## 6. Packet switching, bridges and STP

**Sources:** Sanjeet `cn03`, pp. 3-61; Ambika's separate `Spanning Tree Protocol.pdf`.

### Switching and forwarding

- [ ] Switch operation, interconnected star topologies and aggregate switching capacity.
- [ ] Datagram/connectionless forwarding and forwarding-table lookup.
- [ ] Independent routes, delivery uncertainty and handling of failures.
- [ ] Virtual-circuit switching: setup, data transfer and teardown.
- [ ] VC table fields: incoming interface/VCI and outgoing interface/VCI.
- [ ] VCI rewriting and why a VCI is locally significant.
- [ ] Permanent versus switched virtual circuits (PVC/SVC).
- [ ] Setup signalling and the returning acknowledgment; trace VCI values across switches.
- [ ] Resource reservation, admission and flow control in the X.25 example.
- [ ] Datagram versus VC: setup delay, header overhead, state, failures and QoS.
- [ ] Source routing and rotation/stripping/pointer approaches to its header.

### Bridges and spanning tree

- [ ] Repeater versus bridge; extended LANs.
- [ ] Learning bridge: learn source address/port entries and age them out.
- [ ] Known-destination forwarding/filtering versus unknown-destination flooding.
- [ ] Why loops cause repeated frames and why a spanning tree is needed.
- [ ] Root bridge election using bridge IDs.
- [ ] Configuration BPDUs: root ID, path cost and sender ID.
- [ ] Initialization: each bridge initially assumes itself to be root.
- [ ] Compare candidate paths/BPDUs by root ID, total root path cost and tie-breakers; include sender/port IDs from the separate notes.
- [ ] Root ports, designated ports and blocked/non-designated ports.
- [ ] Trace BPDU exchanges, updates and the final forwarding tree for the supplied examples.
- [ ] Periodic BPDUs, failure detection and reconvergence.
- [ ] Broadcast/multicast forwarding on an extended LAN and limitations of bridges.

## 7. Internetworking, IP addressing and routing

**Sources:** Ambika `cn05`, pp. 3-60; Sanjeet `cn04`, pp. 3-60. Also complete Ambika's separate practice sheet.

### IPv4, fragmentation and forwarding

- [ ] Internetworks and IP's role over heterogeneous underlying networks.
- [ ] IP service model: connectionless, best-effort delivery and global addressing.
- [ ] IPv4 header format and the role of each field.
- [ ] MTU, fragmentation and destination reassembly.
- [ ] Identification, flags, fragment offset and total length.
- [ ] Compute fragment payloads, total sizes, offsets and MF values, including fragmentation again on a smaller-MTU network.
- [ ] Global addresses and network/host hierarchy; classful address examples.
- [ ] Direct delivery, next-hop forwarding and default routes.
- [ ] Trace the IP datagram forwarding algorithm.

### Subnetting and CIDR

- [ ] Subnet number, subnet mask and bitwise AND matching.
- [ ] Prefix length, network address, host range and broadcast address.
- [ ] Number of subnets and hosts per subnet; select a mask for a required number of departments/hosts.
- [ ] Classful address-allocation limitations and address-space exhaustion.
- [ ] Classless Inter-Domain Routing (CIDR), prefix blocks and route aggregation.
- [ ] Aggregating contiguous network blocks with a common prefix.
- [ ] Longest prefix matching when forwarding-table entries overlap.
- [ ] Identify the correct interface/next hop for each destination in a table.

### Supporting protocols

- [ ] ARP: **Address Resolution Protocol**, IP-to-link-address mapping, broadcast request, reply and cache.
- [ ] ARP packet fields and cache maintenance. Some slides call it “Address Translation Protocol”; learn the standard expansion above.
- [ ] Host configuration and DHCP; server, allocation and relay-agent operation shown in the slides.
- [ ] DHCP bootstrap exchange and why broadcasts/relays are needed.
- [ ] ICMP error reports: unreachable destination, failed reassembly, expired TTL and IP-header checksum failure; redirects with better-route information.

### Routing

- [ ] Forwarding versus routing; forwarding tables versus routing tables.
- [ ] Network as a weighted graph and shortest-path routes.
- [ ] Distance-vector routing: initial tables, neighbor exchanges, iterative updates and convergence.
- [ ] Bellman-Ford principle; compute next hops/costs from neighbors' distance vectors.
- [ ] Link-failure updates, routing loops and the count-to-infinity problem.
- [ ] Finite infinity, split horizon and poison reverse; limitations of the remedies.
- [ ] RIP example and distance-vector operation.
- [ ] Link-state routing: neighbors, link costs, link-state packets and reliable flooding.
- [ ] Sequence numbers, aging and propagation of link-state information.
- [ ] Dijkstra's algorithm: work through the supplied graph and build the routing table.
- [ ] Distance-vector versus link-state comparison.
- [ ] OSPF overview, header and link-state advertisement format.

### IPv6

- [ ] Why IPv6; 128-bit addresses and classless addressing.
- [ ] Address notation and the address types/examples shown in the slides.
- [ ] 40-byte base header, next-header field and extension-header concept.
- [ ] IPv4 versus IPv6 header/features comparison.

### Multicast and Mobile IP

**Source:** Ambika `cn05`, pp. 61-79. These sections are absent from Sanjeet's supplied `cn04`.

- [ ] One-to-many/many-to-many multicast and bandwidth savings over repeated unicasts.
- [ ] Multicast groups, group addresses and dynamic group membership.
- [ ] Any-source multicast (ASM) versus source-specific multicast (SSM).
- [ ] IGMP in IPv4 and Multicast Listener Discovery (MLD) in IPv6.
- [ ] Multicast forwarding tables and distribution trees.
- [ ] Distance-vector multicast, reverse-path checks and reverse-path broadcast (RPB).
- [ ] Pruning branches without interested group members.
- [ ] Protocol Independent Multicast (PIM): shared tree, source-specific tree and rendezvous point.
- [ ] Inter-domain multicast/MSDP overview at the depth supplied.
- [ ] Mobile IP: home address, home agent, foreign agent and care-of address.
- [ ] Proxy ARP, IP tunnelling and delivery to a mobile node.
- [ ] Triangle routing and route optimization.
- [ ] Binding updates, binding cache and binding warnings.

## 8. End-to-end protocols: UDP, TCP and RPC

**Sources:** Ambika `cn06`; Sanjeet `cn05`. Page/slide numbering diverges after the TCP connection diagram, so use the section titles too.

### UDP and transport requirements

- [ ] End-to-end services versus the underlying network's loss, duplication, reordering, size and delay limitations.
- [ ] Process-to-process delivery, multiplexing/demultiplexing and ports.
- [ ] UDP service, header format and message queues.
- [ ] UDP length/checksum fields; note the field-order correction explicitly mentioned in the slides.
- [ ] UDP versus TCP.

### TCP operation and flow control

- [ ] Reliable, connection-oriented byte-stream service.
- [ ] End-to-end issues: varying RTTs, reordering, receiver resources and network capacity.
- [ ] Bytes, segments, send buffers and receive buffers.
- [ ] TCP header: ports, sequence number, ACK number, advertised window, flags, checksum and urgent pointer.
- [ ] SYN, FIN, ACK, RST, PSH and URG purposes.
- [ ] Three-way handshake, connection establishment/termination diagrams and sequence-number exchanges.
- [ ] TCP checksum and pseudoheader concept.
- [ ] Sliding-window reliability, ordering and receiver flow control.
- [ ] LastByteAcked, LastByteSent, LastByteWritten, LastByteRead, NextByteExpected and LastByteRcvd.
- [ ] AdvertisedWindow, EffectiveWindow and send/receive buffer constraints.
- [ ] Blocking the writing application when the send buffer is full.
- [ ] Sequence-number wraparound, maximum segment lifetime and the 32-bit sequence space.
- [ ] Required window to keep the pipe full; limits of the basic 16-bit advertised-window field.
- [ ] Transmission triggers: MSS, push and timer.
- [ ] MSS versus MTU and protocol-header overhead.
- [ ] Silly window syndrome and the problem with repeated tiny segments.
- [ ] Nagle's algorithm and its ACK-based self-clocking rule.

### Adaptive retransmission

- [ ] SampleRTT, smoothed EstimatedRTT and the original timeout rule.
- [ ] Retransmission ambiguity: which transmission did an ACK acknowledge?
- [ ] Karn/Partridge: avoid ambiguous RTT samples and double timeout after retransmission.
- [ ] Why RTT variance matters; premature timeouts can worsen congestion.
- [ ] Jacobson/Karels: update estimate/deviation and calculate timeout.
- [ ] Solve numerical updates using the constants given in the question; some mathematical symbols in Ambika's slide 46 are poorly rendered.

### RPC

**Source:** Ambika `cn06`, slides 47-61. This detailed section is absent from Sanjeet's `cn05`.

- [ ] RPC request/reply model and the RPC stack diagrams.
- [ ] Three components: BLAST, CHAN and SELECT.
- [ ] BLAST: large-message fragmentation/reassembly and selective retransmission.
- [ ] Partial acknowledgments/selective retransmission requests (SRR).
- [ ] Sender DONE timer; receiver LAST_FRAG/RETRY timers and give-up conditions.
- [ ] BLAST header: MID, type, NumFrags and FragMask; wraparound protection.
- [ ] CHAN: synchronization, request/reply delivery and at-most-once semantics.
- [ ] Explicit/implicit ACKs; lost requests, replies and ACKs.
- [ ] Slow-server probes/keepalive notices, multiple outstanding calls and crash/reboot handling.
- [ ] CHAN's message ID, channel ID and boot ID; header and session-state fields.
- [ ] SELECT dispatcher; flat versus hierarchical procedure addressing.

## 9. Congestion control, resource allocation and QoS

### TCP congestion control: common to both sets

**Sources:** Ambika `congestion_control`, slides 1-26; Sanjeet `cn06`, pp. 34-58.

- [ ] Flow control versus congestion control.
- [ ] Congestion collapse and why retransmitting too aggressively makes it worse.
- [ ] ACK clocking/self-clocking and estimating usable network capacity.
- [ ] CongestionWindow versus AdvertisedWindow.
- [ ] `MaxWindow=min(CongestionWindow,AdvertisedWindow)`.
- [ ] `EffectiveWindow=MaxWindow-(LastByteSent-LastByteAcked)`.
- [ ] Additive increase/multiplicative decrease (AIMD).
- [ ] Add approximately one MSS per RTT; per-ACK increment `MSS × MSS / CongestionWindow`.
- [ ] Slow start: exponential growth, roughly doubling each RTT in the slides' model.
- [ ] CongestionThreshold/slow-start threshold and transition to additive increase.
- [ ] Timeout response: distinguish halving the target/threshold from restarting the actual window at one MSS in the slides' slow-start model.
- [ ] Duplicate ACKs and fast retransmit after three duplicate ACKs.
- [ ] Fast recovery versus waiting for timeout and restarting with slow start.
- [ ] Interpret congestion-window/time graphs and calculate window evolution under stated assumptions.

### Resource allocation and queueing: Sanjeet's additional coverage

**Source:** Sanjeet `cn06`, pp. 2-33.

- [ ] Resources: link bandwidth and router/switch buffers; bottlenecks and queue overflow.
- [ ] Resource allocation versus congestion control; host and router responsibilities.
- [ ] Connectionless flows, flow granularity and soft state versus hard state.
- [ ] Router-centric versus host-centric designs.
- [ ] Reservation-based versus feedback-based control; explicit versus implicit feedback.
- [ ] Window-based versus rate-based control.
- [ ] Throughput-delay trade-off, fairness and `Power=Throughput/Delay`.
- [ ] FIFO/FCFS scheduling versus tail-drop policy; why these are separate choices.
- [ ] Priority queues and per-priority FIFO service.
- [ ] Fair queuing: per-flow queues and the problem with packet-by-packet round robin when lengths differ.
- [ ] Simulating bit-by-bit round robin with finish timestamps.
- [ ] Calculate `Fi=max(Fi-1,Ai)+Pi` in the slides' normalized model and select the lowest finishing timestamp.
- [ ] Non-preemption of a packet whose transmission has already started.

### Congestion avoidance: Sanjeet's additional coverage

**Source:** Sanjeet `cn06`, pp. 59-79.

- [ ] Congestion avoidance versus reacting after loss.
- [ ] DECbit: average queue length, congestion marking, ACK feedback and sender response.
- [ ] DECbit rules: fewer than 50% marked -> increase by one packet; at least 50% -> multiply window by 0.875.
- [ ] Random Early Detection (RED): early random drops and implicit feedback to TCP.
- [ ] Weighted average queue length: `AvgLen=(1-Weight)×AvgLen+Weight×SampleLen`.
- [ ] MinThreshold/MaxThreshold regions and RED's drop-probability graph.
- [ ] `TempP=MaxP×(AvgLen-MinThreshold)/(MaxThreshold-MinThreshold)` and `P=TempP/(1-count×TempP)`.
- [ ] RED versus DECbit and versus waiting for a full buffer.
- [ ] Source-based avoidance using RTT growth.
- [ ] The two source-based algorithms shown: RTT midpoint comparison, and the product of window change and RTT change.

### Quality of Service: Sanjeet's additional coverage

**Source:** Sanjeet `cn06`, pp. 80-121.

- [ ] Why bandwidth alone is insufficient for real-time audio/video/control.
- [ ] Timeliness, playback points, jitter/playback buffering and late-packet loss.
- [ ] Tolerant versus intolerant applications.
- [ ] Adaptive versus non-adaptive applications; delay-adaptive and rate-adaptive examples.
- [ ] Fine-grained/per-flow QoS versus coarse-grained/class-based QoS.
- [ ] Integrated Services (IntServ): guaranteed service and controlled-load service.
- [ ] Flowspec, TSpec and RSpec.
- [ ] Admission control, resource reservation, packet classification and scheduling.
- [ ] Token bucket: token rate `r`, bucket depth `B`, allowable bursts and long-term rate.
- [ ] Work through the steady-flow and bursty-flow examples; calculate token accumulation and required bucket depth.
- [ ] RSVP: soft state and support for unicast/multicast reservations.
- [ ] PATH message from sender toward receiver; RESV message back toward sender.
- [ ] TSpec/RSpec propagation, router admission decisions, reservation errors and periodic refresh.
- [ ] Differentiated Services (DiffServ): traffic classes and edge marking.
- [ ] Per-hop behaviors (PHBs); why a PHB describes router behavior.
- [ ] Expedited Forwarding (EF): low delay/loss with controlled admitted rate.
- [ ] Assured Forwarding (AF), RED with In and Out (RIO)/Weighted RED and different drop curves.
- [ ] IntServ versus DiffServ comparison.

## 10. What differs between the professors' supplied sets?

These are differences in the supplied files, not confirmed exam exclusions.

| Coverage | Where to study it |
| --- | --- |
| Network evolution and explicit topology list | Sanjeet `cn01`, pp. 2-7 and 31 |
| Shannon-Hartley, media/frequency detail and SONET | Ambika `cn03`, pp. 8-13 and 35-38 |
| Explicit VRC/LRC heading | Sanjeet `cn02`, p. 34 |
| Detailed token ring and FDDI | Ambika `cn03`, pp. 117-141 |
| Detailed Bluetooth/piconet and ZigBee overview | Ambika `cn03`, pp. 174-177 |
| Full packet-switching and learning-bridge lecture | Sanjeet `cn03`; no corresponding standalone packet-switching deck exists in Ambika's supplied folder |
| STP step-by-step supplement and port tie-breakers | Ambika's separate STP PDF; combine with Sanjeet `cn03` |
| Internet multicast and Mobile IP | Ambika `cn05`, pp. 61-79 |
| RPC, BLAST, CHAN and SELECT | Ambika `cn06`, slides 47-61 |
| Focused TCP congestion-control revision | Ambika `congestion_control` |
| Resource allocation, fair queuing, DECbit, RED and QoS | Sanjeet `cn06` |
| Explicit internetworking problem sheet | Ambika's separate 2-page practice PDF |

## 11. Numerical and diagram practice checklist

This list identifies practice supported by the material; it is not a prediction of marks or question frequency.

### Numericals / algorithm traces

- [ ] Delay, transmission time, RTT, throughput and delay-bandwidth product.
- [ ] Shannon capacity and SNR conversion.
- [ ] Encoding waveforms and HDLC bit stuffing/destuffing.
- [ ] One-/two-dimensional parity, one's-complement checksum and CRC division.
- [ ] Stop-and-wait throughput and sliding-window/sequence-space calculations.
- [ ] Ethernet collision timing, minimum frame size and backoff choices.
- [ ] Token holding/rotation time.
- [ ] Datagram lookup and virtual-circuit table/VCI trace.
- [ ] Learning-bridge table updates and STP root/port selection.
- [ ] Subnet masks, host/subnet counts, CIDR aggregation and longest prefix matching.
- [ ] IP fragmentation/refragmentation, offsets and MF flags.
- [ ] Distance-vector iterations and Dijkstra shortest paths.
- [ ] TCP byte sequence/ACK numbers, advertised/effective windows, MSS and sequence wraparound.
- [ ] RTT estimation, timeout/backoff and Jacobson/Karels updates.
- [ ] Congestion-window growth, threshold changes and loss recovery.
- [ ] Fair-queue finish times, RED probability and token-bucket calculations.

### Diagrams / formats to reproduce

- [ ] OSI/TCP-IP stacks, protocol graphs and encapsulation.
- [ ] Client/server socket sequence and the two process models.
- [ ] NRZ, NRZI, Manchester and 4B/5B examples.
- [ ] PPP/HDLC/SONET, Ethernet, token-ring and 802.11 formats.
- [ ] Stop-and-wait/sliding-window timelines; hidden/exposed nodes and RTS/CTS.
- [ ] VC setup, learning bridges and spanning-tree examples.
- [ ] IPv4, ARP and IPv6 headers; fragmentation and forwarding tables.
- [ ] Multicast trees and Mobile IP tunnelling/triangle routing.
- [ ] UDP/TCP headers, TCP handshake and send/receive buffers.
- [ ] RPC stack, BLAST and CHAN exchanges.
- [ ] TCP congestion-window graphs, FIFO/FQ, DECbit and RED graphs.
- [ ] Playback buffer, token bucket, RSVP PATH/RESV and DiffServ drop curves.

## 12. Complete the supplied internetworking practice sheet

**Source:** `ambika_slides/Internetworking - practice questions.pdf`.

1. Class B network with a 6-bit subnet number: maximum subnets and hosts per subnet.
2. Class B network split for 64 departments: choose the subnet mask.
3. Overlapping forwarding-table entries: select interfaces for `128.75.43.16` and `192.12.17.10`.
4. Explain why IPv4 reassembly occurs at the destination rather than intermediate routers.
5. Fragment a TCP message with 1,024 data bytes and a 20-byte TCP header across MTUs of 1,024 and 576 bytes, with 20-byte IP headers; determine final sizes and offsets.
6. Apply longest prefix matching to the five listed `128.96.x.x` destinations using the supplied table.

For subnet-count questions, state whether all subnet numbers are usable or an older convention excludes the all-zero/all-one subnets; use the convention specified by the question/professor.

## 13. Scope gaps and outline-only topics

- **Ambika's file numbering skips `cn04`.** No corresponding file was supplied. Sanjeet's packet-switching deck supplies detailed switching/bridging coverage; do not infer that the missing filename means the topic is excluded.
- **Cell switching/ATM appears in Sanjeet's packet-switching outline**, and ATM/Frame Relay are named as VC examples. The supplied 62-page deck does not contain a separate detailed ATM/cell-switching section.
- **Presentation formatting, compression, cryptography/security and network management appear in broad course-content lists**, but dedicated teaching sections on them are not present in these two supplied folders.
- **Application protocols mentioned as examples are not complete application-layer lectures.** Do not infer full DNS, HTTP, FTP or email chapters from example names alone.
- **RPR is named in Ambika's ring-section heading**, but the detailed ring material supplied focuses on IEEE 802.5 and FDDI.
- Course administration, attendance, evaluation rules, reference lists and thank-you slides are not study topics.
- No topic has been dropped merely because it was likely taught before midsem. A confirmed endsem-only cutoff would be needed to narrow this checklist.
