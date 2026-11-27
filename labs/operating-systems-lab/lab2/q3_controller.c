// CS24I1029
// YASHVANTH S

#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() 
{
    pid_t pid1, pid2;
    pid1 = fork();

    if (pid1 == 0){
        execl("./calc_worker", "calc_worker","60", "+", "40", (char *)NULL);
        printf("Failed to run calc_worker\n");
        return 1;
    }

    pid2 = fork();

    if (pid2 == 0){
        execl("./calc_worker", "calc_worker","100", "*", "16", (char *)NULL);
        printf("Failed to run calc_worker\n");
        return 1;
    }

    waitpid(pid1, NULL, 0);
    waitpid(pid2, NULL, 0);

    printf("Both calculations completed.\n");

    return 0;
}

