#include<stdio.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/mman.h>
#include<string.h>

#define SIZE 256

int main(){
    
    int fd = shm_open("/lab_shm_basic", O_RDONLY,0);
    
    char *ptr = mmap(NULL, SIZE, PROT_READ, MAP_SHARED, fd, 0);
    
    printf("Message from the sender: %s", ptr);
    
    printf("Virtual memory address: %p \n", (void *) ptr);
    
    munmap(ptr, SIZE);
    close(fd);
    shm_unlink("/lab_shm_basic");

    return 0;

}
