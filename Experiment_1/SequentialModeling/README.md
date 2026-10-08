# Experiment 1 - Sequential Matrix Multiplication

## Objective

To implement matrix multiplication sequentially using C and measure the execution time for a large matrix.

## Experiment Overview

In this experiment, matrix multiplication is performed without using parallel programming techniques. The program was written in C and compiled using GCC inside the Ubuntu environment.

The program was compiled using:

```bash
gcc -O2 matrix_sequential.c -o matrix_sequential
```

The compiled program was then executed using:

```bash
./matrix_sequential
```

## Configuration

| Parameter | Value |
|---|---:|
| Matrix Size | 4000 × 4000 |
| Execution Mode | Sequential |
| Execution Time | 266.477234 seconds |
| Verification C[0][0] | 4000.00 |

## Result

The sequential matrix multiplication completed successfully.

The program output was:

```text
Sequential Matrix Multiplication Completed
Matrix Size = 4000 x 4000
Execution Time = 266.477234 seconds
Verification C[0][0] = 4000.00
```

The verification value confirms that the matrix multiplication produced the expected result.

## Environment Setup

The experiment was performed using Ubuntu through WSL. GCC was installed and checked before compiling the program.

The GCC version used in the experiment was:

```text
gcc (Ubuntu 15.2.0-1ubuntu1) 15.2.0
```

## Result Files

This folder contains the screenshots related to the experiment:

```text
SequentialModeling/
├── Sequential_Setup.png
└── Sequential_Result.png
```

- `Sequential_Setup.png` - Shows the Ubuntu/WSL setup, GCC installation and compiler configuration.
- `Sequential_Result.png` - Shows the compilation and final sequential matrix multiplication output.

## Conclusion

The sequential implementation successfully multiplied two 4000 × 4000 matrices. The execution took 266.477234 seconds, and the result was verified using `C[0][0] = 4000.00`.

This sequential implementation can be used as a baseline for comparing the performance of parallel implementations such as OpenMP, MPI, and CUDA.
