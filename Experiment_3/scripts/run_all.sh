#!/bin/bash
# ==============================================================================
# Script: run_all.sh
# Experiment: Analyze Synchronization Mechanisms in Parallel Programs
# Course: Parallel Computing and GPU Programming (PGC) Laboratory
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$ROOT_DIR/src"
RESULTS_DIR="$ROOT_DIR/results"

mkdir -p "$RESULTS_DIR"

echo "================================================================================"
echo "Step 5.4: Verifying GCC and OpenMP Support"
echo "================================================================================"
gcc --version
echo '#include <omp.h>' | gcc -E -fopenmp -xc - > /dev/null && echo "OpenMP OK"

echo ""
echo "================================================================================"
echo "Step 6 & 8: Compiling Programs"
echo "================================================================================"
cd "$SRC_DIR"
echo "[1/6] Compiling race.c (Race Condition)..."
gcc race.c -fopenmp -o race

echo "[2/6] Compiling critical.c (Critical Section)..."
gcc critical.c -fopenmp -o critical

echo "[3/6] Compiling atomic.c (Atomic Operation)..."
gcc atomic.c -fopenmp -o atomic

echo "[4/6] Compiling barrier.c (Barrier Synchronization)..."
gcc barrier.c -fopenmp -o barrier

echo "[5/6] Compiling semaphore.c (POSIX Semaphore)..."
gcc semaphore.c -pthread -o semaphore

echo "[6/6] Compiling compare_sync.c (Benchmark Program)..."
gcc compare_sync.c -fopenmp -o compare_sync

echo ""
echo "================================================================================"
echo "Executing Individual Programs"
echo "================================================================================"
echo "--- Program 1: Race Condition (Unsynchronized) ---"
./race

echo "--- Program 2: Critical Section ---"
./critical

echo "--- Program 3: Atomic Operation ---"
./atomic

echo "--- Program 4: Barrier Synchronization ---"
./barrier

echo "--- Program 5: POSIX Semaphore ---"
./semaphore

echo ""
echo "================================================================================"
echo "Step 9: Testing with Environment Variable OMP_NUM_THREADS"
echo "================================================================================"
echo "--- Running with OMP_NUM_THREADS=4 ---"
OMP_NUM_THREADS=4 ./atomic
OMP_NUM_THREADS=4 ./barrier

echo "--- Running with OMP_NUM_THREADS=8 ---"
export OMP_NUM_THREADS=8
./critical

echo ""
echo "================================================================================"
echo "Step 10: Running Comprehensive Benchmark Program (compare_sync)"
echo "================================================================================"
./compare_sync

echo ""
echo "================================================================================"
echo "All steps completed successfully!"
echo "================================================================================"
