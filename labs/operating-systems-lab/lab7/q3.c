// ===== syscall.h =====
#define SYS_getproccount 23

// ===== user.h =====
int getproccount(void);

// ===== usys.S =====
// SYSCALL(getproccount)

// ===== syscall.c =====
extern int sys_getproccount(void);          // with the other externs
// [SYS_getproccount]  sys_getproccount,    // inside the syscalls[] table

// ===== proc.c =====   (ptable is defined here, so the loop lives here)
int
countprocs(void)
{
  struct proc *p;
  int count = 0;

  acquire(&ptable.lock);                    // consistent snapshot
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
    if(p->state != UNUSED)                  // EMBRYO SLEEPING RUNNABLE RUNNING ZOMBIE
      count++;
  }
  release(&ptable.lock);
  return count;
}

// ===== defs.h =====   (under // proc.c)
int             countprocs(void);

// ===== sysproc.c =====
int
sys_getproccount(void)
{
  return countprocs();
}

// ===== Makefile =====
// UPROGS: add  _getproccount_test\

// ===== getproccount_test.c =====
#include "types.h"
#include "user.h"

int
main(void)
{
  int pid;

  printf(1, "Before fork: %d\n", getproccount());
  pid = fork();
  if(pid < 0){
    printf(1, "fork failed\n");
    exit();
  }
  if(pid == 0)
    exit();

  // The child counts even if it has already become a zombie.
  printf(1, "Before wait: %d\n", getproccount());
  wait();
  printf(1, "After wait: %d\n", getproccount());
  exit();
}
