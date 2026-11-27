/*
Write a program where a child is created from a parent and a child waits 
for a parent to end. As soon as the parent ends child prints the dead parents id and also new parants id without sleep.

*/

// CS24I1029
// YASHVANTH S

#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

int main(){
    pid_t pid=fork();
    
    if(pid<0){
        printf("Fork failed\n");
    }
    else if(pid>0){
        printf("Parent's PID: %d\n", getpid());
        printf("Parent is going to die...\n");
        exit(0);
    }
    else{
        pid_t dead_ppid=getppid();
        while(getppid()==dead_ppid){
            // checking for change in ppid
        }
        
        printf("Dead parent's PID: %d\n", dead_ppid);
        printf("New parent's PID: %d\n", getppid());   
    }
}