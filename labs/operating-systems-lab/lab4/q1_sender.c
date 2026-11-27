#include<stdio.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/mman.h>
#include<string.h>

#define SIZE 256


int main(){
    char buffer[100];
    
    int fd = shm_open("/lab_shm_basic",O_CREAT | O_RDWR, 0666);
    
    ftruncate(fd,SIZE);
    
    char *ptr = mmap(NULL,SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    
    printf("Enter a line of text: ");
    fgets(buffer,sizeof(buffer),stdin);
    strcpy(ptr,buffer);
    printf("Successfully written to the buffer.\n");
    
    printf("Press Enter to exit...");
    getchar();
    
    munmap(ptr,SIZE);
    close(fd);
    
    return 0;
}
