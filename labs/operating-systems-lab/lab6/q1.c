// CS24I1029
// YASHVANTH S

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define SIZE 8          // queue capacity
#define PRODUCERS 3
#define PRINTERS 2
#define JOBS_EACH 10
#define TOTAL (PRODUCERS * JOBS_EACH)   // 30

typedef struct { int id, producer, priority; } Job;

Job q[SIZE];
int n;

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
sem_t empty;            // free slots   (starts at SIZE) -> producer blocks when queue is full
sem_t full;             // queued jobs  (starts at 0)    -> printer blocks when queue is empty

void *producer(void *arg)
{
    int p = *(int *)arg;
    unsigned int seed = p;  // each producer has its own random sequence

    for (int i = 1; i <= JOBS_EACH; i++) {
        Job j = {(p - 1) * JOBS_EACH + i, p, rand_r(&seed) % 2};

        sem_wait(&empty);               // wait for a free slot (never add to a full queue)
        pthread_mutex_lock(&mutex);

        q[n++] = j;
        printf("Terminal %d -> Job %d (%s), queue = %d\n",
               p, j.id, j.priority ? "priority" : "normal", n);

        pthread_mutex_unlock(&mutex);
        sem_post(&full);                // one more job available

        usleep((rand_r(&seed) % 5 + 1) * 100000);   // random delay 0.1 - 0.5 s
    }
    return NULL;
}

void *printer(void *arg)
{
    int pr = *(int *)arg;

    while (1) {
        sem_wait(&full);                // wait for a job (never remove from an empty queue)
        pthread_mutex_lock(&mutex);

        if (n == 0) {  // shutdown wake-up
            pthread_mutex_unlock(&mutex);
            break;
        }

        // pick the oldest priority job; if there is none, the oldest normal job (index 0)
        int pos = 0;
        for (int i = 0; i < n; i++) {
            if (q[i].priority) { pos = i; break; }
        }

        Job j = q[pos];
        for (int i = pos; i < n - 1; i++) q[i] = q[i + 1];   // close the gap
        n--;
        printf("Printer %d <- Job %d from Terminal %d (%s), queue = %d\n",
               pr, j.id, j.producer, j.priority ? "priority" : "normal", n);

        pthread_mutex_unlock(&mutex);
        sem_post(&empty);               // one more free slot

        usleep(300000);  // printing time
    }
    printf("Printer %d finished\n", pr);
    return NULL;
}

int main(void)
{
    pthread_t p[PRODUCERS], pr[PRINTERS];
    int ids[PRODUCERS] = {1, 2, 3};
    sem_init(&empty, 0, SIZE);
    sem_init(&full, 0, 0);

    for (int i = 0; i < PRODUCERS; i++)
        pthread_create(&p[i], NULL, producer, &ids[i]);
    for (int i = 0; i < PRINTERS; i++)
        pthread_create(&pr[i], NULL, printer, &ids[i]);

    for (int i = 0; i < PRODUCERS; i++) pthread_join(p[i], NULL);
    for (int i = 0; i < PRINTERS; i++)
        sem_post(&full);                // one exit wake-up per printer

    for (int i = 0; i < PRINTERS; i++)  pthread_join(pr[i], NULL);

    printf("All %d jobs completed. Final queue = %d\n", TOTAL, n);

    sem_destroy(&empty);
    sem_destroy(&full);
    pthread_mutex_destroy(&mutex);
    return 0;
}
