/*
Write a C program that creates a pipe and then uses fork() to create a child process; 
the parent process should write the string "Hello, Child!" into the pipe, 
while the child process reads that message from the pipe and 
prints it to the screen in the format "Child received: Hello, Child!" — remembering that since only one-way communication 
is needed (parent to child), each process should close the pipe end it doesn't use.
*/

#include<stdio.h>
#include<unistd.h>
#include<string.h>
#include<sys/wait.h>

int main(){
    char buffer[100];
    int fd[2];
    
    pipe(fd);
    int pid=fork();
    
    if(pid>0){
        close(fd[0]);
        write(fd[1],"Hello, Child!",13);
        close(fd[1]);
        wait(NULL);
    }
    else{
        close(fd[1]);
        read(fd[0],buffer,sizeof(buffer));
        printf("Child received: %s\n",buffer);
        close(fd[0]);
    }
    
    return 0;
}