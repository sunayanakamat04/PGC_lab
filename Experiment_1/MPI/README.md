# Experiment 1 - MPI

## Objective

To implement and test parallel matrix multiplication using MPI (Message Passing Interface) with multiple processes running across the master and worker nodes.

## Experiment Overview

This experiment covers:

- Checking communication between the master and worker nodes using `ping`.
- Setting up and verifying MPI on the system.
- Compiling and transferring the MPI program to the worker nodes using `scp`.
- Running matrix multiplication using multiple MPI processes.
- Verifying the output and measuring execution time.

## MPI Setup

The experiment used one master node and three worker nodes:

```text
Master   → 192.168.148.128
Worker 1 → 192.168.148.129
Worker 2 → 192.168.148.130
Worker 3 → 192.168.148.131
```

The nodes were checked using `ping`, and all four packets were received successfully for the worker nodes.

MPI compiler verification:

```text
mpicc --version
gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
```

## MPI Program

The MPI program performs matrix multiplication on a:

```text
4000 × 4000
```

matrix.

The work was distributed among four MPI processes:

```text
Rank 0 → Master   → 1000 rows
Rank 1 → Worker 1 → 1000 rows
Rank 2 → Worker 2 → 1000 rows
Rank 3 → Worker 3 → 1000 rows
```

## Result

The MPI matrix multiplication completed successfully.

| Parameter | Result |
|---|---:|
| Matrix Size | 4000 × 4000 |
| Number of MPI Processes | 4 |
| Rows per Process | 1000 |
| Execution Time | 226.167575 seconds |
| Verification C[0][0] | 4000.00 |

The final verification value was:

```text
Verification C[0][0] = 4000.00
```

## Result Images

The screenshots related to this experiment are stored in this folder:

```text
MPI/
├── mpi_matrixmul_ping.png
├── mpi_matrixmul_send_recv.png
└── mpi_results.png
```

- `mpi_matrixmul_ping.png` - Network connectivity test between the master and worker nodes.
- `mpi_matrixmul_send_recv.png` - MPI installation, compilation, and file transfer using `scp`.
- `mpi_results.png` - Final MPI matrix multiplication output and performance result.

## Conclusion

MPI was successfully configured across the master and worker nodes. The 4000 × 4000 matrix multiplication was divided among four MPI processes, with each process handling 1000 rows. The computation completed successfully with an execution time of 226.167575 seconds, and the output was verified using `C[0][0] = 4000.00`.
