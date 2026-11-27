# OS Lab — Exam Portions / Topics to Prepare

Compiled from `lab1`–`lab4` source files and `linux_commands.pdf`.

---

## Unit 1 — Processes & `fork()`

- `fork()` semantics: return value (`0` in child, `>0` = child PID in parent, `<0` on failure)
- What gets duplicated on fork (PCB, address space, copy-on-write)
- Process count from N forks: general rule `2^N` processes, `2^N - 1` children
- Conditional forks (`fork() % 2`, `if (fork() != 0)`) — counting processes and drawing the process tree
- `getpid()` vs `getppid()`
- **Zombie process**: definition, cause (parent never calls `wait()`), `Z` state, reaping with `wait()`
- **Orphan process**: parent dies first, re-parenting to `init` / PID 1, detecting via `getppid()` change
- `wait()` vs `waitpid()` (waiting on a specific PID), `exit()` vs `return`

**References:** `lab1/q2.c`, `lab1/q3.c`, `lab1/q4.c`, `lab1/q5.c`, `lab2/q4.c`

---

## Unit 2 — Program Execution (exec family)

- `execl()` / `execlp()` / `execv()` syntax and `argv` convention (`argv[0]`, NULL terminator)
- Replacing the child memory image; exec returns only on failure
- Fork + exec pattern (run external Linux commands such as `cp`)
- Parallel child processes: forking multiple children, `waitpid` on each, concurrency
- Command-line arguments: `argc` / `argv`, `atof()`, argument validation

**References:** `lab2/q2/backup.c`, `lab2/q2/b.c`, `lab2/q3/controller.c`, `lab2/q3/calc_worker.c`

---

## Unit 3 — Pipes / IPC

- `pipe(fd)`: `fd[0]` = read end, `fd[1]` = write end
- One-way (half-duplex) communication, parent to child
- Two-way communication using two pipes; avoiding deadlock
- Closing unused pipe ends is mandatory (EOF, no resource leak)
- Reading/writing typed binary data (`sizeof(int)`) vs strings
- Signalling errors (e.g. division by zero) via status codes

**References:** `lab3/q1.c`, `lab3/q2.c`

---

## Unit 4 — Shared Memory

### POSIX API
- `shm_open`, `ftruncate`, `mmap` (`PROT_READ`/`PROT_WRITE`, `MAP_SHARED`), `munmap`, `shm_unlink`
- Virtual filesystem backing: `/dev/shm` (`ls -la /dev/shm`, `cat /dev/shm/<name>`)

### System V API
- `ftok()`, `shmget()` (`IPC_CREAT`, `IPC_PRIVATE`, permissions), `shmat()`, `shmdt()`, `shmctl(IPC_RMID)`
- Kernel inspection: `ipcs -m`, `ipcrm`, meaning of `nattch`
- Cleanup order: detach then remove; who calls `shm_unlink` / `IPC_RMID`
- Parallel computation on non-overlapping partitions (row slices of matrix C, no locks needed)
- Matrix multiply `C[i][j] = Σ A[i][k] * B[k][j]`; verify `A × I = A`

**References:** `lab4/q1.c`, `lab4/q2_sysv_creator.c`, `lab4/q2_sysv_reader.c`, `lab4/q2.txt`, `lab4/q3.c`

---

## Unit 5 — File I/O in C

- `fopen` modes, `fgets`, `strlen`, `isspace`, `fclose`
- Counting lines / words / characters; finding the longest line
- Word counting with whitespace-boundary logic

**References:** `lab1/q1.c`

---

## Unit 6 — Linux Commands & Shell

### File & folder handling
- Navigation: `pwd`, `ls`, `ls -l`, `ls -la`, `cd`, `cd ..`, `cd ~`, `tree`
- Create/remove: `mkdir`, `mkdir -p`, `touch`, `rm`, `rm -r`, `rm -rf`, `rmdir`
- Copy/move: `cp`, `cp -r`, `mv`, `ln -s`
- Viewing/editing: `cat`, `less`, `head`, `tail`, `tail -f`, `nano`, `vim`
- Search: `find /path -name`, `locate`, `grep`, `grep -r`, `which`
- Permissions: `chmod`, `chmod +x`, `chown`, `stat`
- Disk: `df -h`, `du -sh`, `df -T`

### Process management
- Viewing: `ps`, `ps aux`, `ps -ef`, `top`, `htop`, `pgrep`
- Controlling: `kill`, `kill -9`, `killall`, `pkill`, `bg`, `fg`, `jobs`, `nohup cmd &`, `nice`, `renice`

### Process tree
- `pstree`, `pstree -p`, `ps -ef --forest`, `ps -ejH`, `ps --ppid PID`
- `systemctl status`, `cat /proc/PID/status`, `ps -o pid,ppid,cmd -p PID`

### Process states
- `R` running/runnable, `S` sleeping, `D` uninterruptible sleep, `T` stopped, `Z` zombie
- Zombie vs orphan comparison table

### Text pipelines
- `grep` + `awk`/`cut` + `sort` + `uniq -c` + `sort -rn` + `head`
- access.log: extract IPs with 401/403, count per IP, top 5 offenders

**References:** `linux_commands.pdf`, `lab1/q6.txt`, `lab2/q1.txt`

---

## High-Priority / Most Likely Exam Questions

1. Process count and process-tree drawing after multiple `fork()` calls
2. Zombie vs orphan — with code to demonstrate both
3. Two-way pipe calculator (close unused ends, avoid deadlock)
4. Fork + exec to run a command as a child process
5. POSIX vs System V shared memory lifecycle and cleanup (`ipcs -m`, `shm_unlink`, `IPC_RMID`)
6. Parallel computation using shared memory slices + `waitpid`

> Tip: Be able to write each of these from scratch and explain exact system-call return values and cleanup steps.
