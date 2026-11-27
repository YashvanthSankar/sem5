// ===== syscall.h =====   (after #define SYS_close 21)
#define SYS_process_info 22

// ===== user.h =====
int process_info(int option);

// ===== usys.S =====
// SYSCALL(process_info)

// ===== syscall.c =====
extern int sys_process_info(void);          // with the other externs
// [SYS_process_info]  sys_process_info,    // inside the syscalls[] table

// ===== sysproc.c =====
int
sys_process_info(void)
{
  int option, diff, ppid;
  struct proc *p = myproc();

  if(argint(0, &option) < 0)
    return -1;
  if(option == 0)
    return p->pid;
  if((option != 1 && option != 2) || p->parent == 0)
    return -1;

  ppid = p->parent->pid;
  if(option == 1)
    return ppid;
  diff = p->pid - ppid;
  return diff < 0 ? -diff : diff;
}

// ===== Makefile =====
// UPROGS: add  _process_info_test\

// ===== process_info_test.c =====
#include "types.h"
#include "user.h"

int
main(void)
{
  printf(1, "PID: %d\n", process_info(0));
  printf(1, "Parent PID: %d\n", process_info(1));
  printf(1, "PID Difference: %d\n", process_info(2));
  printf(1, "Invalid: %d\n", process_info(5));
  exit();
}
