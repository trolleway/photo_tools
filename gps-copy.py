#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, subprocess

directory='photos'
jpg_exts=list()
jpg_exts.append('.jpg')
raw_exts=('dng','orf')
for src_extension in jpg_exts:
    for dst_extension in raw_exts:
        cmd = ['/opt/exiftool/exiftool', '-tagsfromfile', 
               '%d%f'+src_extension, 
               '-overwrite_original', 
            '-preserve',
            '-gps:all', '-ext', dst_extension, directory]

        subprocess.run(cmd)
