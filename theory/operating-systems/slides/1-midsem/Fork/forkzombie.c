#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
/*fork() creates a child process.
The child prints its message and immediately calls exit(0).
When a child exits, it doesn't disappear right away — the kernel keeps its exit status in the process table entry until the parent calls wait()/waitpid(). During this time, the child is a zombie
(state Z, shown as <defunct> in ps).
Here the parent is stuck in sleep(20), so it hasn't called wait() yet — the child remains a zombie for those 20 seconds.
While the program is sleeping, open another terminal and run:
   ps -l
or
   ps aux | grep defunct

You'll see the child listed with status Z (zombie).
6. After sleep(20) ends, wait(NULL) reaps the child, removing its entry from the process table.*/
int main()
{
    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        printf("Child (PID %d) running, exiting now...\n", getpid());
        exit(0);   // Child terminates immediately
    }
    else {
        // Parent process
        printf("Parent (PID %d), child PID = %d\n", getpid(), pid);
        printf("Parent sleeping for 20 seconds... check 'ps -l' now!\n");
        sleep(20);   // Parent delays calling wait(), so child stays a zombie
        wait(NULL);  // Finally reaps the child
        printf("Parent reaped the child. No more zombie.\n");
    }

    return 0;
}
