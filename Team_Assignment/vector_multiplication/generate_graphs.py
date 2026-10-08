import csv
import matplotlib.pyplot as plt

data = []

with open("results/results.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        data.append({
            "vector_size": int(row["vector_size"]),
            "threads": int(row["threads"]),
            "execution_time": float(row["execution_time"]),
            "speedup": float(row["speedup"]),
            "efficiency": float(row["efficiency"])
        })

sizes = sorted(set(row["vector_size"] for row in data))
threads = sorted(set(row["threads"] for row in data))

# Execution Time
plt.figure(figsize=(9, 6))

for size in sizes:
    rows = [r for r in data if r["vector_size"] == size]
    x = [r["threads"] for r in rows]
    y = [r["execution_time"] for r in rows]
    plt.plot(x, y, marker="o", label=f"{size:,} elements")

plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.title("OpenMP Vector Multiplication - Execution Time")
plt.xticks(threads)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/execution_time.png", dpi=300)
plt.close()

# Speedup
plt.figure(figsize=(9, 6))

for size in sizes:
    rows = [r for r in data if r["vector_size"] == size]
    x = [r["threads"] for r in rows]
    y = [r["speedup"] for r in rows]
    plt.plot(x, y, marker="o", label=f"{size:,} elements")

plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.title("OpenMP Vector Multiplication - Speedup")
plt.xticks(threads)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/speedup.png", dpi=300)
plt.close()

# Efficiency
plt.figure(figsize=(9, 6))

for size in sizes:
    rows = [r for r in data if r["vector_size"] == size]
    x = [r["threads"] for r in rows]
    y = [r["efficiency"] for r in rows]
    plt.plot(x, y, marker="o", label=f"{size:,} elements")

plt.xlabel("Number of Threads")
plt.ylabel("Efficiency (%)")
plt.title("OpenMP Vector Multiplication - Efficiency")
plt.xticks(threads)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/efficiency.png", dpi=300)
plt.close()

print("Graphs generated successfully.")
print("Saved in graphs/")
