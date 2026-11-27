/*

Distributed Matrix Multiplier Using Worker Processes
Concept: Parallel computation, non-overlapping memory partition access.

API: System V (shmget, shmat) or POSIX Shared Memory (shm_open, mmap) + fork() / waitpid().

Problem Statement:

Multiply two large $N \times N$ matrices ($A$ and $B$) using $K$ independent worker processes. The parent process allocates shared memory for Matrix $A$, Matrix $B$, and the resulting Matrix $C$. The parent forks $K$ children, assigning row slices of $C$ to each worker.

The parent forks $K$ worker child processes. Each child is assigned a distinct slice of rows of Matrix $C$ to compute:
𝐶[𝑖][𝑗]=∑𝑘=0𝑁−1𝐴[𝑖][𝑘]⋅𝐵[𝑘][𝑗]
Because each worker writes to a mutually exclusive row partition of Matrix $C$, computations can proceed concurrently without locks or semaphores.

The parent waits for all $K$ children to terminate, verifies the product matrix $C$, and cleans up all shared memory resources.

Initialization & Verification:

Initialize Matrix $A$ with all elements set to 1.0.

Initialize Matrix $B$ as an Identity Matrix ($B[i][j] = 1.0$ if $i == j$, else $0.0$).

Verification Rule: Since $C = A \times I = A$, every element in $C$ should evaluate to 1.0.

If every element in $C$ equals 1.0, print: Verification: SUCCESS or Verification: FAILED

*/

#include <stdio.h>
#include <unistd.h>
#include <sys/shm.h>
#include <sys/wait.h>

int main() {
    int n, k;
    printf("Enter n and k: ");
    scanf("%d %d", &n, &k);
    
    int s = n*n*sizeof(double);
    int sa = shmget(IPC_PRIVATE, s, 0666 | IPC_CREAT);
    int sb = shmget(IPC_PRIVATE, s, 0666 | IPC_CREAT);
    int sc = shmget(IPC_PRIVATE, s, 0666 | IPC_CREAT);

    double *A = shmat(sa, 0, 0);
    double *B = shmat(sb, 0, 0);
    double *C = shmat(sc, 0, 0);

    for (int i = 0; i < n; i++)
        for (int j=0;j<n;j++) {
            A[i*n+j] = 1.0;
            B[i*n+j] = (i==j) ? 1.0 : 0.0;
        }

    for (int w = 0; w < k; w++) {
        if (fork() == 0) {
            int start = w*n/k;
            int end = (w+1)*n/k;

            printf("Worker %d: rows %d to %d\n", w+1, start, end-1);

            for (int i = start; i < end; i++)
                for (int j = 0; j < n; j++) {
                    C[i*n+j] = 0;
                    for (int o = 0; o < n; o++)
                        C[i*n+j] += A[i*n+o] * B[o*n+j];
                }
            return 0;
        }
    }
    
    for (int w = 0; w < k; w++) wait(NULL);
    
    int ok=1;
    for (int i=0;i<n;i++)
        for (int j = 0; j < n; j++)
            if (C[i*n+j] != 1.0) ok = 0;
            
    printf("All workers finished.\n");
    printf("Verification: %s\n", ok ? "SUCCESS" : "FAILED");

    shmdt(A);
    shmdt(B);
    shmdt(C);
    shmctl(sa, IPC_RMID, 0);
    shmctl(sb, IPC_RMID, 0);
    shmctl(sc, IPC_RMID, 0);
    return 0;
}
