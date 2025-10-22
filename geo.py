#!/usr/bin/env python3
# -*- coding: utf8 -*-

import argparse
import subprocess
import os
import sys

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process photos with exiftool and save output to GeoJSONSEQ format.')
    parser.add_argument('directory', type=str, help='The input directory containing the photos')
    parser.add_argument('--output', type=str, default='photos.geojsonseq', help='The output filename (default: photos.geojsonseq)')
    args = parser.parse_args()

    # Check if the source directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: The directory '{args.directory}' does not exist.")
        sys.exit(1)

    # Run the exiftool command
    command = [
        'exiftool',
        '-p', 'fmt_files/geojsonseq.fmt',
        '-f',
        '-api', 'missingtagvalue=null',
        '-m',
        '-r', '"'+args.directory+'"',
        '>',
        '"'+args.output+'"'
    ]
    # Use subprocess to run the command
    subprocess.run(' '.join(command), shell=True, check=True)

if __name__ == '__main__':
    main()
