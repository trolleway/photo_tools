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
            #"-filecreatedate<SubSecDateTimeOriginal", 
            #"-SubSecDateTimeOriginal<datetimeoriginal",
            '-preserve',
            #'-EXIF:OffsetTime*=+3:00',
            #"-FileModifyDate<EXIF:DateTimeOriginal",
            
            '-gps:all', '-ext', dst_extension, directory]

        subprocess.run(cmd)
        #proc = subprocess.Popen(cmd)
        #print("the commandline is {}".format(proc.args)) 

        for root, dirs, files in os.walk(directory):
            for name in files:
                
                if name.upper().endswith(dst_extension.upper()):

                    cmd = ['/opt/exiftool/exiftool', '-DateTimeOriginal', '-s',
                    '-t', '-d', '''%Y%m%d%H%M.%S''', 
                    '-csv','-csvDelim',';' ,
                    os.path.join(directory,name),
                    ]
                    
                    photo_timestamp = subprocess.check_output(cmd).decode()
                    photo_timestamp = photo_timestamp.splitlines()[-1]
                    photo_timestamp = photo_timestamp.rpartition(';')[-1]
                    
                    #print(photo_timestamp)
                    #cmd = ['TZ=UTC ','touch','-t',photo_timestamp,os.path.join(directory,name)]
                    #subprocess.run(cmd)

    