// CS24I1029
// YASHVANTH S

#include <stdio.h>
#include <pthread.h>

int balance = 10000;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *transact(void *arg)
{
    int amount = *(int *)arg;
    for (int i = 0; i < 5; i++) {
        pthread_mutex_lock(&lock);
        balance += amount;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void)
{
    pthread_t threads[3];
    int amounts[] = {2000, -1000, 500};

    for (int i = 0; i < 3; i++)
        pthread_create(&threads[i], NULL, transact, &amounts[i]);
    for (int i = 0; i < 3; i++)
        pthread_join(threads[i], NULL);

    printf("Final balance = %d\n", balance);
    pthread_mutex_destroy(&lock);
    return 0;
}
