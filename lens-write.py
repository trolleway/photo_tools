#!/usr/bin/python3
# -*- coding: utf8 -*-

import os, subprocess, argparse

parser = argparse.ArgumentParser(
    description="Save to exif lens name, focal lenght, focal lenght in 35mm "
)

cmd = ['/opt/exiftool/exiftool', '-EXIF:FocalLength=50',
'-EXIF:FocalLengthIn35mmFormat=75', "-LensModel=SMC Pentax-A 50mm F2",
       '-overwrite_original', 
    '-preserve',
    '-gps:all', '-ext', '.JPG', 'photos/by_lens/50/75/SMC Pentax-A 50mm F2/']
    
subprocess.run(cmd)

cmd = ['/opt/exiftool/exiftool', '-EXIF:FocalLength=50',
'-EXIF:FocalLengthIn35mmFormat=75', "-LensModel=SMC Pentax-A 50mm F2",
       '-overwrite_original', 
    '-preserve',
    '-gps:all', '-ext', '.DNG', 'photos/by_lens/50/75/SMC Pentax-A 50mm F2/']
    
subprocess.run(cmd)

cmd = ['/opt/exiftool/exiftool', '-EXIF:FocalLength=50',
'-EXIF:FocalLengthIn35mmFormat=75', "-LensModel=SMC Pentax-A 50mm F2",
       '-overwrite_original', 
    '-preserve',
    '-gps:all', '-ext', '.tif', 'photos/by_lens/50/75/SMC Pentax-A 50mm F2/']
    
subprocess.run(cmd)
quit()
