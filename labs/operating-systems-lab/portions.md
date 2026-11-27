# OS Lab — Endsem Portions (Lab 1 → Lab 11)

Concept-wise list of everything in this folder, with the file to revise and common mistakes.
⚠️ marks a common mistake, so check those first.

Exam pattern (from the midsem): **Q1 ≈ 10 marks / 45 min** (a smaller program + 2-line theory) and
**Q2 ≈ 20 marks / 90 min** (bigger program + "Trouble" theory parts). Questions are stories (weaver, harbour, printers…);
the concept underneath is what matters. **Read the Allowed / Not allowed list.**

---

## Part A — Processes (Lab 1, Lab 2)

### A1. `fork()`
- Returns `0` in the child, the child's PID in the parent, `-1` on failure.
- Child gets a **copy** of the parent's memory (copy-on-write): globals, stack, heap, open file descriptors.
  Changes in one are **not** seen by the other (midsem Trouble 1: `local_count` stays 0).
- Counting processes: `n` plain forks → `2^n` processes.
  - `fork(); fork(); fork();` → 8 (`lab1/q2.c`)
  - `fork(); fork(); if(fork()==0) fork();` → 12 (`lab1/q3.c`)
  - `if(fork()) if(fork()) fork();` → 4: one parent + 3 children (`lab1/q5.c`)
- Draw the process tree for any fork code. Practise conditions like `fork() && fork() || fork()`.
- ⚠️ `printf` without `\n` before `fork()` → text sits in the stdio buffer, gets copied, prints **twice**.
  Use `\n` or `fflush(stdout)` before forking.
- Fork loop for N children: the child must `exit()` / `break`, or it keeps forking too (midsem Part 1).

### A2. `wait()`, `waitpid()`, `exit()`
- `wait(NULL)` waits for any child; `waitpid(pid, &status, 0)` for a specific one; `WEXITSTATUS(status)`.
- Call `wait()` once per child.

### A3. Zombie and orphan
| | Zombie | Orphan |
|---|---|---|
| Still running? | No, it has exited | Yes |
| Cause | parent hasn't called `wait()` | parent exited first |
| Seen as | `Z` in `ps` | PPID changes to 1 (or a `systemd --user` subreaper on Ubuntu) |
| Cleanup | parent's `wait()` (or init after re-parenting) | init adopts and reaps it |
- Zombie demo: child exits, parent `sleep(10)` + `system("ps -o pid,ppid,stat,cmd")`, then `wait()` (`lab1/q4.c`).
- Orphan demo: save the parent PID before `fork()`, then have the child loop while `getppid() == parent` (`lab2/q4.c`, midsem Trouble 4).
- "Why no orphans when the dock waits?" Because the parent `wait()`s for its children **before** it exits.

### A4. `exec` family
- `execl("/bin/cp", "cp", src, dst, (char *)NULL);` (`argv[0]` = program name, list ends with `NULL`).
- `execlp` searches `PATH`; `execv` takes an array.
- exec **replaces** the process image; code after it runs **only if exec failed**.
- Fork + exec pattern: the child execs, the parent waits (`lab2/q2/backup.c`).
- Parallel children running another program: fork twice, exec in each, `waitpid` both (`lab2/q3/controller.c`).
- `argc/argv`, `atof`, argument checks (`lab2/q3/calc_worker.c`).

### A5. Linux commands (`linux_commands.pdf`, `lab1/q6`, `lab2/q1`)
- Files: `pwd ls -la cd mkdir -p touch rm -r rmdir cp -r mv ln -s cat less head tail -f find grep -r chmod chown stat df -h du -sh`.
- Processes: `ps aux`, `ps -ef`, `ps -ef --forest`, `pstree -p`, `top`, `kill -9`, `pkill`, `jobs/bg/fg`, `nohup`, `nice/renice`,
  `cat /proc/PID/status`, `ps -o pid,ppid,stat,cmd -p PID`.
- States: `R` running, `S` sleeping, `D` uninterruptible, `T` stopped, `Z` zombie.
- Log pipeline (401/403 offenders):
  `grep -E '" (401|403) ' access.log | grep -oE '^[0-9.]+' | sort | uniq -c | sort -nr | head -5`

### A6. File I/O in C (`lab1/q1.c`)
- `fopen/fgets/fclose`, counting lines / words (a word starts where a non-space follows a space) / characters, longest line.

---

## Part B — IPC (Lab 3, Lab 4, Midsem)

### B1. Pipes (`lab3/q1.c`, `lab3/q2.c`, `midsem_lab/q1.c`)
- `pipe(fd)` **before** `fork()`; `fd[0]` = read end, `fd[1]` = write end. A pipe is one-way.
- Each side **closes the end it doesn't use**.
- Two-way communication = **two pipes** (parent→child and child→parent).
- `write(fd[1], &x, sizeof(x))` / `read(fd[0], &x, sizeof(x))` for ints, in the same order.
- `read()` returns **0 (EOF)** when no write end is open anywhere.
- ⚠️ Midsem theory, correct answers:
  - "If the writer exits without writing, what does `read()` return?" → **0 (EOF)**; the variables keep their old values.
  - "Why must the reader close its own write end?" → otherwise the kernel still counts it as a writer, so `read()`
    **never sees EOF** and blocks forever. (Not "because pipes are half duplex".)
- ⚠️ Strings: send the `'\0'` too, or null-terminate after `read()`: `n = read(...); buf[n] = '\0';`
  (`lab3/q1.c` printed garbage after "Hello, Child!").
- Error signalling through a pipe: send a status code first (e.g. `-1` for divide by zero), then the result.

### B2. POSIX shared memory (`lab4/q1`)
- `shm_open("/name", O_CREAT|O_RDWR, 0666)` → `ftruncate(fd, SIZE)` → `mmap(NULL, SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0)`
  → use → `munmap` → `close` → `shm_unlink("/name")`.
- Shows up as a file in `/dev/shm` (`ls -la /dev/shm`, `cat /dev/shm/name`). Linux only (not macOS).

### B3. System V shared memory (`lab4/q2`, `lab4/q3.c`, `midsem_lab/q2.c`)
- `key = ftok(".", 'B')` → `shmid = shmget(key, size, IPC_CREAT|0666)` → `ptr = shmat(shmid, NULL, 0)` → `shmdt(ptr)` →
  `shmctl(shmid, IPC_RMID, NULL)`.
- `IPC_PRIVATE` = a new segment that only this process (and its later-forked children) can find.
- `shmat` returns `(void *)-1` on error.
- Inspect: `ipcs -m` (column **nattch** = attached processes); remove: `ipcrm -m <shmid>`.
  A segment stays listed (nattch 0) after everyone detaches **until IPC_RMID / ipcrm**.
- Attach **before** `fork()`: children inherit the attachment (nattch counts them; 13 in the midsem).
- ⚠️ Midsem Trouble 2: don't store **pointers** in shared memory. A second `shmat` can map the segment at a different
  virtual address, so a stored `best = &porter[i][j]` points to the wrong place. Store an **index/offset**
  (`best_idx`) and rebuild the pointer from the current attachment. (It is not a race condition.)
- ⚠️ Midsem Trouble 3: a child doing `shmget(IPC_PRIVATE)` after fork gets a **brand-new** segment that the parent
  never sees. Fix: use the inherited one.
- Parallel work with no locks: each worker writes only its own slice (matrix rows `w*n/k … (w+1)*n/k`), parent reads
  after `wait()` (`lab4/q3.c`, verify `A × I = A`).
- ⚠️ Initialise accumulators (`int spice[3] = {0};`) and get tie logic right (midsem Q2).

---

## Part C — Threads & synchronization (Lab 5, Lab 6)

| Question | What to learn first |
|---|---|
| [5 Q1 · Thread sums](lab5/q1.md) | Pass each half by pointer. Separate results, then join. |
| [5 Q2 · Bank balance](lab5/q2.md) | One worker, signed amounts, one mutex around each update. |
| [5 Q3 · Printers](lab5/q3.md) | Three permits. Wait before printing, post after. |
| [5 Q4 · Banking engine](lab5/q4.md) | Two locks in account order for transfers. All locks in the same order for audits. One lock to freeze an account. |
| [6 Q1 · Priority spooler](lab6/q1.md) | Wait before locking. Pick the first priority job. For shutdown, join the producers and wake each printer. |
| [6 Q2 · Dining philosophers](lab6/q2.md) | Ordered chopsticks, two sauce permits, then the hungry quota. Add timestamps and max wait last. |
| [7 Q1 · Trace sleep](lab7/q1.md) | EAX and the user stack → syscall handler → sleep and wakeup → popal and iret. |
| [7 Q2 · Process info](lab7/q2.md) | Read the option, get the caller, check for a parent, return the requested value. |
| [7 Q3 · Process count](lab7/q3.md) | Scan under the process-table lock and count every non-UNUSED slot. |
| [8 Q1 · Process states](lab8/q1.md) | Copy under the process-table lock and print after releasing it. |
| [9–10 Q1 · FCFS and non-preemptive priority](lab9-10/q1.md) | Pick a RUNNABLE winner by creation time or priority. Remove timer yield. |
| [9–10 Q2 · Preemptive priority](lab9-10/q2.md) | Pick the lowest priority value, then earliest creation tick. Keep timer yield and yield after a priority change. |
| [9–10 Q3 · Lottery](lab9-10/q3.md) | Sum runnable tickets, draw one, and scan again to find its owner. |
| [11 Q1 · getprocs and ps](lab11/q1.md) | Validate the buffer, copy under the lock, and print in user space. Add nrun for the extension. |

Learn the xv6 syscall registration steps once. Timing delays, random seeds, column formatting, and demo output are details to read after you can explain the main algorithm. Keep any timing, logging, or test behavior that the question explicitly asks for.

Compile with `gcc file.c -o file -pthread`.

### C1. Pthreads basics (`lab5/q1.c`)
- `pthread_create(&t, NULL, func, arg)`, `void *func(void *arg)`, `pthread_join(t, NULL)`.
- Threads **share** globals and heap (unlike fork); each has its own stack.
- Pass `marks` and `marks + HALF` to the two workers. Each pointer starts a five-element half.
  When passing IDs in a loop, give each thread its own ID variable.
- No lock needed when each thread writes a **different** variable and main reads after `join`.

### C2. Race condition, critical section, mutex (`lab5/q2.c`)
- `bal += x` is load → add → store; two threads interleave → **lost update** = race condition.
- Critical section = code touching shared data. Mutex = mutual exclusion:
  `pthread_mutex_init / lock / unlock / destroy` (or `PTHREAD_MUTEX_INITIALIZER`).
- ⚠️ Lock **per transaction** (inside the loop), not around the whole loop (which serializes the threads).

### C3. Semaphores (`lab5/q3.c`)
- `sem_init(&s, 0, N)` (0 = between threads, N = initial count), `sem_wait` (decrement or **block**), `sem_post`
  (increment + wake one), `sem_destroy`. Counting semaphore = N identical resources (3 printers).
- Binary semaphore (init 1) ≈ mutex, but any thread may post; a mutex must be unlocked by its owner.
- macOS doesn't support `sem_init`, so test on Linux.

### C4. Deadlock and lock ordering (`lab5/q4.c`, banking engine)
- 4 conditions: mutual exclusion, hold & wait, no preemption, **circular wait**.
- Lock ordering (always lock the lower-numbered account first) removes circular wait:
  `transfer(5→9)` and `transfer(9→5)` both lock 5 then 9.
- ⚠️ `from == to` → locking the same mutex twice → self-deadlock. Reject it first. Also reject `amount <= 0`.
- Consistent snapshot (audit): lock **all** accounts in the same order, sum, unlock.
- Per-account locks → disjoint transfers run in parallel (no global lock).
- Use `rand_r(&seed)` with a separate seed per worker so each thread has its own random sequence.

### C5. Producer–consumer / bounded buffer (`lab6/q1.c`)
- `empty` = free slots (init N), `full` = filled slots (init 0), mutex for the buffer.
- Producer: `sem_wait(empty)` → lock → insert → unlock → `sem_post(full)`. Consumer is the mirror.
- **Order matters:** `sem_wait` **before** locking the mutex. Locking first and then blocking on a full/empty buffer
  = deadlock.
- Priority jobs: the consumer scans for a priority job, else takes the oldest.
- Clean termination: join producers and post `full` once per printer. Only those extra wake-ups can find an empty queue.

### C6. Dining philosophers (`lab6/q2.c`)
- Deadlock if everyone picks up the left chopstick first. Fixes: **resource ordering** (lower-numbered chopstick
  first), allow at most N−1 at the table, or an asymmetric philosopher.
- Extra resource (sauce, max 2) = counting semaphore, taken **last**, released **first** → no new cycle.
- Starvation vs deadlock: no deadlock does not mean no starvation. A fairness rule is needed (hungry philosophers: each normal
  one may start at most 2 meals between two hungry meals).
- Timing: `gettimeofday`, elapsed ms, `usleep`; summary table of meals and max wait.
- Update the fairness counters at the logged start of eating. Check the quota before taking any chopsticks.

Also revise: `theory/operating-systems/questions/OS_Synchronization_30_Questions.pptx` (30 synchronization questions).

---

## Part D — xv6 (Lab 7 → Lab 11)

Setup: `xv6/` in this folder (Docker Ubuntu), `references/xv6_installation.md`. Run with `make qemu-nox CPUS=1`, quit with `Ctrl-a x`.

### D1. Adding a system call: the 8 edits (`lab7/q1.md`)
| File | Add |
|---|---|
| `syscall.h` | `#define SYS_name N` (next unused; stock uses 1–21) |
| `user.h` | user prototype |
| `usys.S` | `SYSCALL(name)` → `movl $SYS_name, %eax; int $64; ret` |
| `syscall.c` | `extern int sys_name(void);` + `[SYS_name] sys_name,` |
| `sysproc.c` | `int sys_name(void)` → fetch args, call helper |
| `proc.c` | helper that touches `ptable` (the table is defined there) |
| `defs.h` | kernel prototype of the helper (`// proc.c` section) |
| `Makefile` | `_prog\` in `UPROGS` (then `make clean`) |
- ⚠️ Never redefine an existing number (`SYS_close 24` in your lab 9 Q2 screenshots).

### D2. Syscall path and arguments (lab 7 Q1, the `sleep(100)` trace)
- User `sleep(100)` → 100 pushed on the **user stack** → `usys.S`: `eax = SYS_sleep (13)`, `int $64` → CPU switches to the
  kernel stack (TSS) → `vectors.S` → `alltraps` (`trapasm.S`) builds the **trapframe** → `trap(tf)` → `syscall()`:
  `num = tf->eax`, `tf->eax = syscalls[num]()` → `trapret` → `iret` → back in user mode, return value in `%eax`.
- `argint(n, &x)` reads `tf->esp + 4 + 4*n` (skip the return address) via `fetchint`; `argptr(n, &p, size)` also checks
  the whole buffer is inside the process's memory; `argstr` for strings.
- `sys_sleep`: `acquire(&tickslock); ticks0 = ticks; while(ticks - ticks0 < n){ if killed → -1; sleep(&ticks, &tickslock); }`.
- Timer: CPU 0 does `ticks++; wakeup(&ticks);` every tick → the sleeper is woken **every tick** and re-checks.

### D3. Process table and states (lab 7 Q3, lab 8, lab 11)
- `struct proc` (`proc.h`), `ptable.proc[NPROC=64]` + `ptable.lock` (`proc.c`).
- States: `UNUSED → EMBRYO (allocproc) → RUNNABLE (fork/userinit) ⇄ RUNNING (scheduler / yield) → SLEEPING (sleep) →
  RUNNABLE (wakeup/kill)`; `RUNNING → ZOMBIE (exit) → UNUSED (parent's wait)`.
- Traverse `ptable` **only under `ptable.lock`**: other CPUs change states under that lock; you'd see half-updated slots.
  `acquire` also disables interrupts.
- `myproc()` = `mycpu()->proc`: only the process running **on this CPU**, which is the caller. To see others, scan `ptable`.
- Print after releasing the lock: `cprintf` takes `cons.lock`, and the console interrupt takes `cons.lock` then
  `ptable.lock` (lab 8 design).
- `getproccount` (lab 7 Q3): count `state != UNUSED`; fork test 3 → 4 → 3; compare with `>=` because of other activity.
- `process_info(option)` (lab 7 Q2): pid / parent pid / |difference| / −1; init has `parent == 0`.
- `getprocstates` (lab 8, `lab8/`): current process via `myproc()` + all non-UNUSED via ptable.
- `getprocs(struct uproc *buf, int max)` + `ps` (lab 11, `lab11/q1.md`): shared header `uproc.h`,
  `argint` + `argptr`, `safestrcpy`, never more than `max` entries.
- Explain from `ps` output:
  - ps is always **RUNNING**: it is the caller.
  - init and sh are **SLEEPING** in `wait()` (sh in `read()` when idle).
  - init's **PPID is 0**: created by `userinit`, no parent.
  - **ZOMBIE**: between a child's `exit` and the parent's `wait`.
  - **RUNNABLE** `spin`: it was preempted by the timer.
  - Background `&` jobs have **PPID 1** because sh's intermediate child exits; init prints `zombie!` when it reaps them.

### D4. Scheduler internals (scheduler PDF)
- One `scheduler()` loop per CPU; every switch goes process → scheduler → process via `swtch`
  (saves `edi esi ebx ebp eip`).
- Only 3 ways into `sched()`: `yield()` (timer), `sleep()`, `exit()`. `sched()` panics unless: `ptable.lock` held,
  `ncli == 1`, state ≠ RUNNING, interrupts off.
- `ptable.lock` is acquired by the old process and released by the new one (or by `forkret` for a new process).
- Timer preemption = the `yield()` at the end of `trap()` (trap.c). Time slice = 1 tick.
- Default policy = **round robin by slot index** (not arrival order).
- `sleep(chan, lk)` takes `ptable.lock` before releasing `lk` → no lost wakeup; `wakeup` only marks RUNNABLE.
- Where to change things: `proc.h` (new fields), `allocproc` (initialise them), `fork` (inherit), `scheduler()`
  (selection), `trap.c` (preemption, per-tick accounting), new syscalls (`setpriority`, `settickets`), `CPUS=1`.
- Keep the scheduler "plumbing" in order: `c->proc = p; switchuvm(p); p->state = RUNNING; swtch(&(c->scheduler), p->context);
  switchkvm(); c->proc = 0;`. ⚠️ Not the old `proc = p` / `cpu->scheduler`.

### D5. Scheduling policies (lab 9–10, `lab9-10/q1.md–q3.md`)
- **Non-preemptive** (Q1): comment out the timer `yield()`; `ctime = ticks` in allocproc; FCFS = smallest ctime
  (tie → pid); priority = smallest priority, ties by ctime. A CPU-bound job keeps the CPU until it exits or blocks.
  ⚠️ Set priorities from the **parent** (by pid) before the children run. A child setting its own priority after it is
  already scheduled just gives FCFS order.
- **Preemptive priority** (Q2): keep the timer `yield()`; default priority 10; pick the lowest value, ties by creation tick, then PID;
  `setpriority(pid, prio)` under `ptable.lock` then `yield()`. Issue: **starvation** → fix with **aging**.
- **Lottery** (Q3): `tickets` field (default 10, inherited in `fork`), `settickets(n)`, kernel PRNG (xorshift),
  winner = `rand % total + 1` over the RUNNABLE ticket ranges. CPU share ∝ tickets.
  Probabilistic; no starvation.
- Compare: FCFS (simple, convoy effect), non-preemptive priority, preemptive priority (responsive, starvation),
  round robin (fair, more switches), lottery (proportional, probabilistic).
- `nrun` counter (lab 11 extension): incremented in `scheduler()` each time a process is chosen. It counts *selections*,
  not CPU time. A process in `sleep()` is still chosen every tick (woken by `wakeup(&ticks)`).

---

## Priority order for the last days

1. **Midsem-style Q2 from scratch** (SysV shm + fork tree + the 4 Troubles) and **Q1** (pipe + EOF theory).
2. **Producer–consumer** and **dining philosophers** with semaphores (with correct termination and no deadlock).
3. **Mutex bank / lock ordering** (deadlock conditions, `from == to`).
4. **Adding an xv6 syscall end-to-end** (8 files) in ≤ 20 min: `getproccount`, `process_info`, `getprocstates`, `getprocs`/`ps`.
5. **One scheduler change** each: non-preemptive FCFS/priority, preemptive priority + `setpriority`, lottery.
6. Theory one-liners: zombie vs orphan, fork vs threads memory, race / critical section, mutex vs semaphore,
   4 deadlock conditions, `myproc()` vs ptable scan, why lock ptable, process states, `sleep(100)` trace.
7. Linux commands and the `grep | sort | uniq -c | sort -nr | head` pipeline.

Not in your labs (check your syllabus): condition variables, reader–writer locks, paging/virtual memory, file systems.
