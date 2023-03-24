#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, subprocess

directory='dirname'
jpg_exts=('jpg')
raw_exts=('dng','orf')
for src_extension in jpg_exts:
    for dst_extension in raw_exts:
        cmd = ['exiftool', '-tagsfromfile', '%d%f'+src_extension, '-gps:all', '-ext', dst_extension, directory]
        proc = subprocess.Popen(cmd)
        print("the commandline is {}".format(proc.args)) 