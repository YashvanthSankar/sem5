/*
Create a child process that prints its PID and exits immediately. In the parent, sleep for 10 seconds without calling wait(), 
then run ps to show the child is now a zombie (Z state). After the sleep, call wait() and show the zombie disappears.
*/

#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    pid_t pid = fork();
    
    if(pid == 0){
        printf("child PID: %d\n", getpid());
        printf("child process exited now\n");
        exit(0);
    }
    else{
        printf("parent PID: %d\n", getpid());
        printf("parent sleeping for 10 seconds...\n");
        sleep(10);
        printf("calling wait()...\n");
        wait(NULL);
        printf("zombie disappeared.\n");
    }
    
    return 0;
}


