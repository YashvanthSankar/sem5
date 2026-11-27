#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
/*
Since the parent never calls wait(), the child remains a zombie for the entire 60-second sleep. Only when the parent process finally terminates does init/systemd (PID 1) inherit and reap the zombie.

Key exam-style points to remember:

A zombie = process that has called exit() but whose parent hasn't called wait() yet (entry still occupies the process table).
An orphan = process whose parent exited before it did; it gets reparented to init (PID 1), which automatically reaps it.
wait()/waitpid() is what removes a zombie by collecting its exit status.
Zombies consume a process table slot (not memory/CPU), but too many can exhaust the PID table.
*/
int main()
{
    pid_t pid = fork();

    if (pid == 0) {
        exit(0);           // Child exits immediately
    } else {
        printf("Parent PID %d, Child PID %d\n", getpid(), pid);
        sleep(60);          // Parent never calls wait() -> child stays zombie
                             // until parent itself exits
    }
    return 0;
}
