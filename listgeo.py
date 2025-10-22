import os
import subprocess
import argparse

def has_geo_coordinates(file_path):
    try:
        result = subprocess.run(
            ['exiftool', '-GPSLatitude', '-GPSLongitude', file_path],
            capture_output=True,
            text=True
        )
        return 'GPS Latitude' in result.stdout and 'GPS Longitude' in result.stdout
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main(directory):
    for entry in os.scandir(directory):
        if entry.is_file():
            globe = " 🌍" if has_geo_coordinates(entry.path) else ""
            print(f"{entry.name}{globe}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List files with GPS metadata.")
    parser.add_argument("directory", help="Path to the target directory")
    args = parser.parse_args()
    main(args.directory)
