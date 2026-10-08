# Experiment 1 - CUDA Matrix Multiplication

## Objective

To perform matrix multiplication using CUDA and observe the execution performance of the computation on the GPU.

## Experiment Details

The CUDA program performs matrix multiplication using a 2D grid of CUDA thread blocks.

| Parameter | Value |
|---|---:|
| Matrix Size | 4000 × 4000 |
| Grid Size | 250 × 250 blocks |
| Block Size | 16 × 16 threads |
| Kernel Execution Time | 0.064499 seconds |
| Total CUDA Phase Time | 0.077087 seconds |
| Verification C[0][0] | 4000.00 |

## Result

The CUDA matrix multiplication completed successfully.

The output verification value was:

```text
Verification C[0][0] = 4000.00
```

The measured kernel execution time was:

```text
0.064499 seconds
```

and the total CUDA phase time was:

```text
0.077087 seconds
```

## Output

The execution output and measured performance are available in:

`CUDA_Result.png`

## Folder Structure

```text
Experiment_1/
└── CUDA/
    ├── CUDA_Result.png
    └── README.md
```

## Conclusion

CUDA was successfully used to perform matrix multiplication on a 4000 × 4000 matrix. The experiment also recorded the CUDA kernel execution time and total CUDA phase time, and the result was verified successfully.
