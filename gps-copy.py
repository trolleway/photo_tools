#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, subprocess, argparse

directory='photos'
jpg_exts=list()
jpg_exts.append('.jpg')
raw_exts=('dng','orf','nef','mpo','tif')

parser = argparse.ArgumentParser(description='copy exif from jpg files in folder '+directory+' to RAW files with same name and extensions '+' '.join(raw_exts))

parser.add_argument('mode', type=str, choices=['gps','all'], default='gps', help='copy location only or copy all tags')
args = parser.parse_args()

for src_extension in jpg_exts:
    for dst_extension in raw_exts:
        print(f'copy tags from {src_extension} to {dst_extension}')
        cmd = ['exiftool', '-tagsfromfile', 
               '%d%f'+src_extension, 
               '-overwrite_original', 
            '-preserve',
            '-gps:all', '-ext', dst_extension, directory]

        subprocess.run(cmd)
