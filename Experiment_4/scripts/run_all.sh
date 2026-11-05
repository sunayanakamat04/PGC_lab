#!/bin/bash
# ==============================================================================
# Script: run_all.sh
# Experiment 4: Analyze Cache Coherence (MSI, MESI, MOESI) and NUMA Performance
# Course: Parallel Computing and GPU Programming (PGC) Laboratory
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$ROOT_DIR/src"
RESULTS_DIR="$ROOT_DIR/results"

mkdir -p "$RESULTS_DIR"

echo "================================================================================"
echo "Step 2: NUMA Topology & Hardware Verification"
echo "================================================================================"
numactl --hardware
lscpu | grep -E 'Socket|Core|Thread|NUMA'
gcc --version
echo '#include <omp.h>' | gcc -E -fopenmp -xc - > /dev/null && echo "OpenMP OK"

echo ""
echo "================================================================================"
echo "Step 4: Running Cache Coherence Protocol Simulator (MSI, MESI, MOESI)"
echo "================================================================================"
cd "$SRC_DIR"
python3 coherence_sim.py 1000

echo ""
echo "================================================================================"
echo "Steps 5 to 7: Compiling C Programs (-O2 and -fopenmp)"
echo "================================================================================"
echo "[1/3] Compiling false_sharing.c..."
gcc -O2 false_sharing.c -fopenmp -o false_sharing

echo "[2/3] Compiling numa_sweep.c..."
gcc -O2 numa_sweep.c -fopenmp -o numa_sweep

echo "[3/3] Compiling compare_numa.c..."
gcc -O2 compare_numa.c -fopenmp -o compare_numa

echo ""
echo "================================================================================"
echo "Step 8: Testing False Sharing with 2 Threads"
echo "================================================================================"
echo "--- Adjacent Layout (Shared Cache Line) ---"
OMP_NUM_THREADS=2 ./false_sharing adjacent

echo "--- Padded Layout (Separate Cache Lines) ---"
OMP_NUM_THREADS=2 ./false_sharing padded

echo ""
echo "================================================================================"
echo "Step 12: Testing Physical Core Pinning with taskset (Cores 0, 2)"
echo "================================================================================"
OMP_NUM_THREADS=2 taskset -c 0,2 ./false_sharing adjacent
OMP_NUM_THREADS=2 taskset -c 0,2 ./false_sharing padded

echo ""
echo "================================================================================"
echo "Step 9 & 10: Running Comprehensive Comparison Program (compare_numa)"
echo "================================================================================"
echo "--- Default Allocation ---"
./compare_numa

echo "--- numactl Node 0 Binding ---"
numactl --cpunodebind=0 --membind=0 ./compare_numa

echo ""
echo "================================================================================"
echo "All steps completed successfully!"
echo "================================================================================"
