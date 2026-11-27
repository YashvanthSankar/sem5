#include<stdio.h>
#include<unistd.h>
#include<sys/wait.h>

int main(int argc, char *argv[]){
    if(argc!=3){
        printf("Usage: %s <source_file> <backup_file>\n", argv[0]);
        return 1;
    }
    pid_t pid =fork();
    
    if(pid<0){
        printf("Fork failed.\n");
    }
    else if(pid==0){
        printf("Child process: Copying the file\n");
        
        execl("/bin/cp", "cp", argv[1], argv[2], (char *) NULL);
        
        printf("Child process: Copy failed\n");
        return 1;
    }
    else{
        printf("Parent process: My child is copying the file. I'm doing other work\n");
        
        wait(NULL);
        
        printf("Parent process: Backup completed\n");
    }
    
    return 0;
}
