#include<stdio.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include<stdlib.h>
#include<sys/types.h>

int main(){
    key_t key = ftok(".",'B');
    int shmid = shmget(key, sizeof(int), IPC_CREAT | 0666);
    int *ptr = (int *)shmat(shmid, NULL, 0);
    
    *ptr = 36424;
    
    printf("ipc key: %d\n", key);
    printf("shared memory id: %d\n", shmid);
    printf("attached address : %p\n", (void *)ptr);
    printf("stored value     : %d\n", *ptr);
    
    shmdt(ptr);
    
    return 0;
}
