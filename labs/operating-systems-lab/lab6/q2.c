// CS24I1029
// YASHVANTH S

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <sys/time.h>

#define N 7
#define MEALS 5

sem_t chop[N];          // one binary semaphore per chopstick
sem_t sauce;            // counting semaphore: at most 2 philosophers use the sauce at once
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;   // protects the fairness variables below

int since[2][N];    // since[k][p] = normal p's meal starts since hungry k last started
int hungry_meals[2];  // meals started by each hungry philosopher

int meals[N];
double maxwait[N];

struct timeval start;

double time_ms(){
    struct timeval t;
    gettimeofday(&t, NULL);
    return (t.tv_sec - start.tv_sec) * 1000.0 + (t.tv_usec - start.tv_usec) / 1000.0;
}

int is_hungry(int p){ return p < 2; }

void logmsg(int p, const char *msg){
    printf("%.2f ms: Philosopher %d %s\n", time_ms(), p + 1, msg);
}

// Check the meal quota while holding the mutex.
int allowed(int p){
    if (is_hungry(p)) return 1;
    for (int k = 0; k < 2; k++)
        if (hungry_meals[k] < MEALS && since[k][p] >= 2) return 0;
    return 1;
}

void *philosopher(void *arg){
    int p = *(int *)arg;
    int left = p, right = (p + 1) % N;
    int first  = left < right ? left : right;    // resource ordering: lower-numbered chopstick first
    int second = left < right ? right : left;

    for (int m = 0; m < MEALS; m++){
        logmsg(p, "thinking");
        usleep(50000);

        double startwait = time_ms();
        logmsg(p, "waiting");

        // fairness gate (a normal philosopher may wait here; it holds no chopsticks, so no deadlock)
        pthread_mutex_lock(&mutex);
        while (!allowed(p)){
            pthread_mutex_unlock(&mutex);
            usleep(1000);
            pthread_mutex_lock(&mutex);
        }
        pthread_mutex_unlock(&mutex);

        sem_wait(&chop[first]);         // ordered pickup -> no circular wait -> no deadlock
        sem_wait(&chop[second]);

        double wait = time_ms() - startwait;
        if (wait > maxwait[p]) maxwait[p] = wait;    // only this thread writes maxwait[p]

        logmsg(p, "picked both chopsticks");

        sem_wait(&sauce);               // at most 2 at a time; taken while holding both chopsticks
        logmsg(p, "using sauce");
        usleep(50000);
        logmsg(p, "done with sauce");   // logged BEFORE sem_post so the log never shows 3 at the sauce
        sem_post(&sauce);

        pthread_mutex_lock(&mutex);
        if (is_hungry(p)) {
            hungry_meals[p]++;
            for (int j = 2; j < N; j++)
                since[p][j] = 0;
        } else {
            since[0][p]++;
            since[1][p]++;
        }
        logmsg(p, "eating");
        pthread_mutex_unlock(&mutex);
        usleep(70000);
        meals[p]++;

        logmsg(p, "releasing both chopsticks");   // logged BEFORE sem_post, so a neighbour's "picked"
        sem_post(&chop[second]);                    // can never appear in the log before this line
        sem_post(&chop[first]);
    }
    return NULL;
}

int main(void){
    pthread_t t[N];
    int id[N];

    gettimeofday(&start, NULL);

    for (int i = 0; i < N; i++) sem_init(&chop[i], 0, 1);
    sem_init(&sauce, 0, 2);

    for (int i = 0; i < N; i++){
        id[i] = i;
        pthread_create(&t[i], NULL, philosopher, &id[i]);
    }
    for (int i = 0; i < N; i++) pthread_join(t[i], NULL);

    for (int i = 0; i < N; i++)
        printf("Philosopher %d: %d meals, max wait %.2f ms\n", i + 1, meals[i], maxwait[i]);

    for (int i = 0; i < N; i++) sem_destroy(&chop[i]);
    sem_destroy(&sauce);
    pthread_mutex_destroy(&mutex);
    return 0;
}
