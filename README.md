# PGC Lab — Parallel Computing Experiments

<p align="center">
  <b>Sequential vs OpenMP Matrix Multiplication</b><br>
  Parallel and Distributed Computing Laboratory
</p>

---

## 📌 Overview

This repository contains the implementation, execution results, screenshots, and performance analysis of matrix multiplication using:

1. **Sequential execution**
2. **OpenMP shared-memory parallelism**

The same **4000 × 4000 matrix multiplication** problem is used for both implementations.

---

## 🧪 Experiments

| Experiment | Topic | Description |
|---|---|---|
| [Experiment 1 — Sequential](./Experiment-1-Sequential/) | Sequential Matrix Multiplication | 4000 × 4000 matrix multiplication using sequential execution |
| [Experiment 2 — OpenMP](./Experiment-2-OpenMP/) | OpenMP Matrix Multiplication | Parallel matrix multiplication using OpenMP threads |

---

# 1️⃣ Experiment 1 — Sequential Matrix Multiplication

## 🎯 Objective

To implement 4000 × 4000 matrix multiplication using sequential execution and measure the execution time as the baseline for parallel performance comparison.

## ⚙️ Working Principle

For every element of matrix `C`:

```text
C[i][j] = Σ A[i][k] × B[k][j]
           k=0 to N-1
```

The complete computation is performed sequentially.

### Execution Model

```text
       Matrix A
          │
          ├──────────┐
          │          │
       Matrix B      ↓
          │     Sequential
          └───→ Computation
                    │
                    ↓
                Matrix C
```

## 🔧 Configuration

- Matrix size: **4000 × 4000**
- Matrix A elements: **1.0**
- Matrix B elements: **1.0**
- Execution model: **Sequential**
- Verification: **C[0][0] = 4000.00**

## 📊 Reference Result

| Parameter | Value |
|---|---:|
| Matrix Size | 4000 × 4000 |
| Execution Time | **244.120000 s** |
| Verification | **4000.00** |

---

# 2️⃣ Experiment 2 — OpenMP Matrix Multiplication

## 🎯 Objective

To parallelize the 4000 × 4000 matrix multiplication using OpenMP and compare its performance with the sequential implementation.

## ⚙️ Working Principle

OpenMP divides loop iterations among multiple threads running on the same shared-memory system.

```c
#pragma omp parallel for
```

### Execution Model

```text
                    Matrix Multiplication
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
          Thread 1       Thread 2       Thread 3    ...
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                       Matrix C
```

## 🔧 Configuration

- Matrix size: **4000 × 4000**
- Reference threads: **8**
- Execution model: **Shared-memory parallelism**
- Verification: **C[0][0] = 4000.00**

## 📊 Reference Result

| Parameter | Value |
|---|---:|
| Matrix Size | 4000 × 4000 |
| Threads | **8** |
| Execution Time | **30.830434 s** |
| Verification | **4000.00** |
| Speedup | **≈ 7.92×** |

---

# 📈 Performance Analysis

## 1. Execution Time Comparison

**Reference values:**

- Sequential: **244.120000 seconds**
- OpenMP: **30.830434 seconds**

<!-- The graph is embedded directly in this README. No external graph image is required. -->

<svg width="760" height="430" viewBox="0 0 760 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Execution time comparison">
  <text x="380" y="32" text-anchor="middle" font-size="22" font-family="Arial">4000 × 4000 Matrix Multiplication — Execution Time</text>
  <line x1="90" y1="360" x2="720" y2="360" stroke="#333" stroke-width="2"/>
  <line x1="90" y1="60" x2="90" y2="360" stroke="#333" stroke-width="2"/>
  <line x1="90" y1="360" x2="720" y2="360" stroke="#ddd"/>
  <line x1="90" y1="285" x2="720" y2="285" stroke="#ddd"/>
  <line x1="90" y1="210" x2="720" y2="210" stroke="#ddd"/>
  <line x1="90" y1="135" x2="720" y2="135" stroke="#ddd"/>
  <line x1="90" y1="60" x2="720" y2="60" stroke="#ddd"/>
  <text x="78" y="365" text-anchor="end" font-size="13" font-family="Arial">0</text>
  <text x="78" y="290" text-anchor="end" font-size="13" font-family="Arial">60</text>
  <text x="78" y="215" text-anchor="end" font-size="13" font-family="Arial">120</text>
  <text x="78" y="140" text-anchor="end" font-size="13" font-family="Arial">180</text>
  <text x="78" y="65" text-anchor="end" font-size="13" font-family="Arial">240</text>
  <rect x="190" y="60" width="150" height="300" fill="#4e79a7"/>
  <rect x="480" y="321.5" width="150" height="38.5" fill="#59a14f"/>
  <text x="265" y="50" text-anchor="middle" font-size="16" font-family="Arial">244.12 s</text>
  <text x="555" y="312" text-anchor="middle" font-size="16" font-family="Arial">30.83 s</text>
  <text x="265" y="388" text-anchor="middle" font-size="17" font-family="Arial">Sequential</text>
  <text x="555" y="388" text-anchor="middle" font-size="17" font-family="Arial">OpenMP</text>
  <text x="30" y="210" text-anchor="middle" font-size="14" font-family="Arial" transform="rotate(-90 30 210)">Execution Time (seconds)</text>
</svg>

### Observation

In the reference run, OpenMP completes the same matrix multiplication in substantially less time because the computation is distributed among multiple CPU threads.

---

## 2. Speedup Comparison

### Formula

```text
Speedup = Sequential Execution Time / OpenMP Execution Time

        = 244.120000 / 30.830434

        ≈ 7.92×
```

<svg width="760" height="430" viewBox="0 0 760 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Speedup comparison">
  <text x="380" y="32" text-anchor="middle" font-size="22" font-family="Arial">Speedup Relative to Sequential Baseline</text>
  <line x1="90" y1="360" x2="720" y2="360" stroke="#333" stroke-width="2"/>
  <line x1="90" y1="60" x2="90" y2="360" stroke="#333" stroke-width="2"/>
  <line x1="90" y1="360" x2="720" y2="360" stroke="#ddd"/>
  <line x1="90" y1="285" x2="720" y2="285" stroke="#ddd"/>
  <line x1="90" y1="210" x2="720" y2="210" stroke="#ddd"/>
  <line x1="90" y1="135" x2="720" y2="135" stroke="#ddd"/>
  <line x1="90" y1="60" x2="720" y2="60" stroke="#ddd"/>
  <text x="78" y="365" text-anchor="end" font-size="13" font-family="Arial">0</text>
  <text x="78" y="290" text-anchor="end" font-size="13" font-family="Arial">2</text>
  <text x="78" y="215" text-anchor="end" font-size="13" font-family="Arial">4</text>
  <text x="78" y="140" text-anchor="end" font-size="13" font-family="Arial">6</text>
  <text x="78" y="65" text-anchor="end" font-size="13" font-family="Arial">8</text>
  <rect x="190" y="322.5" width="150" height="37.5" fill="#4e79a7"/>
  <rect x="480" y="63" width="150" height="297" fill="#59a14f"/>
  <text x="265" y="312" text-anchor="middle" font-size="16" font-family="Arial">1.00×</text>
  <text x="555" y="53" text-anchor="middle" font-size="16" font-family="Arial">7.92×</text>
  <text x="265" y="388" text-anchor="middle" font-size="17" font-family="Arial">Sequential</text>
  <text x="555" y="388" text-anchor="middle" font-size="17" font-family="Arial">OpenMP</text>
  <text x="30" y="210" text-anchor="middle" font-size="14" font-family="Arial" transform="rotate(-90 30 210)">Speedup (×)</text>
</svg>

### Interpretation

The calculated speedup is approximately **7.92×** for the reference measurements.

---

# 📊 Overall Comparison

| Feature | Sequential | OpenMP |
|---|---|---|
| Execution model | Sequential | Parallel |
| CPU execution | Single execution flow | Multiple threads |
| Memory model | Sequential execution | Shared memory |
| Matrix size | 4000 × 4000 | 4000 × 4000 |
| Reference time | 244.120000 s | 30.830434 s |
| Verification | 4000.00 | 4000.00 |
| Speedup | 1× baseline | ≈ 7.92× |

---

# 🧠 Sequential vs OpenMP — Simple Difference

### Sequential

```text
Work
 ↓
One execution flow
 ↓
Complete calculation
 ↓
Result
```

### OpenMP

```text
                 Work
                  ↓
        ┌─────────┼─────────┐
        ↓         ↓         ↓
     Thread 1  Thread 2  Thread 3 ...
        └─────────┼─────────┘
                  ↓
                Result
```

**Sequential:** one execution flow performs the work.

**OpenMP:** multiple threads perform different portions of the work while sharing memory.

---

# ✅ Verification

Both implementations should produce:

```text
Verification C[0][0] = 4000.00
```

This verifies the matrix multiplication result for matrices initialized with `1.0`.

---

# 🖥️ Compilation and Execution

## Sequential

```bash
gcc -O2 matrix_sequential.c -o matrix_sequential
./matrix_sequential
```

If the file is named `mat.c` on Windows PowerShell:

```powershell
gcc -O2 mat.c -o mat.exe
.\mat.exe
```

## OpenMP

On a Linux/WSL environment with OpenMP support:

```bash
export OMP_NUM_THREADS=8
gcc -O2 -fopenmp mat_openmp.c -o mat_openmp
./mat_openmp
```

---

# 📁 Repository Structure

```text
PGC_lab/
│
├── Experiment-1-Sequential/
│   └── screenshots/
│
├── Experiment-2-OpenMP/
│   └── screenshots/
│
└── README.md
```

---

# 🛠️ Tools & Technologies

- **C**
- **GCC**
- **OpenMP**
- **Git**
- **GitHub**
- **Windows / Linux execution environments**

---

# 📝 Conclusion

These experiments demonstrate the difference between sequential and shared-memory parallel execution for large-scale matrix multiplication.

The sequential implementation provides the baseline performance, while OpenMP distributes the computation among multiple CPU threads.

For the reference measurements, execution time decreased from **244.120000 s** to **30.830434 s**, giving a calculated speedup of approximately **7.92×**.

> **Note:** The timings shown above are reference values. Replace them with your own measured timings if your final experiment results differ.
