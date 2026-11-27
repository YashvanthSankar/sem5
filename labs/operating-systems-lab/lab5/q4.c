// CS24I1029
// YASHVANTH S

#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

#define N 1000
#define INITIAL 1000
#define TRANSFERS 20000

typedef struct {
    int balance;
    int frozen;
    pthread_mutex_t lock;       // one lock per account (no global lock)
} Account;

Account accounts[N];

int transfer(int from, int to, int amount)
{
    if (from < 0 || from >= N || to < 0 || to >= N ||
        from == to || amount <= 0)
        return -1;

    // Both transfer directions lock the lower account number first.
    int first = from < to ? from : to;
    int second = from < to ? to : from;
    pthread_mutex_lock(&accounts[first].lock);
    pthread_mutex_lock(&accounts[second].lock);

    Account *source = &accounts[from];
    Account *target = &accounts[to];
    int result = -1;
    if (!source->frozen && !target->frozen && source->balance >= amount) {
        source->balance -= amount;
        target->balance += amount;
        result = 0;
    }

    pthread_mutex_unlock(&accounts[second].lock);
    pthread_mutex_unlock(&accounts[first].lock);
    return result;
}

// Hold all locks while summing so each transfer is seen in full.
int audit_total(void)
{
    int total = 0;

    for (int i = 0; i < N; i++)
        pthread_mutex_lock(&accounts[i].lock);

    for (int i = 0; i < N; i++)
        total += accounts[i].balance;

    for (int i = N - 1; i >= 0; i--)
        pthread_mutex_unlock(&accounts[i].lock);

    return total;
}

void *transfer_worker(void *arg)
{
    unsigned int seed = *(unsigned int *)arg;
    for (int i = 0; i < TRANSFERS; i++) {
        int from = rand_r(&seed) % N;
        int to = rand_r(&seed) % N;
        int amount = rand_r(&seed) % 2000 + 1;
        transfer(from, to, amount);
    }
    return NULL;
}

void *audit_worker(void *arg)
{
    (void)arg;
    for (int i = 0; i < 5; i++) {
        printf("Audit total = %d\n", audit_total());
        usleep(1000);
    }
    return NULL;
}

void *closure_worker(void *arg)
{
    (void)arg;
    unsigned int seed = 3;
    for (int i = 0; i < 5; i++) {
        int id = rand_r(&seed) % N;
        pthread_mutex_lock(&accounts[id].lock);
        accounts[id].frozen = 1;
        pthread_mutex_unlock(&accounts[id].lock);
        printf("Account %d frozen\n", id);
        usleep(1000);
    }
    return NULL;
}

int main(void)
{
    pthread_t threads[4];
    unsigned int seeds[] = {1, 2};

    for (int i = 0; i < N; i++) {
        accounts[i].balance = INITIAL;
        pthread_mutex_init(&accounts[i].lock, NULL);
    }

    pthread_create(&threads[0], NULL, transfer_worker, &seeds[0]);
    pthread_create(&threads[1], NULL, transfer_worker, &seeds[1]);
    pthread_create(&threads[2], NULL, audit_worker, NULL);
    pthread_create(&threads[3], NULL, closure_worker, NULL);

    for (int i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);
    printf("Final total = %d\n", audit_total());

    for (int i = 0; i < N; i++)
        pthread_mutex_destroy(&accounts[i].lock);
    return 0;
}
