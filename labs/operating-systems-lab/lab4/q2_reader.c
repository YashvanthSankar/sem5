#include<stdio.h>
#include<stdlib.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include<sys/types.h>

int main(){
    int key = ftok(".",'B');
    int shmid = shmget(key, sizeof(int), 0666);
    int *ptr = (int *)shmat(shmid, NULL, 0);

    printf("ipc key: %d\n", key);
    printf("shared memory id: %d\n", shmid);
    printf("attached address: %p\n", (void *)ptr);
    printf("read value: %d\n", *ptr);
    
    printf("shared memory segment marked for removal.\n");
    shmdt(ptr);
    shmctl(shmid, IPC_RMID, NULL);
    
    return 0;
}
