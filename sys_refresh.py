import os
import time
import shutil
import subprocess
import sys

# Colors
class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# Function to display a progress bar with percentage
def show_progress(duration):
    interval = 0.1
    total = int(duration / interval)
    
    for i in range(total + 1):
        percent = int((i / total) * 100)
        bar = '#' * (percent // 2) + '-' * (50 - percent // 2)
        sys.stdout.write(f"\r{colors.GREEN}[{bar}]{colors.ENDC} {percent}%")
        sys.stdout.flush()
        time.sleep(interval)
    print()

# Function to display the overall progress bar
def show_overall_progress(current_step, total_steps):
    progress = int((current_step / total_steps) * 100)
    filled = progress // 2
    empty = 50 - filled
    bar = '#' * filled + '-' * empty
    print(f"{colors.GREEN}[{bar}]{colors.ENDC} {progress}%")

total_steps = 3
current_step = 0

# Clear PageCache, dentries, and inodes
print(f"{colors.YELLOW}Attempting to clear PageCache, dentries, and inodes...{colors.ENDC}")
if os.path.exists('/proc/sys/vm/drop_caches'):
    subprocess.run(['sudo', 'sync'])
    result = subprocess.run(['sudo', 'tee', '/proc/sys/vm/drop_caches'], input='3', text=True)
    if result.returncode == 0:
        print(f"{colors.GREEN}PageCache, dentries, and inodes cleared.{colors.ENDC}")
        show_progress(3)
        current_step += 1
    else:
        print(f"{colors.RED}Failed to clear PageCache, dentries, and inodes.{colors.ENDC}")
else:
    print(f"{colors.RED}Skipping cache clearing: /proc/sys/vm/drop_caches not available.{colors.ENDC}")
show_overall_progress(current_step, total_steps)

# Clear swap space
print(f"{colors.YELLOW}Attempting to clear swap space...{colors.ENDC}")
if shutil.which('swapoff') and shutil.which('swapon'):
    result_swapoff = subprocess.run(['sudo', 'swapoff', '-a'])
    result_swapon = subprocess.run(['sudo', 'swapon', '-a'])
    if result_swapoff.returncode == 0 and result_swapon.returncode == 0:
        print(f"{colors.GREEN}Swap space cleared.{colors.ENDC}")
        show_progress(3)
        current_step += 1
    else:
        print(f"{colors.RED}Failed to clear swap space.{colors.ENDC}")
else:
    print(f"{colors.RED}Skipping swap space clearing: swapoff or swapon command not found.{colors.ENDC}")
show_overall_progress(current_step, total_steps)

# Clear package cache
print(f"{colors.YELLOW}Clearing package cache...{colors.ENDC}")
if shutil.which('dnf'):
    result = subprocess.run(['sudo', 'dnf', 'clean', 'all'])
    if result.returncode == 0:
        print(f"{colors.GREEN}Package cache cleared.{colors.ENDC}")
        show_progress(2)
        current_step += 1
    else:
        print(f"{colors.RED}Failed to clear package cache.{colors.ENDC}")
else:
    print(f"{colors.RED}Skipping package cache clearing: dnf command not found.{colors.ENDC}")
show_overall_progress(current_step, total_steps)

print(f"{colors.GREEN}System cleaning operations completed.{colors.ENDC}")
show_overall_progress(total_steps, total_steps)
