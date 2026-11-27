// ===== proc.h =====  (inside struct proc, after "int pid;")
  int ctime;                   // creation tick
  int priority;                // lower value = higher priority

// ===== proc.c =====  (allocproc(), after "p->pid = nextpid++;")
  p->ctime = ticks;
  p->priority = 10;            // default priority

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
      if(best == 0 ||
         p->priority < best->priority ||                              // higher priority wins
         (p->priority == best->priority && p->ctime < best->ctime) ||
         (p->priority == best->priority && p->ctime == best->ctime &&
          p->pid < best->pid))   // same creation tick: earlier PID wins
        best = p;
    }

    if(best != 0){
      c->proc = best;          // not "proc = best" (old xv6)
      switchuvm(best);
      best->state = RUNNING;
      swtch(&(c->scheduler), best->context);   // not "&cpu->scheduler" (old xv6)
      switchkvm();
      c->proc = 0;
    }
    release(&ptable.lock);
  }
}

// ===== proc.c =====  (add at the end of the file; ptable is defined in this file)
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

// ===== trap.c =====  (keep it unchanged: the timer yield() is the preemption)
  if(myproc() && myproc()->state == RUNNING &&
     tf->trapno == T_IRQ0+IRQ_TIMER)
    yield();

// ===== sysproc.c =====  (add at the end)
int
sys_setpriority(void)
{
  int pid, priority;

  if(argint(0, &pid) < 0 || argint(1, &priority) < 0)
    return -1;
  if(setpriority(pid, priority) < 0)
    return -1;
  yield();                     // let a now-higher-priority process run at once
  return 0;
}

// ===== defs.h =====  (proc.c section, after "void yield(void);")
int             setpriority(int, int);

// ===== syscall.h =====  (next free number: 22 in clean xv6; 24 in your tree. Do NOT touch SYS_close 21)
#define SYS_setpriority 22

// ===== syscall.c =====
extern int sys_setpriority(void);          // with the other externs (no second sys_close extern)
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

#define WORK 20000000

int
main(void)
{
  int pid[4];
  int priority[4] = {15, 10, 5, 1};
  int i, j;

  printf(1, "\nPreemptive priority test (parent = 10)\n");
  for(i = 0; i < 4; i++){
    pid[i] = fork();
    if(pid[i] < 0){
      printf(1, "fork failed\n");
      exit();
    }
    if(pid[i] == 0){
      volatile int count = 0;
      for(j = 0; j < WORK; j++)
        count++;
      printf(1, "Child PID %d completed\n", getpid());
      exit();
    }
  }
  // Children start at 10, same as the parent, but were created later, so the parent keeps the CPU.
  for(i = 0; i < 4; i++){
    if(setpriority(pid[i], priority[i]) == 0)      // raising a child above 10 preempts the parent here
      printf(1, "PID %d assigned priority %d\n", pid[i], priority[i]);
    else
      printf(1, "setpriority failed for PID %d\n", pid[i]);
  }
  for(i = 0; i < 4; i++)
    wait();
  printf(1, "\nAll child processes completed.\n");
  exit();
}
