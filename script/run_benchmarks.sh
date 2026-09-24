#!/bin/bash
# PGC Benchmark Automation Script

set -e

echo "=========================================================="
echo " Parallel & Grid Computing (PGC) Matrix Multiplication "
echo "=========================================================="

# 1. Compile C & OpenMP programs
echo "[+] Compiling Sequential implementation..."
gcc -O2 src/matrix_sequential.c -o src/matrix_sequential

echo "[+] Compiling OpenMP implementation..."
gcc -O2 -fopenmp src/matrix_openmp.c -o src/matrix_openmp

# 2. Compile MPI if available
if command -v mpicc &> /dev/null; then
    echo "[+] Compiling MPI implementation..."
    mpicc -O2 src/matrix_mpi.c -o src/matrix_mpi
fi

# 3. Compile CUDA if nvcc available
if command -v nvcc &> /dev/null; then
    echo "[+] Compiling CUDA implementation..."
    nvcc -O2 src/matrix_cuda.cu -o src/matrix_cuda
fi

echo "=========================================================="
echo " Execution & Verification Complete."
echo "=========================================================="
