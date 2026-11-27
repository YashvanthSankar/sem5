/*
Use 3 fork() system calls to create 4 processes exactly and 
print the process tree that contains the PID of parent process along with the 3 child processes.
*/

#include<stdio.h>
#include<unistd.h>
#include<sys/wait.h>
#include<sys/types.h>


int main(){
    if(fork()!=0){
        if(fork()!=0){
            fork();
        }
    }
    printf("Process PID: %d\n", getpid());
    
    return 0;
}