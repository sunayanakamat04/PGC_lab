<div align="center">

# Parallel Computing and GPU Programming (PGC) Laboratory
### Laboratory Experiments, Parallel Architectures, Synchronization Benchmarks & Implementations

**Student:** Sunayana Kamat  
**Repository:** [sunayanakamat04/PGC_lab](https://github.com/sunayanakamat04/PGC_lab)  

---

</div>

## Repository Index

| Directory | Experiment / Project | Technologies | Key Highlights |
| :--- | :--- | :--- | :--- |
| [`Experiment_1/`](./Experiment_1) | **Experiment 1:** High Performance Matrix Multiplication & Parallel Models | OpenMP, MPI, CUDA, C | Sequential vs OpenMP vs MPI vs CUDA benchmarks, speedup & roofline analysis |
| [`Experiment_2/`](./Experiment_2) | **Experiment 2:** Multithreaded Programming with Pthreads & OpenMP | POSIX Threads, OpenMP, C | Thread creation, mutexes, barriers, work-sharing, race conditions |
| [`Experiment_3/`](./Experiment_3) | **Experiment 3:** Analyze Synchronization Mechanisms in Parallel Programs | OpenMP, POSIX Semaphores, C | Race conditions, critical sections, atomics, barriers, binary semaphores, 1-8 thread benchmark |
| [`Team_Assignment/`](./Team_Assignment) | **Team Assignment:** Parallel Vector Multiplication | OpenMP, C, Python | Scalability and vector operation acceleration |

---

## Experiment 3 Overview

- **Aim:** To implement and study common synchronization mechanisms in shared-memory parallel programs (unsynchronized race, critical sections, atomic operations, barriers, semaphores/locks) and evaluate correctness, execution time, and scalability.
- **Environment:** Ubuntu 22.04 LTS (WSL2 / VMware Workstation Pro), GCC 15.2.0, OpenMP runtime (`libgomp`), POSIX Threads.
- **Hardware:** 12th Gen Intel Core i5-12500H (16 vCPUs).
- **Key Finding:** Atomic operations provide the best performance and scalability for simple shared variable updates by leveraging CPU bus-lock instructions, while critical sections and locks suffer heavy performance degradation under high thread contention.

For complete documentation, source codes, execution steps, terminal screenshots, and performance graphs, see **[`Experiment_3/README.md`](./Experiment_3/README.md)**.
