import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


# Directory containing the photos
BASE_DIR = "/mnt/2022backup/photos_backup_2003-2019/_THEMATICS"
OUTPUT_DIR = "../photosgeo"
from concurrent.futures import ThreadPoolExecutor
FINAL_OUTPUT = os.path.join('/mnt/2022backup/', "geo.geojsonseq")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
for file in Path(OUTPUT_DIR).glob("*"):
    if file.is_file():
        file.unlink()

# Get list of subdirectories at depth 1
subdirs = [f.path for f in os.scandir(BASE_DIR) if f.is_dir()]

# Run geo.py for each directory

# Function to run geo.py for a single directory
def process_subdir(subdir):
    subdir_name = os.path.basename(subdir)
    output_file = os.path.join(OUTPUT_DIR, f"{subdir_name}.geojsonseq")
    subprocess.run(["python3", "geo.py", subdir, "--output", output_file], check=True)

# Run geo.py in parallel using ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    executor.map(process_subdir, subdirs)

# Concatenate all output files into one using 'cat'
output_files = str(Path(OUTPUT_DIR) / "*.geojsonseq")
subprocess.run(f"cat {output_files} > {FINAL_OUTPUT}", shell=True, check=True)

print(f"Processing complete. Final output saved to {FINAL_OUTPUT}")
