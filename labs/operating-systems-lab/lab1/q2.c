/*Using exactly three fork() system calls, write a C program to create 8 processes also display the PID of each process.*/

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main()
{
    fork();
    fork();
    fork();

    printf("Process PID: %d\n", getpid());

    return 0;
}