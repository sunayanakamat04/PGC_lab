# Parallel Computing Laboratory

## Sequential and OpenMP Matrix Multiplication

This repository contains the implementation and performance analysis of matrix multiplication using sequential execution and OpenMP-based shared-memory parallelism.

The experiments use the same 4000 × 4000 matrix multiplication problem to provide a consistent basis for performance comparison.

---

## Experiments

| Experiment | Implementation | Description |
|---|---|---|
| [Experiment 1 — Sequential](./Experiment-1-Sequential/) | Sequential C | Matrix multiplication using a single execution flow |
| [Experiment 2 — OpenMP](./Experiment-2-OpenMP/) | OpenMP | Matrix multiplication using multiple CPU threads |

---

# Experiment 1 — Sequential Matrix Multiplication

## Objective

To implement matrix multiplication using sequential execution and measure the execution time as a baseline for evaluating parallel implementations.

## Methodology

For each element of the result matrix `C`, the dot product of the corresponding row of matrix `A` and column of matrix `B` is calculated.

```text
C[i][j] = Σ A[i][k] × B[k][j]
           k=0 to N-1
```

### Execution Model

```text
Matrix A ──┐
           ├──> Sequential Computation ──> Matrix C
Matrix B ──┘
```

## Configuration

| Parameter | Value |
|---|---|
| Matrix Size | 4000 × 4000 |
| Matrix Initialization | 1.0 |
| Execution Model | Sequential |
| Verification | `C[0][0] = 4000.00` |

## Reference Performance

| Metric | Result |
|---|---:|
| Execution Time | 244.120000 s |
| Verification | 4000.00 |

---

# Experiment 2 — OpenMP Matrix Multiplication

## Objective

To parallelize matrix multiplication using OpenMP shared-memory parallelism and evaluate the performance improvement relative to the sequential implementation.

## Methodology

OpenMP distributes iterations of the matrix multiplication loop across multiple CPU threads operating on shared memory.

The primary OpenMP directive is:

```c
#pragma omp parallel for
```

### Execution Model

```text
                         Matrix Multiplication
                                  |
             ┌────────────────────┼────────────────────┐
             ↓                    ↓                    ↓
         Thread 1             Thread 2             Thread 3   ...
             └────────────────────┼────────────────────┘
                                  ↓
                              Matrix C
```

## Configuration

| Parameter | Value |
|---|---|
| Matrix Size | 4000 × 4000 |
| Reference Thread Count | 8 |
| Execution Model | Shared-memory parallelism |
| Verification | `C[0][0] = 4000.00` |

## Reference Performance

| Metric | Result |
|---|---:|
| Execution Time | 30.830434 s |
| Verification | 4000.00 |
| Speedup | 7.92× |

---

# Performance Analysis

## Execution Time Comparison

The following graph compares the reference execution times for the sequential and OpenMP implementations.

```text
Execution Time (seconds)

250 | ██████████████████████████████████████████████
    | █
200 | █
    | █
150 | █
    | █
100 | █
    | █
 50 | █                         ██████
    | █                         ██████
  0 +------------------------------------------------
          Sequential              OpenMP

          244.12 s               30.83 s
```

### Numerical Comparison

| Implementation | Execution Time (s) |
|---|---:|
| Sequential | 244.120000 |
| OpenMP | 30.830434 |

The reference OpenMP implementation requires substantially less execution time than the sequential implementation for the same matrix multiplication workload.

---

## Speedup Comparison

Speedup is calculated relative to the sequential implementation.

```text
Speedup (×)

8 |                              ████████████████████████████████████████
7 |                              ████████████████████████████████████████
6 |                              ████████████████████████████████████████
5 |                              ████████████████████████████████████████
4 |                              ████████████████████████████████████████
3 |                              ████████████████████████████████████████
2 |                              ████████████████████████████████████████
1 | █████                        ████████████████████████████████████████
0 +----------------------------------------------------------------------
      Sequential                         OpenMP

        1.00×                              7.92×
```

### Speedup Calculation

```text
Speedup = Sequential Execution Time / OpenMP Execution Time

        = 244.120000 / 30.830434

        ≈ 7.92×
```

---

# Overall Performance Comparison

| Parameter | Sequential | OpenMP |
|---|---:|---:|
| Matrix Size | 4000 × 4000 | 4000 × 4000 |
| Execution Model | Sequential | Parallel |
| Thread Count | Single execution flow | 8 |
| Memory Model | Sequential execution | Shared memory |
| Execution Time | 244.120000 s | 30.830434 s |
| Verification | 4000.00 | 4000.00 |
| Relative Speedup | 1.00× | 7.92× |

---

# Execution Model Comparison

## Sequential Execution

The complete computation is handled by a single execution flow.

```text
Input Matrices
      |
      v
Sequential Computation
      |
      v
Result Matrix
```

## OpenMP Execution

The computational workload is distributed among multiple threads.

```text
                    Input Matrices
                          |
                          v
                 Parallel Region
                          |
          ┌───────────────┼───────────────┐
          v               v               v
      Thread 1        Thread 2        Thread 3 ...
          └───────────────┼───────────────┘
                          |
                          v
                    Result Matrix
```

---

# Verification

Both implementations use the same matrix initialization and must produce:

```text
C[0][0] = 4000.00
```

This provides a basic correctness check for the matrix multiplication result.

---

# Compilation and Execution

## Sequential Implementation

For Linux/WSL:

```bash
gcc -O2 matrix_sequential.c -o matrix_sequential
./matrix_sequential
```

For the current Windows file `mat.c`:

```powershell
gcc -O2 mat.c -o mat.exe
.\mat.exe
```

## OpenMP Implementation

On an environment with OpenMP support:

```bash
export OMP_NUM_THREADS=8
gcc -O2 -fopenmp mat_openmp.c -o mat_openmp
./mat_openmp
```

---

# Repository Structure

```text
PGC_lab/
│
├── Experiment-1-Sequential/
│   ├── mat.c
│   └── screenshots/
│
├── Experiment-2-OpenMP/
│   ├── mat_openmp.c
│   └── screenshots/
│
└── README.md
```

---

# Technologies

- C
- GCC
- OpenMP
- Git
- GitHub
- Windows / Linux execution environments

---

# Conclusion

The experiments demonstrate the performance difference between sequential and shared-memory parallel execution for a 4000 × 4000 matrix multiplication workload.

The sequential implementation provides the baseline execution time of 244.120000 seconds, while the reference OpenMP implementation completes the same workload in 30.830434 seconds using 8 threads.

Based on these reference measurements:

```text
Speedup ≈ 7.92×
```

The results demonstrate how OpenMP can exploit multiple CPU threads to reduce execution time for computationally intensive workloads.

> Note: The performance values documented above are reference values. Actual execution times may vary depending on processor architecture, compiler, operating system, thread scheduling, and system load.
