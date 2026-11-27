// CS24I1029
// YASHVANTH S

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define STUDENTS 6
#define PRINTERS 3

sem_t printer_sem;   // counting semaphore: value = number of free printers

void *student(void *args)
{
    int id = *(int *)args;

    printf("Student %d waiting...\n", id);
    sem_wait(&printer_sem);                 // value > 0: take a printer; value == 0: block
    printf("Student %d acquired a printer\n", id);
    sleep(2);                               // printing
    printf("Student %d released the printer\n", id);
    sem_post(&printer_sem);                 // give the printer back, wakes one waiting student
    return NULL;
}

int main(void)
{
    pthread_t students[STUDENTS];
    int id[STUDENTS];

    sem_init(&printer_sem, 0, PRINTERS);    // 0 = shared between threads of this process; 3 printers
    printf("Available printers = %d\n", PRINTERS);

    for (int i = 0; i < STUDENTS; i++) {
        id[i] = i + 1;                      // each thread gets its OWN id variable
        pthread_create(&students[i], NULL, student, &id[i]);
    }

    for (int i = 0; i < STUDENTS; i++)
        pthread_join(students[i], NULL);

    sem_destroy(&printer_sem);              // only after every thread has finished
    return 0;
}
