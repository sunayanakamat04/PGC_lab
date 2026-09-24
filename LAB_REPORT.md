# LABORATORY EXPERIMENT REPORT

**Course Title:** Parallel and Grid Computing (PGC)  
**Experiment Title:** Performance Analysis of Matrix Multiplication using Sequential and OpenMP Paradigms  
**Author / Repository Owner:** `sunayanakamat04`  
**Repository:** `PGC_lab`  
**Date:** September 2026  

---

## 1. Abstract

This laboratory experiment evaluates the performance of dense `4000 × 4000` matrix multiplication using sequential CPU execution and OpenMP shared-memory parallel execution. The sequential implementation was executed using one CPU thread, while the OpenMP implementation used 8 threads. Both implementations produced the verified mathematical result `C[0][0] = 4000.00`.

In the recorded runs, the sequential implementation required **166.734358 seconds**, while the OpenMP implementation required **40.215130 seconds** using 8 threads. Based on these recorded measurements, OpenMP reduced the execution time compared with the sequential baseline. The measured speedup is approximately **4.15×**.

MPI and CUDA source files are included in the repository under `src/`, but verified execution-time measurements for those implementations were not included in the supplied experiment results. Therefore, this report does not claim MPI or CUDA performance values.

---

## 2. Experimental Objectives

1. Implement dense `4000 × 4000` matrix multiplication using a sequential C program and an OpenMP parallel C program.
2. Verify numerical correctness by confirming `C[0][0] = 4000.00`.
3. Measure execution time for the sequential and OpenMP implementations.
4. Calculate the OpenMP speedup relative to the sequential baseline.
5. Compare single-threaded execution with shared-memory multi-threaded execution.
6. Organize the source code, scripts, images, and report in the GitHub repository.

---

## 3. System Architecture and Resource Allocation

| Paradigm | Environment | Compute Units | Memory Architecture | Compiler / Toolchain |
| :--- | :--- | :--- | :--- | :--- |
| **Sequential** | WSL2 Ubuntu | 1 CPU Thread | Shared System RAM | GCC `-O2` |
| **OpenMP** | WSL2 Ubuntu | 8 CPU Threads | Shared System RAM | GCC `-O2 -fopenmp` |
| **MPI** | Source included in repository | Not benchmarked | Distributed Memory | Open MPI |
| **CUDA** | Source included in repository | Not benchmarked | GPU VRAM | NVIDIA `nvcc` |

The sequential implementation performs conventional three-nested-loop matrix multiplication. The OpenMP implementation parallelizes the outer loop using OpenMP directives.

---

## 4. Empirical Data and Benchmarking Results

### 4.1 Performance Summary

| Computing Model | Resources | Execution Time (s) | Speedup vs Sequential | Verification `C[0][0]` |
| :--- | :--- | :---: | :---: | :---: |
| **Sequential Baseline** | 1 CPU Thread | **166.734358** | **1.00×** | **4000.00** |
| **OpenMP Shared Memory** | 8 CPU Threads | **40.215130** | **4.15×** | **4000.00** |
| **MPI Distributed** | Not benchmarked | — | — | — |
| **CUDA GPU** | Not benchmarked | — | — | — |

### 4.2 Speedup Calculation

The speedup is calculated as:

`Speedup = Sequential Time / Parallel Time`

For the recorded OpenMP run:

`Speedup = 166.734358 / 40.215130`

`Speedup ≈ 4.15×`

The recorded 8-thread OpenMP implementation therefore completed the matrix multiplication in approximately one-quarter of the sequential execution time.

---

## 5. Performance Visualizations

Performance images and comparison graphs are maintained in the `image/` directory.

The repository can contain:

- Sequential execution output
- OpenMP execution output
- Sequential verification screenshot
- OpenMP verification screenshot
- Resource-monitor screenshot
- Execution-time comparison graph
- Speedup comparison graph
- Overall performance dashboard

The `script/` directory contains the benchmark automation, result parsing, and graph-generation scripts.

---

## 6. Discussion and Technical Findings

### 6.1 Sequential Execution

The sequential implementation performs matrix multiplication using three nested loops. With a matrix size of `4000 × 4000`, the computation involves a large number of arithmetic operations and memory accesses. The recorded execution time was **166.734358 seconds**.

### 6.2 OpenMP Shared-Memory Execution

The OpenMP implementation parallelizes the outer matrix-multiplication loop. The recorded run used **8 threads** and completed in **40.215130 seconds**.

Compared with the sequential result, this corresponds to approximately **4.15× speedup**.

### 6.3 Parallelization Overhead and Scaling

The measured speedup is lower than the theoretical maximum of 8× for 8 threads. Practical performance can be affected by memory bandwidth, cache behavior, thread-management overhead, CPU resource contention, and other system-level factors.

This demonstrates that increasing the number of threads does not necessarily produce perfectly linear speedup.

### 6.4 MPI and CUDA Implementations

MPI and CUDA source files are included in the `src/` directory. However, verified execution-time results for these implementations were not part of the supplied sequential/OpenMP experiment evidence. They are therefore not assigned performance values in this report.

---

## 7. Repository Organization

The repository is organized as follows:

```text
PGC_lab/
│
├── image/
│   ├── sequential-result.png
│   ├── openmp-result.png
│   └── other performance and verification images
│
├── script/
│   ├── generate_plots.py
│   ├── parse_results.py
│   └── run_benchmarks.sh
│
├── src/
│   ├── matrix_sequential.c
│   ├── matrix_openmp.c
│   ├── matrix_mpi.c
│   └── matrix_cuda.cu
│
├── README.md
└── LAB_REPORT.md
```

---

## 8. Conclusion

The experiment demonstrates the performance benefit of shared-memory parallelism for large matrix multiplication. For the recorded `4000 × 4000` workload, the sequential implementation required **166.734358 seconds**, whereas the 8-thread OpenMP implementation required **40.215130 seconds**. This produced an observed speedup of approximately **4.15×**.

The experiment also demonstrates that practical parallel performance depends on system resources, memory behavior, and parallelization overhead, so measured speedup is not necessarily equal to the number of available threads.

MPI and CUDA implementations are included as project source files. Their benchmark results should be added only after those implementations are executed and their results are verified.
