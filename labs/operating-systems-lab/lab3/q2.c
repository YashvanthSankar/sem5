/*
Write a C program that simulates a simple calculator worker process using two pipes
for two-way communication, where the parent process sends two integers and an operator (+, -, *, or /) 
to the child (for example, "12 4 +"), the child reads these values,
performs the corresponding arithmetic operation, and sends the result back to the parent, 
which then prints the final output in the format "Result of 12 + 4 = 16"; the program should 
use one pipe for parent-to-child communication and a separate pipe for child-to-parent communication, 
handle division by zero gracefully by having the child send back an error code instead of crashing, 
ensure all unused pipe ends are properly closed in both processes, and use wait() in the parent to avoid leaving a zombie child process.

*/

#include<stdio.h>
#include<unistd.h>
#include<string.h>
#include<sys/wait.h>

int main(){
    char buffer[100];
    int fd1[2], fd2[2];
    int a,b,result,code;
    char op;
    
    pipe(fd1);
    pipe(fd2);
    int pid = fork();
    
    if(pid>0){
        close(fd1[0]);
        close(fd2[1]);
        printf("Enter input (a b op): ");
        scanf("%d %d %c",&a,&b,&op);
        write(fd1[1],&a,sizeof(a));
        write(fd1[1],&b,sizeof(b));
        write(fd1[1],&op,sizeof(op));
        close(fd1[1]);
        
        read(fd2[0],&code,sizeof(code));
        if(code==0){
            read(fd2[0],&result,sizeof(result));
            printf("Result of %d %c %d = %d",a,op,b,result);
        }
        else if(code==-1){
            printf("Error code: %d , Division by 0 is prohibited",code);
        }
        else{
            printf("Error code: %d , Invalid input",code);
        }
        
        close(fd2[0]);
        wait(NULL);
    }
    else{
        close(fd1[1]);
        close(fd2[0]);
        read(fd1[0],&a,sizeof(a));
        read(fd1[0],&b,sizeof(b));
        read(fd1[0],&op,sizeof(op));
        close(fd1[0]);
        
        if (op=='+') result=a+b;
        else if (op=='-') result=a-b;
        else if (op=='*') result=a*b;
        else if (op=='/') {
            if (b==0) code=-1;
            else { result=a/b; code=0; }
        } else code=-2;
        if (op!='/' && (op=='+' || op=='-' || op=='*'))
            code = 0;
            
        write(fd2[1],&code,sizeof(code));
        if(code==0){
            write(fd2[1],&result,sizeof(result));
        }
        
        close(fd2[1]);
    }
    return 0;
}