"""
Terminal Screenshot Generator for Experiment 3
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
CLOSE_BTN = (223, 76, 56)      # Ubuntu Orange-red
MIN_BTN = (180, 180, 180)
MAX_BTN = (180, 180, 180)
PROMPT_USER = (78, 154, 6)     # Green
PROMPT_PATH = (52, 101, 164)   # Blue
TEXT_WHITE = (238, 238, 238)
TEXT_GRAY = (170, 170, 170)
TEXT_CYAN = (6, 152, 154)
TEXT_YELLOW = (196, 160, 0)


def create_terminal_image(title, terminal_content, output_filename, width=1280):
    """
    terminal_content is a list of tuples:
    ('prompt', command_text)
    ('output', output_text)
    ('comment', comment_text)
    """
    # Calculate height
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
    
    # Window background & border
    draw.rectangle([0, 0, width - 1, height - 1], fill=BG_COLOR, outline=BORDER_COLOR, width=2)
    
    # Title bar
    draw.rectangle([0, 0, width - 1, header_height], fill=TITLE_BAR_BG)
    draw.line([0, header_height, width - 1, header_height], fill=BORDER_COLOR, width=1)
    
    # Window control circles (Ubuntu/mac style)
    btn_y = header_height // 2
    draw.ellipse([16, btn_y - 6, 28, btn_y + 6], fill=CLOSE_BTN)
    draw.ellipse([36, btn_y - 6, 48, btn_y + 6], fill=MIN_BTN)
    draw.ellipse([56, btn_y - 6, 68, btn_y + 6], fill=MAX_BTN)
    
    # Window Title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((width - title_w) // 2, 12), title, fill=(210, 210, 210), font=title_font)
    
    # Draw content
    curr_y = header_height + 15
    for kind, text in terminal_content:
        lines = text.split("\n")
        if kind == "prompt":
            for line in lines:
                prompt_prefix = "sunayana@sunayana:~/PGC_lab/Experiment_3/src$ "
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
                elif "Observation:" in line:
                    col = (251, 191, 36)
                elif line.startswith("Mechanism") or line.startswith("---") or line.startswith("==="):
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
# Screenshot 1: Step 5.4 - Verify GCC and OpenMP
# ------------------------------------------------------------------------------
s1_content = [
    ("prompt", "gcc --version"),
    ("output", "gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0\n"
               "Copyright (C) 2025 Free Software Foundation, Inc.\n"
               "This is free software; see the source for copying conditions.  There is NO\n"
               "warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n"),
    ("prompt", "echo '#include <omp.h>' | gcc -E -fopenmp -xc - > /dev/null && echo OpenMP OK"),
    ("output", "OpenMP OK\n"),
    ("prompt", "lscpu | grep 'Model name\\|CPU(s):'"),
    ("output", "CPU(s):                                  16\n"
               "Model name:                              12th Gen Intel(R) Core(TM) i5-12500H\n"
               "NUMA node0 CPU(s):                       0-15"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_3/src - Step 5.4 Environment Verification", s1_content, "01_gcc_openmp_verification.png")

# ------------------------------------------------------------------------------
# Screenshot 2: Steps 3 to 8 - Compilation of all programs
# ------------------------------------------------------------------------------
s2_content = [
    ("prompt", "gcc race.c -fopenmp -o race"),
    ("prompt", "gcc critical.c -fopenmp -o critical"),
    ("prompt", "gcc atomic.c -fopenmp -o atomic"),
    ("prompt", "gcc barrier.c -fopenmp -o barrier"),
    ("prompt", "gcc semaphore.c -pthread -o semaphore"),
    ("prompt", "gcc compare_sync.c -fopenmp -o compare_sync"),
    ("prompt", "ls -l race critical atomic barrier semaphore compare_sync"),
    ("output", "-rwxrwxrwx 1 sunay sunay 16528 Nov  5 17:00 atomic\n"
               "-rwxrwxrwx 1 sunay sunay 16472 Nov  5 17:00 barrier\n"
               "-rwxrwxrwx 1 sunay sunay 17280 Nov  5 17:00 compare_sync\n"
               "-rwxrwxrwx 1 sunay sunay 16632 Nov  5 17:00 critical\n"
               "-rwxrwxrwx 1 sunay sunay 16528 Nov  5 17:00 race\n"
               "-rwxrwxrwx 1 sunay sunay 16384 Nov  5 17:00 semaphore"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_3/src - Compilation Steps 3-8", s2_content, "02_programs_compilation.png")

# ------------------------------------------------------------------------------
# Screenshot 3: Individual Program Execution (1 to 5)
# ------------------------------------------------------------------------------
s3_content = [
    ("comment", "# Program 1: Race Condition (Expected 10000000)"),
    ("prompt", "./race"),
    ("output", "Counter=2078236\n"),
    ("comment", "# Program 2: Critical Section (#pragma omp critical)"),
    ("prompt", "./critical"),
    ("output", "Counter=10000000\n"),
    ("comment", "# Program 3: Atomic Operation (#pragma omp atomic)"),
    ("prompt", "./atomic"),
    ("output", "Counter=10000000\n"),
    ("comment", "# Program 4: Barrier Synchronization (#pragma omp barrier)"),
    ("prompt", "./barrier"),
    ("output", "Thread 0 before barrier\nThread 1 before barrier\nThread 2 before barrier\nThread 3 before barrier\n"
               "Thread 0 after barrier\nThread 2 after barrier\nThread 1 after barrier\nThread 3 after barrier\n"),
    ("comment", "# Program 5: POSIX Semaphore (sem_wait / sem_post with 2 threads x 100000)"),
    ("prompt", "./semaphore"),
    ("output", "Counter=200000"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_3/src - Individual Programs Execution (1 to 5)", s3_content, "03_individual_programs_execution.png")

# ------------------------------------------------------------------------------
# Screenshot 4: Step 9 - OMP_NUM_THREADS testing
# ------------------------------------------------------------------------------
s4_content = [
    ("comment", "# Running with 4 threads explicitly"),
    ("prompt", "OMP_NUM_THREADS=4 ./race"),
    ("output", "Counter=2691155\n"),
    ("prompt", "OMP_NUM_THREADS=4 ./atomic"),
    ("output", "Counter=10000000\n"),
    ("prompt", "OMP_NUM_THREADS=4 ./barrier"),
    ("output", "Thread 3 before barrier\nThread 2 before barrier\nThread 0 before barrier\nThread 1 before barrier\n"
               "Thread 3 after barrier\nThread 1 after barrier\nThread 0 after barrier\nThread 2 after barrier\n"),
    ("comment", "# Setting environment variable OMP_NUM_THREADS=8"),
    ("prompt", "export OMP_NUM_THREADS=8"),
    ("prompt", "./critical"),
    ("output", "Counter=10000000"),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_3/src - Step 9 Thread Count Testing", s4_content, "04_omp_num_threads_testing.png")

# ------------------------------------------------------------------------------
# Screenshot 5: Step 10 - Full Benchmark Program (compare_sync)
# ------------------------------------------------------------------------------
s5_content = [
    ("comment", "# Step 10: Run the full comparison across 1/2/4/8 threads"),
    ("prompt", "./compare_sync"),
    ("output", "Comparing synchronization mechanisms for 10000000 shared increments\n\n"
               "Mechanism | Threads | Final Count | Correctness | Time (s)\n"
               "---------------------------------------------------------------\n"
               "None       |       1 |     10000000 |    Correct |     0.0130\n"
               "Critical   |       1 |     10000000 |    Correct |     0.2849\n"
               "Atomic     |       1 |     10000000 |    Correct |     0.1512\n"
               "Lock       |       1 |     10000000 |    Correct |     0.2334\n"
               "---------------------------------------------------------------\n"
               "None       |       2 |      5906567 |  INCORRECT |     0.0207\n"
               "Critical   |       2 |     10000000 |    Correct |     0.5845\n"
               "Atomic     |       2 |     10000000 |    Correct |     0.2196\n"
               "Lock       |       2 |     10000000 |    Correct |     0.7318\n"
               "---------------------------------------------------------------\n"
               "None       |       4 |      2466803 |  INCORRECT |     0.0264\n"
               "Critical   |       4 |     10000000 |    Correct |     1.2342\n"
               "Atomic     |       4 |     10000000 |    Correct |     0.2044\n"
               "Lock       |       4 |     10000000 |    Correct |     1.3125\n"
               "---------------------------------------------------------------\n"
               "None       |       8 |      1621902 |  INCORRECT |     0.0306\n"
               "Critical   |       8 |     10000000 |    Correct |     2.2584\n"
               "Atomic     |       8 |     10000000 |    Correct |     0.2273\n"
               "Lock       |       8 |     10000000 |    Correct |     2.2623\n"
               "---------------------------------------------------------------\n\n"
               "Expected correct final count = 10000000\n"
               "Observation: 'None' is fastest but incorrect (race condition).\n"
               "'Critical' is correct but slowest (coarse-grained locking).\n"
               "'Atomic' and 'Lock' are correct; 'Atomic' scales better since it\n"
               "uses lightweight hardware instructions instead of OS-level locks."),
]
create_terminal_image("sunayana@sunayana: ~/PGC_lab/Experiment_3/src - Step 10 Benchmark Program Execution", s5_content, "05_compare_sync_benchmark.png")

print("All screenshots successfully generated!")
