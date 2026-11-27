// CS24I1029
// YASHVANTH S

#include <stdio.h>
#include <pthread.h>

#define HALF 5

int sum1, sum2;

int sum_half(const int *marks)
{
    int sum = 0;
    for (int i = 0; i < HALF; i++)
        sum += marks[i];
    return sum;
}

void *first_half(void *arg)
{
    sum1 = sum_half(arg);
    return NULL;
}

void *second_half(void *arg)
{
    sum2 = sum_half(arg);
    return NULL;
}

int main(void)
{
    int marks[2 * HALF] = {97, 85, 98, 54, 23, 45, 78, 27, 67, 76};
    int n = sizeof(marks) / sizeof(marks[0]);
    pthread_t t1, t2;

    pthread_create(&t1, NULL, first_half, marks);
    pthread_create(&t2, NULL, second_half, marks + HALF);

    pthread_join(t1, NULL);   // wait for both threads BEFORE reading their results
    pthread_join(t2, NULL);

    printf("thread 1 sum = %d\n", sum1);
    printf("thread 2 sum = %d\n", sum2);

    int sum = sum1 + sum2;
    float avg = (float)sum / n;

    printf("total sum = %d\n", sum);
    printf("average = %.2f\n", avg);

    return 0;
}
