#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, subprocess

directory='photos'
jpg_exts=list()
jpg_exts.append('.jpg')

proxies_dir=os.path.join(directory,'geo_ok')


if os.path.isdir(proxies_dir):
    raw_exts=('dng','orf','nef','jpg','JPG')
    for src_extension in jpg_exts:
        for dst_extension in raw_exts:
            cmd = ['/opt/exiftool/exiftool', '-tagsfromfile', 
               proxies_dir+'/'+'%f'+src_extension, 
               '-overwrite_original', 
            '-preserve',
            '-gps:all', '-ext', dst_extension, directory]
            
            print(' '.join(cmd))

            subprocess.run(cmd)
else:
    print('not found proxies dir: '+proxies_dir)