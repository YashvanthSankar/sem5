// ===== syscall.h =====
#define SYS_getprocstates 24

// ===== user.h =====
int getprocstates(void);

// ===== usys.S =====
// SYSCALL(getprocstates)

// ===== syscall.c =====
extern int sys_getprocstates(void);         // with the other externs
// [SYS_getprocstates] sys_getprocstates,   // inside the syscalls[] table

// ===== defs.h =====   (under // proc.c)
int             getprocstates(void);

// ===== sysproc.c =====
int
sys_getprocstates(void)
{
  return getprocstates();
}

// ===== proc.c =====   (ptable is defined here)
int
getprocstates(void)
{
  static char *statename[] = {
  [UNUSED]    "UNUSED  ",                   // padded to 8 chars so columns line up
  [EMBRYO]    "EMBRYO  ",
  [SLEEPING]  "SLEEPING",
  [RUNNABLE]  "RUNNABLE",
  [RUNNING]   "RUNNING ",
  [ZOMBIE]    "ZOMBIE  "
  };
  struct snap {
    int pid;
    enum procstate state;
    char name[16];
  } list[NPROC];
  struct proc *cur = myproc();              // the caller
  struct proc *p;
  int i, n = 0, cpid;
  enum procstate cstate;
  char cname[16];

  acquire(&ptable.lock);                    // copy under the lock
  cpid = cur->pid;
  cstate = cur->state;                      // always RUNNING
  safestrcpy(cname, cur->name, sizeof(cname));
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
    if(p->state == UNUSED)
      continue;
    list[n].pid = p->pid;
    list[n].state = p->state;
    safestrcpy(list[n].name, p->name, sizeof(list[n].name));
    n++;
  }
  release(&ptable.lock);                    // print only after releasing

  cprintf("Current process: PID=%d NAME=%s STATE=%s\n", cpid, cname, statename[cstate]);
  cprintf("PID\tSTATE\t\tNAME\n");
  for(i = 0; i < n; i++)
    cprintf("%d\t%s\t%s\n", list[i].pid, statename[list[i].state], list[i].name);
  return n;
}

// ===== Makefile =====
// UPROGS: add  _procstate\

// ===== procstate.c =====
#include "types.h"
#include "stat.h"
#include "user.h"

int
main(void)
{
  getprocstates();
  exit();
}
