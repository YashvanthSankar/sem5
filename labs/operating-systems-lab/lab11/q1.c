// ===== uproc.h =====  (new file, shared by kernel and user programs)
#ifndef UPROC_H
#define UPROC_H

struct uproc {
  int pid;
  int ppid;        // parent's pid, 0 if no parent (init)
  int state;       // enum procstate value
  int nrun;        // extension: times chosen by scheduler()
  char name[16];
};

#endif

// ===== proc.h =====  (extension: inside struct proc, after "char name[16];")
  int nrun;                    // times chosen by scheduler()

// ===== proc.c =====  (with the other includes)
#include "uproc.h"

// ===== proc.c =====  (extension: allocproc(), after "p->pid = nextpid++;")
  p->nrun = 0;

// ===== proc.c =====  (extension: scheduler(), after "p->state = RUNNING;")
      p->nrun++;

// ===== proc.c =====  (add at the end of the file)
int
getprocs(struct uproc *buf, int max)
{
  struct proc *p;
  int count = 0;

  acquire(&ptable.lock);
  for(p = ptable.proc; p < &ptable.proc[NPROC] && count < max; p++){
    if(p->state == UNUSED)
      continue;                // skip empty slots
    buf[count].pid = p->pid;
    buf[count].ppid = p->parent ? p->parent->pid : 0;   // init has no parent
    buf[count].state = p->state;
    buf[count].nrun = p->nrun;
    safestrcpy(buf[count].name, p->name, sizeof(buf[count].name));
    count++;
  }
  release(&ptable.lock);
  return count;
}

// ===== sysproc.c =====  (with the other includes, after "proc.h")
#include "uproc.h"

// ===== sysproc.c =====  (add at the end)
int
sys_getprocs(void)
{
  int max;
  char *buf;

  if(argint(1, &max) < 0)
    return -1;
  if(max < 0 || max > 2147483647 / sizeof(struct uproc))   // avoid overflow in max*size
    return -1;
  if(argptr(0, &buf, max * sizeof(struct uproc)) < 0)      // whole buffer must be user memory
    return -1;
  return getprocs((struct uproc *)buf, max);
}

// ===== defs.h =====
struct uproc;                                     // top, with the other struct declarations
int             getprocs(struct uproc*, int);     // proc.c section

// ===== syscall.h =====  (next free number: 22 in clean xv6)
#define SYS_getprocs 22

// ===== syscall.c =====
extern int sys_getprocs(void);             // with the other externs
[SYS_getprocs] sys_getprocs,               // last entry in syscalls[]

// ===== user.h =====
struct uproc;
int getprocs(struct uproc *buf, int max);

// ===== usys.S =====
// SYSCALL(getprocs)

// ===== Makefile =====  (UPROGS)
// 	_ps\
// 	_sleepy\
// 	_ztest\
// 	_spin\

// ===== ps.c =====  (new file)
#include "types.h"
#include "stat.h"
#include "user.h"
#include "uproc.h"

#define MAXPROC 64

// Same order as enum procstate in proc.h. Padded to 8 chars so the columns line up.
char *statename[] = {
  "UNUSED  ", "EMBRYO  ", "SLEEPING", "RUNNABLE", "RUNNING ", "ZOMBIE  "
};

int
main(void)
{
  struct uproc buf[MAXPROC];
  int n, i;
  char *s;

  n = getprocs(buf, MAXPROC);
  if(n < 0){
    printf(1, "ps: getprocs failed\n");
    exit();
  }

  printf(1, "PID\tPPID\tSTATE\t\tNRUN\tNAME\n");
  for(i = 0; i < n; i++){
    if(buf[i].state >= 0 && buf[i].state <= 5)
      s = statename[buf[i].state];
    else
      s = "UNKNOWN ";
    printf(1, "%d\t%d\t%s\t%d\t%s\n",
           buf[i].pid, buf[i].ppid, s, buf[i].nrun, buf[i].name);
  }
  exit();
}

// ===== sleepy.c =====  (new file: mostly sleeps)
#include "types.h"
#include "stat.h"
#include "user.h"

int
main(void)
{
  printf(1, "Sleepy process started\n");
  sleep(500);                      // 500 ticks = 5 seconds
  printf(1, "Sleepy process finished\n");
  exit();
}

// ===== ztest.c =====  (new file: child exits before the parent waits)
#include "types.h"
#include "stat.h"
#include "user.h"

int
main(void)
{
  int pid = fork();

  if(pid < 0){
    printf(1, "fork failed\n");
    exit();
  }
  if(pid == 0){
    printf(1, "Child process exiting\n");
    exit();                        // child is a ZOMBIE until the parent waits
  }
  printf(1, "Parent sleeping before wait()\n");
  sleep(300);                      // 3 seconds: time to type ps
  wait();
  printf(1, "Child collected by parent\n");
  exit();
}

// ===== spin.c =====  (new file: CPU-bound, never blocks)
#include "types.h"
#include "stat.h"
#include "user.h"

int
main(void)
{
  for(;;)
    ;
}
