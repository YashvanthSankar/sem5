/*Write a C program to create less than 16 processes using 4 fork() calls also display the PID of each process.*/

#include <stdio.h>
#include <unistd.h>

int main()
{
    fork();
    fork();
    if (fork() == 0)
        fork();

    printf("PID: %d\n", getpid());

    return 0;
}