# OS Portions — CS3000

Based on sir's material in `MID_SEM_NOTES/` and `postmid/`, including the syllabus embedded as images in `Firstclass.pptx`.

**How to use this file:** the folder names identify when material was shared, not a confirmed examination cutoff. Synchronization and deadlocks occur in both folders. No separate endsem exclusion notice was found in these folders; do not assume that pre-midsem material is excluded.

## At a glance

| Area | Material supplied | What to prepare |
| --- | --- | --- |
| OS introduction, kernels, hardware and booting | Midsem | Concepts, comparisons, boot sequence |
| Processes and system calls | Midsem; additional processes deck in project root | PCB, states, fork/exec/wait/exit, output tracing, xv6 |
| IPC | Midsem; repeated in postmid | Pipes, POSIX and System V shared memory, signals |
| CPU scheduling | Midsem | Algorithms, Gantt charts, numerical problems, Linux scheduling |
| Threads and multithreading | Official syllabus | Pthreads, models, management, cancellation, thread pools, scheduling |
| Synchronization | Both folders | Critical sections, Peterson, Bakery, locks, semaphores, classical problems |
| Deadlocks and Banker's algorithm | Both; expanded postmid practice | RAG, prevention/avoidance/detection/recovery, safety and requests |
| Memory management and virtual memory | Postmid | Allocation, paging, TLB, multilevel tables, replacement, segmentation, xv6 |
| Disk scheduling | Postmid | HDD structure, timing, six algorithms and head movement |
| File systems, RTOS and FreeRTOS | Official syllabus | Listed below; no dedicated teaching notes found in the two folders |

## 1. Pre-midsem material

### 1.1 OS fundamentals and kernel architectures

- [ ] Need for an OS; hardware abstraction and resource management.
- [ ] OS functions and services: CPU, memory, storage, devices, protection and isolation.
- [ ] Multiprogramming versus time sharing/multitasking; concurrency versus parallel execution.
- [ ] Multiprocessors, multicore processors and hardware threads.
- [ ] User mode versus kernel mode; privileges and controlled system-call entry.
- [ ] Kernel versus complete operating system/distribution.
- [ ] Monolithic, microkernel, hybrid and exokernel designs: structure and trade-offs.
- [ ] Windows/NT, Linux, Ubuntu and macOS/XNU: kernel type, platform distinctions and uses.
- [ ] Basic protection/security ideas: virtual-memory permissions, access control and authentication.

**Sources:** `week1_Intro/w1_1_Introduction.ppt`, `w1_lecture1.ppt`, `2_Overview.ppt`, `w1_lecture4.ppt`, `Operating_Systems_Kernels_and_Platforms.pptx`.

### 1.2 Hardware, addressing and booting

- [ ] Memory addresses, port-mapped I/O and memory-mapped I/O; load/store versus in/out.
- [ ] PC memory map; conventional/low and extended memory; device/BIOS address regions.
- [ ] CPU registers and x86 evolution: 8088, 80386 and x86-64; address width and addressable memory.
- [ ] Real-mode address calculation: `(segment << 4) + offset`.
- [ ] Boot sequence: reset → BIOS/POST → boot device/MBR → bootloader → kernel → first user process.
- [ ] MBR layout, boot sector at `0x7c00`, and xv6 kernel loading at `0x100000` in these x86 notes.
- [ ] Real mode versus protected mode; A20, GDT and interrupt setup during boot.
- [ ] xv6 `bootasm.S`, `bootmain.c` and kernel entry.
- [ ] SMP boot: BSP/AP roles, MP table, APIC/startup IPI, `mpinit` and `startothers`.

**Sources:** `week1_Intro/3_Hardware.ppt`, `w1_lecture2.ppt`.

### 1.3 Processes and system calls

- [ ] Program versus process; text, data, heap and stack; virtual address space.
- [ ] PCB: PID/PPID, state, registers/program counter, scheduling, memory and open-file information.
- [ ] Process lifecycle and state transitions: new, ready/runnable, running, blocked/waiting and terminated.
- [ ] System-call mechanism: library wrapper → argument/syscall-number setup → trap → kernel dispatch → return.
- [ ] System call versus API versus library function; parameter passing through registers, blocks and stack.
- [ ] Six categories: process control, file management, device management, information, communication and protection.
- [ ] `fork`: return values, parent/child identities, inherited resources and separate variable copies.
- [ ] Copy-on-write; shared open-file descriptions/file offsets after fork.
- [ ] `exec`: replaces the current image, preserves PID, returns only on failure.
- [ ] `execl`, `execlp`, `execle`, `execv`, `execvp`, `execve`; meaning of l/v/p/e and NULL termination.
- [ ] `wait`, `waitpid`, `exit`, `_exit`; termination status, reaping, zombies and orphans.
- [ ] Shell pattern: fork → child exec → parent wait.
- [ ] Fork trees and output-count questions: sequential/nested forks, conditionals, loops, child `break`, successful/failed exec and independent variable updates.
- [ ] Output ordering and stdio buffering: buffered output present before fork may be duplicated unless flushed.
- [ ] File descriptors and `open`, `read`, `write`, `lseek`, `close`; introductory `strace` use.

**Sources:** all files in `MID_SEM_NOTES/Fork/`; process-state/PCB diagram in `Image.jpeg`.

**Additional supplied deck outside the folders:** `w2_processes1.ppt.pptx` has 122 slides covering process address spaces, user/kernel stacks, PCB/`ptable`, xv6 fork/exit/wait/exec, ELF headers, process context and timer-driven context switching. Include:

- [ ] `struct proc`, process states, `allocproc`, `copyuvm`, child trapframe return register and `RUNNABLE` transition.
- [ ] xv6 exit/wait cleanup, adoption of children and reclamation of zombie entries.
- [ ] ELF sections versus loadable segments, exec loading, argv/user stack and entry point.
- [ ] Trapframe versus saved context; timer interrupt → trap → yield → sched → swtch → scheduler.
- [ ] Direct and indirect context-switch overhead; time-quantum trade-off.
- [ ] Heap growth through `sys_sbrk` and `growproc` (exercise in the deck).

### 1.4 Inter-process communication

- [ ] Why IPC is needed; information sharing, modularity and cooperation.
- [ ] Shared memory versus message passing versus pipes: mechanism, copying overhead and synchronization.
- [ ] Pipes: `pipe(fd)`, `fd[0]` read end, `fd[1]` write end, descriptor inheritance after fork.
- [ ] Closing unused ends, blocking reads/writes, full/empty pipes, and EOF after every write-end reference closes.
- [ ] Parent–child communication, two pipes for two-way communication, tracing code that hangs because a writer remains open.
- [ ] Shell pipelines with `dup`/`dup2`, standard-input/output redirection and exec; `fdopen` to bridge descriptors to C streams.
- [ ] Unnamed pipes versus named FIFOs/`mkfifo`; `SIGPIPE` when writing after all read ends close.
- [ ] Signals: asynchronous notification, `kill` and handler registration; basic signal handling.
- [ ] POSIX shared-memory lifecycle: `shm_open → ftruncate → mmap(MAP_SHARED) → access → munmap/close → shm_unlink`.
- [ ] POSIX names, flags and permissions; descriptor versus mapped pointer; `MAP_SHARED` versus `MAP_PRIVATE`.
- [ ] Same shared object mapped at different virtual addresses; pointer/offset issues in shared structures.
- [ ] System V lifecycle: `shmget → shmat → access → shmdt → shmctl(IPC_RMID)`.
- [ ] Key versus shmid versus attached pointer; `ftok`, `IPC_CREAT`, `IPC_EXCL`, `SHM_RDONLY`, `IPC_STAT` and `IPC_SET`.
- [ ] Detaching/unmapping versus unlinking/removing; lifetime, startup order, cleanup and error checks.
- [ ] Writer/reader programs; adding semaphores to coordinate shared-memory producer–consumer.

**Sources:** all four files in `MID_SEM_NOTES/IPC/`; IPC slides 1–13 in both synchronization decks.

### 1.5 CPU scheduling

- [ ] CPU-bound versus I/O-bound processes; CPU/I/O bursts, ready queue and scheduler triggers.
- [ ] Goals: utilization, throughput, turnaround, waiting, response and fairness.
- [ ] Preemptive versus non-preemptive scheduling; tie-breaking and CPU idle intervals.
- [ ] FCFS and convoy effect.
- [ ] SJF and preemptive SRTF; burst prediction and starvation of long jobs.
- [ ] LJF, as introduced in the scheduling notes.
- [ ] Round Robin: ready-queue tracing, quantum, context-switch count and overhead.
- [ ] Priority scheduling in both modes; static/dynamic priorities, starvation and aging.
- [ ] Multilevel queues versus multilevel feedback queues; demotion, arrivals/preemption and gaming the scheduler.
- [ ] HRRN: choose maximum `(waiting + burst) / burst`.
- [ ] Gantt charts; completion, turnaround, waiting and first-response times; averages.
- [ ] Problems mixing CPU/I/O phases and overlapping I/O; CPU idle percentage.
- [ ] Multiprocessor scheduling: global/per-CPU/hybrid queues, contention, migration, hard/soft affinity and load balancing.
- [ ] Push versus pull migration.
- [ ] xv6 Round Robin policy.
- [ ] Linux scheduling **as presented historically in the notes**: O(n), O(1), active/expired priority queues, bitmap selection, nice values and timeslices.
- [ ] Classical CFS: ideal fairness, target latency, vruntime, priority weights, red-black tree and minimum-runtime selection.

**Source:** `MID_SEM_NOTES/8_Scheduling.ppt`. Additional revision: `process_scheduling_exam_summary.pdf` in the project root.

### 1.6 Linux command reference

- [ ] File navigation, creation/removal, copying/moving, links and viewing/searching files.
- [ ] Permissions/ownership and disk-space commands.
- [ ] `ps`, `top`, `pgrep`, `kill`, `jobs`, `bg`, `fg`, `nohup`, `nice` and `renice`.
- [ ] `pstree`, process hierarchy, `/proc/PID/status`, PID/PPID and process-state letters.
- [ ] Recognizing zombie versus orphan processes.

**Source:** `MID_SEM_NOTES/linux_commands_reference.pdf`.

## 2. Synchronization and deadlocks — present in BOTH folders

The midsem deck has 114 slides. The postmid deck has 191 slides, with extra explanations and numerical/practice questions. These are overlapping material, not two separate units.

### 2.1 Critical sections and software solutions

- [ ] Race conditions and lost updates; interleavings on one CPU and across cores.
- [ ] Critical-section requirements: mutual exclusion, progress and bounded waiting.
- [ ] Atomicity; why checking a lock and then setting it in separate steps fails.
- [ ] Disabling interrupts: privilege requirement and multicore limitations.
- [ ] Strict alternation/turn-variable approach and why it violates progress.
- [ ] Two-flag attempts: failure of mutual exclusion versus deadlock when both announce intent.
- [ ] Peterson's two-process solution: flags, turn/favored variable, tie-breaking and correctness.
- [ ] Lamport's Bakery algorithm: ticket selection, choosing array, lexicographic `(ticket, process ID)` order and ties.
- [ ] Simplified Bakery algorithm and its atomic-doorway assumption.
- [ ] Busy waiting/spinning versus blocking.

### 2.2 Hardware locks, mutexes and priorities

- [ ] Atomic test-and-set and `xchg`; acquire/release code and interleaving traces.
- [ ] Spinlocks: appropriate short critical sections, CPU cost, cache/bus traffic and improved test-then-test-and-set loops.
- [ ] Memory ordering/compiler concerns; xv6 spinlock references.
- [ ] Blocking mutexes, sleep/wakeup and wait queues.
- [ ] Thundering herd; waking one waiter rather than every waiter.
- [ ] Pthread spinlock/mutex operations and initialization/cleanup.
- [ ] Priority inversion: low-priority lock holder, high-priority waiter, medium-priority interference.
- [ ] Bounded versus unbounded inversion; priority inheritance and the priority-ceiling idea.

### 2.3 Semaphores and classical problems

- [ ] Binary versus counting semaphores; P/down/wait and V/up/signal; atomic operations.
- [ ] Counting resources, blocked waiters, semaphore-value calculations and possible concurrency.
- [ ] POSIX `sem_init`, `sem_wait`, `sem_post`, `sem_getvalue`, `sem_destroy`; meaning of initial value and process-sharing parameter.
- [ ] Producer–consumer/bounded buffer: overflow, underflow, race conditions and lost wakeups.
- [ ] Correct initialization: `empty=N`, `full=0`, `mutex=1`; correct order of waits/signals.
- [ ] Circular buffer indices and producer/consumer pthread implementation.
- [ ] Dining philosophers: deadlock, starvation, picking one fork first, retry/livelock issues, global-mutex limitation.
- [ ] State-based solution using THINKING/HUNGRY/EATING, neighbor tests, per-philosopher semaphores and a mutex.
- [ ] Semaphore code/output problems: feasible interleavings, ordering constraints, deadlock-free acquisition and min/max shared-variable values.

### 2.4 Deadlocks

- [ ] Deadlock versus starvation versus livelock.
- [ ] Four necessary conditions: mutual exclusion, hold-and-wait, no preemption and circular wait.
- [ ] Resource-allocation graphs: processes, resource instances, assignment edges and request edges.
- [ ] Single-instance graph: cycle implies deadlock; multiple-instance graph: cycle alone is insufficient.
- [ ] Handling strategies: ignorance/ostrich, prevention, avoidance, detection and recovery.
- [ ] Prevention by breaking a condition; disadvantages and resource utilization.
- [ ] Consistent/hierarchical resource ordering and semaphore acquisition order.
- [ ] Detection using a graph or Available/Allocation/current-Request vectors and matrices.
- [ ] Recovery: termination/victim selection, preemption and checkpoint/rollback.
- [ ] Safe versus unsafe versus already deadlocked; unsafe does not mean definitely deadlocked.

### 2.5 Banker's algorithm and supplied practice

- [ ] Available, Max, Allocation and `Need = Max − Allocation`.
- [ ] Total instances = Available + column sums of Allocation.
- [ ] Safety algorithm: Work/Finish, `Need[i] <= Work`, then `Work += Allocation[i]`.
- [ ] Identify initially eligible processes; produce safe sequences and Work traces.
- [ ] Enumerate all safe sequences when explicitly requested.
- [ ] Resource request: check Request ≤ Need and Request ≤ Available; tentatively update; run safety test; grant or roll back.
- [ ] Distinguish unavailable resources from available-but-unsafe allocation.
- [ ] Restore the original snapshot between independent requests.
- [ ] Skipping an ineligible process does not establish unsafety; try another unfinished process.
- [ ] Completing an eligible process never reduces Work; safety testing does not need backtracking among eligible choices.
- [ ] Complete Problem 1: four processes/three resources; independent P0/P1 requests and all safe sequences.
- [ ] Complete Problem 2: five processes/four resources; two starting choices, invalid proposed order and independent requests.

**Sources:** `MID_SEM_NOTES/9_Synchronization.pptx`; `postmid/Synchronization_Deadlock.pptx`; `postmid/Banker_Algorithm_Two_Problems (1).pdf`; `postmid/Bankers_Algorithm_Problems_1_and_2_Detailed_Solutions.docx`; `postmid/deadlock_classroom_simulation.html`.

## 3. Post-midsem additions: memory and storage

### 3.1 Contiguous memory allocation

- [ ] Purpose of memory management and sharing RAM between processes.
- [ ] Single contiguous allocation; fixed/static versus dynamic/variable partitioning.
- [ ] First Fit, Best Fit and Worst Fit; allocate a sequence of processes and update remaining holes.
- [ ] Internal versus external fragmentation; compaction, relocation and merging adjacent free holes.
- [ ] Base/relocation and limit registers: validate logical address before adding base.
- [ ] Constraints on process size and multiprogramming; why non-contiguous allocation is useful.

### 3.2 Paging and address numericals

- [ ] Pages versus frames; equal sizes; non-contiguous physical placement.
- [ ] Per-process page tables and PTBR; mapping page number to frame number.
- [ ] PTE fields: frame number, present/valid, protection, reference, cache-control and dirty bits.
- [ ] Logical address = page number + offset; physical address = frame number + unchanged offset.
- [ ] Calculate pages, frames, offset/page/frame bits, address-space size and page-table size.
- [ ] Byte-addressable versus word-addressable memory; unit conversions.
- [ ] Page-table storage overhead versus internal fragmentation; theoretical optimal page size.

### 3.3 TLB and multilevel paging

- [ ] TLB purpose, hit/miss paths, page-table lookup and effective memory access time.
- [ ] Effect of context switches on translations in the simplified model in the notes.
- [ ] Why large page tables need multiple levels; tables fit into pages; upper entries point to lower tables.
- [ ] Entries per table = page size / PTE size; index-bit split and required number of levels.
- [ ] Physical versus virtual address layouts; partially used outer tables.
- [ ] One/two/multiple-level memory-access counts, with and without a TLB hit.
- [ ] TLB reach, number of TLB entries and total TLB storage including page/frame numbers, process IDs and control bits (image-based practice question).
- [ ] Practice the supplied 46-bit/8-KB/4-byte-PTE, 48-bit/16-KB/4-byte-PTE and 64-bit/1-MB examples.

### 3.4 Virtual memory, demand paging and replacement

- [ ] Virtual address space and MMU translation; only needed pages resident in RAM.
- [ ] Demand paging, present bit, swap space and page faults.
- [ ] Page-fault sequence: validate → locate backing → obtain/victimize frame → write dirty victim if needed → load → update mapping → restart.
- [ ] TLB miss versus page fault; protection fault versus absent page.
- [ ] FIFO, LIFO, LRU, Optimal and Random page replacement; LFU is also named in the overview.
- [ ] Trace reference strings through initially empty frames; count hits/faults and compute ratios.
- [ ] Limited-lookahead variation of Optimal in the practice questions.
- [ ] Page-fault rate/service time and effective access time; ns/ms conversions.
- [ ] Belady's anomaly; stack property; why LRU and Optimal avoid the anomaly, and the FIFO counterexample.

### 3.5 Segmentation and xv6 memory implementation

- [ ] Logical modules and variable-size segments; segment number + offset.
- [ ] Segment table base/limit; valid offsets `0 ... limit−1`; physical address or trap.
- [ ] Segment-table size from number of segments and entry size.
- [ ] Paging versus segmentation: view, allocation, fragmentation, table structure and overhead.
- [ ] x86 logical → linear via segmentation → physical via paging.
- [ ] GDT, GDTR, segment descriptors, base/limit/access rights/DPL and segment selectors/registers.
- [ ] 32-bit two-level translation, page directory/table, CR3 and paging enable in CR0.
- [ ] xv6 kernel/user segments, kernel mappings, `KERNBASE`, `V2P`/`P2V` and memory-mapped I/O.
- [ ] `walkpgdir`, `mappages`, PDX/PTX/PTE_ADDR and page permissions/present bit.
- [ ] Physical-page allocation: `kalloc`, `kfree`, 4-KB pages and embedded freelist links.

**Source for 3.1–3.5:** `postmid/w1_4_memory_management (1).pptx` — 195 slides. Slides 132–133 introduce disk scheduling; slides 134–195 return to virtual memory, segmentation and xv6. Do not stop reading at slide 133.

### 3.6 HDD structure and disk scheduling

- [ ] HDD platters, surfaces, tracks, sectors, cylinders and read/write heads.
- [ ] Seek time, rotational latency, transfer rate/time, controller overhead and queueing delay.
- [ ] Scheduling objectives: reduce movement/seek, increase throughput, fairness and response time.
- [ ] FCFS, SSTF, SCAN, C-SCAN, LOOK and C-LOOK: selection rule, direction, endpoints, reversal and wraparound.
- [ ] Draw service order/head path; total head movement and average movement per request.
- [ ] Distinguish disk boundary from last pending request; state whether return jumps are counted.
- [ ] Compare starvation risk, waiting-time uniformity and unnecessary endpoint travel.
- [ ] HDD versus SSD relevance of seek-based scheduling.

**Sources:** `postmid/Disk Scheduling.pptx` (9 slides) and `postmid/Disk Scheduling in Operating Systems.pdf` (worked examples for all six algorithms).

## 4. Official-syllabus topics needing separate revision

These are explicitly listed in the syllabus image in `MID_SEM_NOTES/Firstclass.pptx`. Their presence in the syllabus does not establish that they were all taught or included in the endsem. Dedicated coverage was not found in the two supplied folders.

### 4.1 Threads and multithreaded programming

- [ ] Benefits, challenges and multithreading models; process versus thread.
- [ ] Pthreads: creation, arguments, joining, termination and shared/private state.
- [ ] Thread cancellation, thread-specific data and thread pools.
- [ ] Signal handling in the threading context.
- [ ] Thread scheduling and contention scope; pthread scheduling support.

### 4.2 File systems

- [ ] File operations.
- [ ] File access methods.
- [ ] Directory structure.
- [ ] Mounting file systems.

Basic file-descriptor calls appear in the system-call slides, but those do not replace the full file-system syllabus above.

### 4.3 RTOS and FreeRTOS

- [ ] Introduction to operating systems for handheld devices.
- [ ] Real-time operating systems.
- [ ] Introduction to FreeRTOS.

## 5. Numerical and code-tracing checklist

| Topic | Be able to do without looking at solutions |
| --- | --- |
| fork/exec | Draw the actual process tree; count processes/prints; follow branch termination and exec failure |
| CPU scheduling | Draw Gantt chart and compute CT, TAT, WT, RT, utilization and context switches |
| Semaphores | Trace P/V and blocked processes; reason about possible outputs/concurrency and deadlock |
| Banker's | Need/total vectors, safe sequence, Work trace, all sequences if asked, independent request tests |
| Allocation | Apply fit algorithms in order; update holes and fragmentation |
| Paging | Page/frame/offset, logical-to-physical address, PTE/table size and addressability |
| TLB/multilevel | EAT, number of levels, address-field split and access counts |
| Replacement | Frame-by-frame FIFO/LRU/Optimal, hits/faults, ratios and Belady examples |
| Segmentation | Check offset against limit, then compute base + offset or trap |
| Disk scheduling | Service order, direction/endpoints, wraparound and total/average head movement |

## 6. Compact formula sheet

Assume byte-addressable memory unless stated otherwise; use consistent units.

| Quantity | Formula / rule |
| --- | --- |
| Turnaround | `TAT = CT − AT` |
| Waiting, single CPU-burst problems | `WT = TAT − BT` |
| Response | `RT = first CPU start − AT` |
| HRRN | `(waiting + burst) / burst` |
| RR useful-time fraction in the simple repeated-slice model | `q / (q + context-switch time)` |
| Banker's Need | `Max − Allocation` |
| Total instances | `Available + sum of Allocation column` |
| Safety step | If `Need[i] <= Work`, simulate completion with `Work += Allocation[i]` |
| Page count for an actual process | `ceil(process bytes / page bytes)` |
| Frame count | `physical-memory bytes / frame bytes` |
| Offset bits | `log2(page size in addressable units)` |
| Page number / offset | `address // page_size`, `address % page_size` |
| Physical address | `frame_number × page_size + offset` |
| Full single-level page-table size | `number of virtual pages × PTE bytes` |
| Entries per page-table page | `page bytes / PTE bytes` |
| Minimum levels, uniform power-of-two tables | `ceil((virtual_bits − offset_bits) / log2(entries_per_table))` |
| Theoretical optimal page size | `sqrt(2 × process_size × PTE_size)` under the notes' half-page-waste model |
| TLB EAT, L levels, no faults | `h(c + m) + (1−h)(c + (L+1)m)`; c=TLB time, m=memory time |
| EAT with faults | Weight normal and fault paths by their probabilities; check whether service time already includes restart/access |
| Hit / fault ratio | `hits / references`, `faults / references` |
| Segment validity | `0 <= offset < limit`; then `PA = base + offset` |
| Disk head movement | Sum `abs(next_position − current_position)` including required endpoints/jumps |

## 7. Scope notes and reading inventory

- `MID_SEM_NOTES/` contains **21 teaching/support files**, one full textbook PDF, and one process-state/PCB image (23 files excluding `.DS_Store`). The six introductory `.ppt` files contain overlapping material; all six are accounted for above.
- `postmid/` contains **7 files**: three PPTX decks, two PDFs, one DOCX and one HTML simulation. All seven are represented above.
- `Firstclass.pptx` includes the formal CS3000 syllabus and CS3003 practice outline as images. The practice outline additionally names readers–writers, threaded min/max/sum/average applications, pipes/shared memory, scheduling APIs and deadlock algorithms. Treat this as lab context, not proof of extra theory-exam questions.
- The Silberschatz 9th-edition textbook is a reference covering much more than these lecture portions. Its inclusion does **not** make every textbook chapter an assigned exam portion. Relevant chapter mapping: 1–2 introduction/structures, 3 processes/IPC, 4 threads, 5 synchronization, 6 scheduling, 7 deadlocks, 8–9 memory/virtual memory, 10 storage, 11 file-system interface.
- Other project-root supplements are separate from sir's two folders: `w2_processes1.ppt.pptx`, `OS_Synchronization_30_Questions.pptx`, `DOC-20261104-WA0000.pdf`, `process_scheduling_exam_summary.pdf`, `xv6_RISC-V_Primer.pdf`, and another copy of the deadlock simulation. The `project/` research/code directory is not treated as course portions.
- Architecture matters: several lecture examples use **32-bit x86 xv6**, while the separate primer is labelled **RISC-V**. Register names and paging details should be studied in their respective architecture context.
- This is a source-based portions checklist, not a faculty-confirmed endsem announcement. File systems/RTOS and the exact pre-midsem cutoff remain syllabus/exam-scope questions.
