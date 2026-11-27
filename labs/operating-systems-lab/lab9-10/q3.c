// ===== proc.h =====  (inside struct proc, after "char name[16];")
  int tickets;                 // lottery tickets

// ===== proc.c =====  (allocproc(), after "p->pid = nextpid++;")
  p->tickets = 10;             // default tickets

// ===== proc.c =====  (fork(), right after the allocproc() check)
  if((np = allocproc()) == 0){
    return -1;
  }
  np->tickets = curproc->tickets;   // child inherits parent's tickets

// ===== proc.c =====  (above scheduler(): prototype, because random_next() is defined below it)
static uint random_next(void);

// ===== proc.c =====  (replace the whole scheduler() function)
void
scheduler(void)
{
  struct proc *p;
  struct cpu *c = mycpu();
  uint total, winning, current;

  c->proc = 0;
  for(;;){
    sti();
    acquire(&ptable.lock);

    // 1. Count the tickets of all RUNNABLE processes.
    total = 0;
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
      if(p->state == RUNNABLE)
        total += p->tickets;

    if(total > 0){
      // 2. Draw a winning ticket in 1..total.
      winning = random_next() % total + 1;

      // 3. Walk the RUNNABLE processes until the running sum reaches it.
      current = 0;
      for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
        if(p->state != RUNNABLE)
          continue;
        current += p->tickets;
        if(current >= winning){
          c->proc = p;
          switchuvm(p);
          p->state = RUNNING;
          swtch(&(c->scheduler), p->context);
          switchkvm();
          c->proc = 0;
          break;               // one winner per lottery
        }
      }
    }
    release(&ptable.lock);
  }
}

// ===== proc.c =====  (right below scheduler())
// Xorshift pseudo-random number generator.
static uint rand_state = 2463534242U;

static uint
random_next(void)
{
  uint x = rand_state;
  x ^= x << 13;
  x ^= x >> 17;
  x ^= x << 5;
  rand_state = x;
  return x;
}

// ===== trap.c =====  (unchanged: the timer yield() makes a new lottery every tick)

// ===== sysproc.c =====  (add at the end)
int
sys_settickets(void)
{
  int tickets;

  if(argint(0, &tickets) < 0)
    return -1;
  if(tickets < 1 || tickets > 1000000)  // bound the sum across NPROC entries
    return -1;
  myproc()->tickets = tickets;
  return 0;
}

// ===== syscall.h =====  (next free number: 22 in clean xv6)
#define SYS_settickets 22

// ===== syscall.c =====
extern int sys_settickets(void);           // with the other externs
[SYS_settickets] sys_settickets,           // last entry in syscalls[]

// ===== user.h =====
int settickets(int);

// ===== usys.S =====
// SYSCALL(settickets)

// ===== Makefile =====  (UPROGS)
// 	_lotterytest\

// ===== lotterytest.c =====  (new file)
#include "types.h"
#include "stat.h"
#include "user.h"

#define DURATION 3000          // ticks (100 ticks = 1 second): longer run = closer to 4:1

void
work(int tickets, int end)
{
  int i;
  volatile uint count = 0;
  int rounds = 0;

  settickets(tickets);
  while(uptime() < end){
    for(i = 0; i < 10000; i++)
      count++;
    rounds++;
  }
  if(tickets == 10)
    sleep(5);                   // stagger output after the timed work
  printf(1, "%d tickets: %d rounds\n", tickets, rounds);
  exit();
}

int
main(void)
{
  int end = uptime() + DURATION;
  int first = fork();
  if(first == 0)
    work(40, end);
  int second = fork();
  if(second == 0)
    work(10, end);

  if(first < 0 || second < 0)
    printf(1, "fork failed\n");
  if(first > 0)
    wait();
  if(second > 0)
    wait();
  exit();
}
