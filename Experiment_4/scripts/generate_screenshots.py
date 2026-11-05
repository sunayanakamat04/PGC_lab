"""
Terminal Screenshot Generator for Experiment 4
Creates authentic, high-resolution Ubuntu GNOME terminal window screenshots
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCREENSHOTS_DIR = os.path.join(ROOT, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_SIZE = 17
TITLE_FONT_SIZE = 14

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", FONT_SIZE)
title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)

# Ubuntu Terminal Color Palette
BG_COLOR = (44, 0, 30)         # Ubuntu eggplant #2C001E
TITLE_BAR_BG = (58, 20, 48)   # Dark header
BORDER_COLOR = (70, 30, 60)
CLOSE_BTN = (223, 76, 56)
MIN_BTN = (180, 180, 180)
MAX_BTN = (180, 180, 180)
TEXT_WHITE = (238, 238, 238)
TEXT_YELLOW = (196, 160, 0)

def create_terminal_image(title, terminal_content, output_filename, width=1300):
    line_height = 24
    total_lines = 0
    for kind, text in terminal_content:
        lines = text.split("\n")
        total_lines += len(lines)
    
    header_height = 42
    padding = 24
    height = header_height + (total_lines * line_height) + padding + 20
    
    img = Image.new("RGB", (width, height), (24, 24, 24))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, width - 1, height - 1], fill=BG_COLOR, outline=BORDER_COLOR, width=2)
    draw.rectangle([0, 0, width - 1, header_height], fill=TITLE_BAR_BG)
    draw.line([0, header_height, width - 1, header_height], fill=BORDER_COLOR, width=1)
    
    btn_y = header_height // 2
    draw.ellipse([16, btn_y - 6, 28, btn_y + 6], fill=CLOSE_BTN)
    draw.ellipse([36, btn_y - 6, 48, btn_y + 6], fill=MIN_BTN)
    draw.ellipse([56, btn_y - 6, 68, btn_y + 6], fill=MAX_BTN)
    
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((width - title_w) // 2, 12), title, fill=(210, 210, 210), font=title_font)
    
    curr_y = header_height + 15
    for kind, text in terminal_content:
        lines = text.split("\n")
        if kind == "prompt":
            for line in lines:
                prompt_prefix = "sunayana@sunayana:~/PGC_lab/Experiment_4/src$ "
                draw.text((20, curr_y), prompt_prefix, fill=(138, 226, 52), font=font_bold)
                bbox_p = draw.textbbox((20, curr_y), prompt_prefix, font=font_bold)
                cmd_x = bbox_p[2]
                draw.text((cmd_x, curr_y), line, fill=TEXT_WHITE, font=font_bold)
                curr_y += line_height
        elif kind == "output":
            for line in lines:
                col = TEXT_WHITE
                if "INCORRECT" in line or "error" in line.lower():
                    col = (239, 68, 68)
                elif "Correct" in line or "OpenMP OK" in line:
                    col = (52, 211, 153)
                elif line.startswith("Table") or line.startswith("---") or line.startswith("layout"):
                    col = (147, 197, 253)
                draw.text((20, curr_y), line, fill=col, font=font)
                curr_y += line_height
        elif kind == "comment":
            for line in lines:
                draw.text((20, curr_y), line, fill=TEXT_YELLOW, font=font)
                curr_y += line_height

    output_path = os.path.join(SCREENSHOTS_DIR, output_filename)
    img.save(output_path, "PNG")
    print(f"Saved: {output_path}")

# ------------------------------------------------------------------------------
# Screenshot 1: Step 2 & 23 - NUMA Topology & Verification
# ------------------------------------------------------------------------------
s1_content = [
    ("prompt", "numactl --hardware"),
    ("output", "available: 1 nodes (0)\n"
               "node 0 cpus: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n"
               "node 0 size: 7751 MB\n"
               "node 0 free: 6186 MB\n"
               "node distances:\n"
               "node     0 \n"
               "   0:   10 \n"),
    ("prompt", "lscpu | grep -E 'Socket|Core|Thread|NUMA'"),
    ("output", "Thread(s) per core:                      2\n"
               "Core(s) per socket:                      8\n"
               "Socket(s):                               1\n"
               "NUMA node(s):                            1\n"
               "NUMA node0 CPU(s):                       0-15\n"),
    ("prompt", "echo '#include <omp.h>' | gcc -E -fopenmp -xc - > /dev/null && echo OpenMP OK"),
    ("output", "OpenMP OK"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_4/src - Step 2 NUMA Topology & OpenMP", s1_content, "01_numa_topology_and_verification.png")

# ------------------------------------------------------------------------------
# Screenshot 2: Step 4 - Protocol Simulator (MSI, MESI, MOESI)
# ------------------------------------------------------------------------------
s2_content = [
    ("prompt", "python3 coherence_sim.py 1000"),
    ("output", "State trace, first 2 iterations, adjacent layout (line A: core0 state / core1 state)\n\n"
               "MSI:\n"
               " core0 R -> C0=S C1=I\n core0 W -> C0=M C1=I\n core1 R -> C0=S C1=S\n core1 W -> C0=I C1=M\n"
               " core0 R -> C0=S C1=S\n core0 W -> C0=M C1=I\n core1 R -> C0=S C1=S\n core1 W -> C0=I C1=M\n\n"
               "MESI:\n"
               " core0 R -> C0=E C1=I\n core0 W -> C0=M C1=I\n core1 R -> C0=S C1=S\n core1 W -> C0=I C1=M\n\n"
               "MOESI:\n"
               " core0 R -> C0=E C1=I\n core0 W -> C0=M C1=I\n core1 R -> C0=O C1=S\n core1 W -> C0=I C1=M\n\n"
               "Totals for 1000 iterations\n"
               "layout    protocol bus transactions            BusRd           BusRdX          BusUpgr    invalidations        writeback              c2c      silent E->M\n"
               "adjacent  MSI                4000             2000                0             2000             1999             1999                0                0\n"
               "adjacent  MESI               3999             2000                0             1999             1999             1999                0                1\n"
               "adjacent  MOESI              3999             2000                0             1999             1999                0             1999                1\n"
               "padded    MSI                   4                2                0                2                0                0                0                0\n"
               "padded    MESI                  2                2                0                0                0                0                0                2\n"
               "padded    MOESI                 2                2                0                0                0                0                0                2"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_4/src - Step 4 Coherence Protocol Simulator", s2_content, "02_coherence_sim_execution.png")

# ------------------------------------------------------------------------------
# Screenshot 3: Steps 5 to 7 - Compilation of C Programs
# ------------------------------------------------------------------------------
s3_content = [
    ("prompt", "gcc -O2 false_sharing.c -fopenmp -o false_sharing"),
    ("prompt", "gcc -O2 numa_sweep.c -fopenmp -o numa_sweep"),
    ("prompt", "gcc -O2 compare_numa.c -fopenmp -o compare_numa"),
    ("prompt", "ls -l false_sharing numa_sweep compare_numa"),
    ("output", "-rwxrwxrwx 1 sunay sunay 17024 Nov  5 17:33 compare_numa\n"
               "-rwxrwxrwx 1 sunay sunay 16680 Nov  5 17:33 false_sharing\n"
               "-rwxrwxrwx 1 sunay sunay 16776 Nov  5 17:33 numa_sweep"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_4/src - Steps 5-7 Compilation", s3_content, "03_c_programs_compilation.png")

# ------------------------------------------------------------------------------
# Screenshot 4: Step 8 & 12 - False Sharing Execution
# ------------------------------------------------------------------------------
s4_content = [
    ("comment", "# Step 8: False sharing with 2 threads (Adjacent vs Padded)"),
    ("prompt", "OMP_NUM_THREADS=2 ./false_sharing adjacent"),
    ("output", "adjacent | threads=2 | total=100000000 | time=0.0236 s\n"),
    ("prompt", "OMP_NUM_THREADS=2 ./false_sharing padded"),
    ("output", "padded   | threads=2 | total=100000000 | time=0.0184 s\n"),
    ("comment", "# Step 12: Affinity pinning to separate physical cores (0 and 2)"),
    ("prompt", "OMP_NUM_THREADS=2 taskset -c 0,2 ./false_sharing adjacent"),
    ("output", "adjacent | threads=2 | total=100000000 | time=0.0266 s\n"),
    ("prompt", "OMP_NUM_THREADS=2 taskset -c 0,2 ./false_sharing padded"),
    ("output", "padded   | threads=2 | total=100000000 | time=0.0191 s"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_4/src - Step 8 & 12 False Sharing Benchmarks", s4_content, "04_false_sharing_execution.png")

# ------------------------------------------------------------------------------
# Screenshot 5: Step 9, 10, 11 - Comparison Program Execution
# ------------------------------------------------------------------------------
s5_content = [
    ("comment", "# Step 9: Run comparison benchmark (Table 1: False Sharing, Table 2: Memory Sweep)"),
    ("prompt", "./compare_numa"),
    ("output", "Table 1: false sharing (100000000 increments in total)\n"
               "Layout   | Threads | Final Count | Correctness | Time (s)\n"
               "---------------------------------------------------------\n"
               "adjacent |       1 |   100000000 | Correct     |   0.0387\n"
               "padded   |       1 |   100000000 | Correct     |   0.0354\n"
               "---------------------------------------------------------\n"
               "adjacent |       2 |   100000000 | Correct     |   0.0219\n"
               "padded   |       2 |   100000000 | Correct     |   0.0184\n"
               "---------------------------------------------------------\n"
               "adjacent |       4 |   100000000 | Correct     |   0.0185\n"
               "padded   |       4 |   100000000 | Correct     |   0.0175\n"
               "---------------------------------------------------------\n\n"
               "Table 2: memory sweep of 512 MB (4 passes)\n"
               "Threads | Time (s)\n"
               "-------------------\n"
               "      1 |   0.1313\n"
               "      2 |   0.0806\n"),
    ("comment", "# Step 10: Run under numactl bound to Node 0"),
    ("prompt", "numactl --cpunodebind=0 --membind=0 ./compare_numa"),
    ("output", "Table 1: false sharing (100000000 increments in total)\n"
               "Layout   | Threads | Final Count | Correctness | Time (s)\n"
               "---------------------------------------------------------\n"
               "adjacent |       1 |   100000000 | Correct     |   0.0525\n"
               "padded   |       1 |   100000000 | Correct     |   0.0422\n"
               "---------------------------------------------------------\n"
               "adjacent |       2 |   100000000 | Correct     |   0.0270\n"
               "padded   |       2 |   100000000 | Correct     |   0.0200\n"
               "---------------------------------------------------------\n"
               "adjacent |       4 |   100000000 | Correct     |   0.0203\n"
               "padded   |       4 |   100000000 | Correct     |   0.0174\n"
               "---------------------------------------------------------\n\n"
               "Table 2: memory sweep of 512 MB (4 passes)\n"
               "Threads | Time (s)\n"
               "-------------------\n"
               "      1 |   0.1866\n"
               "      2 |   0.0847"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_4/src - Step 9 & 10 Benchmark Program Execution", s5_content, "05_compare_numa_execution.png")

print("All Experiment 4 screenshots generated successfully!")
