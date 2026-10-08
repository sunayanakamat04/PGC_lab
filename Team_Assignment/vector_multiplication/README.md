# Parallel Vector Multiplication using OpenMP

## 1. Experiment Title

**Parallel Vector Multiplication using OpenMP**

## 2. Objective

To implement element-wise vector multiplication sequentially and in parallel using OpenMP, and compare their execution performance for different vector sizes and numbers of threads.

The experiment evaluates:

* Execution time
* Parallel speedup
* Parallel efficiency
* Effect of vector size on parallel performance
* Effect of increasing the number of OpenMP threads

---

## 3. Problem Definition

Given two input vectors `A` and `B` of equal size `N`, compute the output vector `C` using element-wise multiplication:

`C[i] = A[i] × B[i]`

for every element:

`0 ≤ i < N`

The sequential implementation processes the elements one at a time, while the OpenMP implementation distributes the independent vector multiplication operations across multiple CPU threads.

---

## 4. Parallel Design

The vector multiplication operation is highly parallel because each output element can be calculated independently.

The OpenMP implementation uses:

```c
#pragma omp parallel for
```

to divide the loop iterations among multiple threads.

No GPU is required for this experiment. The parallel implementation uses the CPU cores available on the laptop through OpenMP.

---

## 5. Hardware / Environment

### Processor

**13th Gen Intel(R) Core(TM) i5-13400**

### CPU Threads

**16 logical CPUs**

### Operating Environment

* Ubuntu through WSL
* GCC compiler
* OpenMP
* Python 3
* Matplotlib

---

## 6. Repository Structure

```text
vector_multiplication/
│
├── README.md
│
├── src/
│   ├── vector_mul_seq.c
│   └── vector_mul_omp.c
│
├── data/
│
├── results/
│   └── results.csv
│
├── graphs/
│   ├── execution_time.png
│   ├── speedup.png
│   └── efficiency.png
│
├── report/
│
└── generate_graphs.py
```

---

## 7. Compilation and Execution

### Sequential Version

Compile:

```bash
gcc -O2 src/vector_mul_seq.c -o vector_mul_seq
```

Run:

```bash
./vector_mul_seq
```

The program asks for the vector size.

### OpenMP Version

Compile:

```bash
gcc -O2 -fopenmp src/vector_mul_omp.c -o vector_mul_omp
```

Run:

```bash
./vector_mul_omp
```

The program asks for:

1. Vector size
2. Number of threads

---

## 8. Experimental Configuration

Three vector sizes were tested:

* 1,000,000 elements
* 10,000,000 elements
* 50,000,000 elements

Five OpenMP thread counts were tested:

* 1
* 2
* 4
* 6
* 16

This produced a total of **15 OpenMP performance measurements**.

Each run was verified by checking:

```text
C[0] = 6.00
C[N-1] = 6.00
```

---

## 9. Performance Results

### Sequential Baseline

| Vector Size | Sequential Time (s) |
| ----------: | ------------------: |
|   1,000,000 |            0.007267 |
|  10,000,000 |            0.023113 |
|  50,000,000 |            0.127989 |

### OpenMP Execution Time

| Vector Size | 1 Thread | 2 Threads | 4 Threads | 6 Threads | 16 Threads |
| ----------: | -------: | --------: | --------: | --------: | ---------: |
|   1,000,000 | 0.005523 |  0.006204 |  0.003895 |  0.006700 |   0.004731 |
|  10,000,000 | 0.030223 |  0.013761 |  0.011840 |  0.014404 |   0.011540 |
|  50,000,000 | 0.129369 |  0.084077 |  0.067768 |  0.071014 |   0.040625 |

The complete raw results are stored in:

```text
results/results.csv
```

---

## 10. Speedup

Speedup is calculated using:

```text
Speedup = Sequential Execution Time / Parallel Execution Time
```

For the 50,000,000-element vector with 16 threads:

```text
Speedup = 0.127989 / 0.040625
        ≈ 3.15×
```

The maximum measured speedup in this experiment was approximately **3.15×**.

---

## 11. Efficiency

Parallel efficiency is calculated as:

```text
Efficiency = (Speedup / Number of Threads) × 100
```

For the 50,000,000-element vector using 16 threads:

```text
Efficiency = (3.1505 / 16) × 100
           ≈ 19.69%
```

---

## 12. Performance Analysis

The results show that increasing the vector size generally makes parallelization more beneficial because there is more computational work to distribute among the threads.

The 50,000,000-element workload demonstrated the clearest improvement. Its sequential execution time was **0.127989 seconds**, while the 16-thread OpenMP implementation completed in **0.040625 seconds**, producing approximately **3.15× speedup**.

The scaling is not perfectly linear. Increasing the number of threads does not always reduce execution time. For example, for the 10,000,000-element vector, the execution time increased from **0.011840 seconds with 4 threads** to **0.014404 seconds with 6 threads**.

This behavior demonstrates that parallel performance is affected by factors such as thread-management overhead and memory-access limitations. For smaller workloads, these overheads can become significant compared with the actual computation.

Efficiency also decreases at higher thread counts. For the 50,000,000-element workload, efficiency was approximately **76.11% with 2 threads**, **47.22% with 4 threads**, **30.04% with 6 threads**, and **19.69% with 16 threads**.

Therefore, adding more threads does not guarantee proportional performance improvement. The available workload, CPU resources, memory subsystem, and parallel overhead all influence the final performance.

---

## 13. Generated Graphs

The following graphs are included in the `graphs/` directory:

### Execution Time

`graphs/execution_time.png`

Shows the relationship between the number of OpenMP threads and execution time for each vector size.

### Speedup

`graphs/speedup.png`

Shows the speedup achieved by the OpenMP implementation relative to the sequential baseline.

### Efficiency

`graphs/efficiency.png`

Shows the percentage efficiency of parallel execution at different thread counts.

---

## 14. Conclusion

The experiment demonstrates that element-wise vector multiplication can be effectively parallelized using OpenMP because individual vector elements can be computed independently.

The performance benefit becomes more visible as the workload increases. The largest tested workload, 50,000,000 elements, achieved approximately **3.15× speedup using 16 threads** compared with the sequential implementation.

However, the results also demonstrate that parallel scaling is not perfectly linear. Increasing the number of threads introduces overhead and can result in diminishing efficiency.

Overall, the experiment provides a practical comparison between sequential and CPU-based OpenMP vector multiplication and demonstrates the relationship between workload size, thread count, execution time, speedup, and efficiency.
