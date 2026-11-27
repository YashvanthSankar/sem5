#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
/*fork() creates a child process that is initially an exact copy of the parent (same code, same memory image, same open file descriptors).
In the child (pid == 0), we call execlp("ls", "ls", "-l", NULL).
exec replaces the child's entire memory image (code, data, stack, heap) with the new program (ls).
The child's PID stays the same, but everything else about the process is overwritten.
Because of this replacement, any code written after a successful exec() call never executes — the process is now running ls, not your C program anymore.
If exec() fails (e.g., ls isn't found), it returns -1, and execution continues with the line right after it — this is the only case where the printf after execlp would run.
In the parent, wait(NULL) blocks until the child finishes running ls, then the parent resumes and prints its final message.*/
int main()
{
    pid_t pid = fork();

    if (pid < 0) {
        // fork failed
        perror("fork failed");
        exit(1);
    }
    else if (pid == 0) {
        // Child process
        printf("Child (PID %d) before exec\n", getpid());

        execlp("ls", "ls", "-l", NULL);   // Replace child's image with 'ls -l'

        // This line only runs if execlp() FAILS
        printf("This will never print if exec succeeds\n");
        exit(1);
    }
    else {
        // Parent process
        printf("Parent (PID %d), child PID = %d\n", getpid(), pid);
        wait(NULL);   // Wait for child to finish
        printf("Child terminated, parent resuming\n");
    }

    return 0;
}
