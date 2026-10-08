#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main()
{
    long N;
    int threads;

    printf("Enter vector size: ");
    scanf("%ld", &N);

    printf("Enter number of threads: ");
    scanf("%d", &threads);

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

    omp_set_num_threads(threads);

    double start = omp_get_wtime();

    #pragma omp parallel for
    for (long i = 0; i < N; i++)
    {
        C[i] = A[i] * B[i];
    }

    double end = omp_get_wtime();

    printf("Vector size = %ld\n", N);
    printf("Threads = %d\n", threads);
    printf("Execution time = %.6f seconds\n", end - start);
    printf("Verification C[0] = %.2f\n", C[0]);
    printf("Verification C[N-1] = %.2f\n", C[N - 1]);

    free(A);
    free(B);
    free(C);

    return 0;
}
