#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double get_time()
{
    struct timespec ts;

    clock_gettime(CLOCK_MONOTONIC, &ts);

    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main()
{
    long N;

    printf("Enter vector size: ");
    scanf("%ld", &N);

    float *A = malloc(N * sizeof(float));
    float *B = malloc(N * sizeof(float));
    float *C = malloc(N * sizeof(float));

    if (A == NULL || B == NULL || C == NULL)
    {
        printf("Memory allocation failed\n");
        return 1;
    }

    for (long i = 0; i < N; i++)
    {
        A[i] = 2.0f;
        B[i] = 3.0f;
    }

    double start = get_time();

    for (long i = 0; i < N; i++)
    {
        C[i] = A[i] * B[i];
    }

    double end = get_time();

    printf("Vector size = %ld\n", N);
    printf("Execution time = %.6f seconds\n", end - start);
    printf("Verification C[0] = %.2f\n", C[0]);
    printf("Verification C[N-1] = %.2f\n", C[N - 1]);

    free(A);
    free(B);
    free(C);

    return 0;
}
