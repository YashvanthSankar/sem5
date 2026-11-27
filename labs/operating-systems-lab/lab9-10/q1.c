// ===== proc.h =====  (inside struct proc, after "int pid;")
  int ctime;                   // creation time (ticks)
  int priority;                // lower value = higher priority

// ===== proc.c =====  (allocproc(), after "p->pid = nextpid++;")
  p->ctime = ticks;
  p->priority = 3;             // default priority

// ===== proc.c =====  (replace the whole scheduler() function)
void
scheduler(void)
{
  struct proc *p, *best;
  struct cpu *c = mycpu();

  c->proc = 0;
  for(;;){
    sti();
    acquire(&ptable.lock);

    best = 0;
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
      if(p->state != RUNNABLE)
        continue;
      // Method 2: priority, then ctime, then pid
      if(best == 0 ||
         p->priority < best->priority ||
         (p->priority == best->priority && p->ctime < best->ctime) ||
         (p->priority == best->priority && p->ctime == best->ctime &&
          p->pid < best->pid))
        best = p;
      // Method 1 (pure FCFS): use this condition instead
      // if(best == 0 ||
      //    p->ctime < best->ctime ||
      //    (p->ctime == best->ctime && p->pid < best->pid))   // same tick -> smaller pid
      //   best = p;
    }

    if(best != 0){
      c->proc = best;
      switchuvm(best);
      best->state = RUNNING;
      swtch(&(c->scheduler), best->context);
      switchkvm();
      c->proc = 0;
    }
    release(&ptable.lock);
  }
}

// ===== proc.c =====  (add at the end of the file)
int
setpriority(int pid, int priority)
{
  struct proc *p;

  if(priority < 0)
    return -1;
  acquire(&ptable.lock);
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
    if(p->pid == pid && p->state != UNUSED){
      p->priority = priority;
      release(&ptable.lock);
      return 0;
    }
  }
  release(&ptable.lock);
  return -1;                   // no such process
}

// ===== trap.c =====  (inside trap(): comment out the timer yield = no preemption)
  // if(myproc() && myproc()->state == RUNNING &&
  //    tf->trapno == T_IRQ0+IRQ_TIMER)
  //   yield();

// ===== sysproc.c =====  (add at the end)
int
sys_setpriority(void)
{
  int pid, priority;

  if(argint(0, &pid) < 0 || argint(1, &priority) < 0)
    return -1;
  return setpriority(pid, priority);
}

// ===== defs.h =====  (proc.c section, after "void yield(void);")
int             setpriority(int, int);

// ===== syscall.h =====  (next free number: 22 in clean xv6; 24 in your tree after lab 7's 22 and 23)
#define SYS_setpriority 22

// ===== syscall.c =====
extern int sys_setpriority(void);          // with the other externs
[SYS_setpriority] sys_setpriority,         // last entry in syscalls[]

// ===== user.h =====
int setpriority(int pid, int priority);

// ===== usys.S =====
// SYSCALL(setpriority)

// ===== Makefile =====  (UPROGS)
// 	_schedtest\

// ===== schedtest.c =====  (new file)
#include "types.h"
#include "stat.h"
#include "user.h"

#define NCHILDREN 4
#define WORK 20000000          // raise it if children finish too fast to see

void
runtest(int mode)
{
  int pids[NCHILDREN];
  int prio[NCHILDREN] = {3, 1, 2, 0};
  int i, j;

  if(mode == 1)
    printf(1, "\n=== FCFS test (every child keeps priority 3) ===\n");
  else
    printf(1, "\n=== Priority test (parent sets priorities) ===\n");

  for(i = 0; i < NCHILDREN; i++){
    pids[i] = fork();
    if(pids[i] < 0){
      printf(1, "fork failed\n");
      exit();
    }
    if(pids[i] == 0){
      volatile int v = 0;
      printf(1, "Child %d started\n", getpid());
      for(j = 0; j < WORK; j++)
        v++;
      printf(1, "Child %d finished\n", getpid());
      exit();
    }
  }

  // No preemption: the parent keeps the CPU until it calls wait(),
  // so it can set every child's priority before any child runs.
  if(mode == 2){
    for(i = 0; i < NCHILDREN; i++){
      setpriority(pids[i], prio[i]);
      printf(1, "PID %d -> priority %d\n", pids[i], prio[i]);
    }
  }

  for(i = 0; i < NCHILDREN; i++)
    wait();                    // parent sleeps -> scheduler picks the next child
  printf(1, "All children completed.\n");
}

int
main(void)
{
  runtest(1);
  runtest(2);
  exit();
}
