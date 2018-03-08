#!/usr/bin/python



import sys
import os

def get_args():
    import argparse
    p = argparse.ArgumentParser(description='Call ShiftN with straightforward process, then call photo_geocode on corrected photo')
    p.add_argument('path', help='Location of one JPG file. GPS Dest Coordinates are required.')

    return p.parse_args()

shiftn_path = 'D:\Programs\ShiftN\ShiftN.exe'

if __name__ == '__main__':
    args = get_args() 
    photo = args.path
    photo_basename = os.path.splitext(photo)[0]
    
    cmd = '{shiftn_path} {photo} {photo_basename}_ShiftN.jpg'.format(shiftn_path = shiftn_path, photo=photo, photo_basename = photo_basename)
    print cmd
    os.system(cmd)
    
    cmd = 'python photo_geocode.py {photo_basename}_ShiftN.jpg'.format(photo_basename = photo_basename)
    print cmd
    os.system(pause)
    os.system(cmd)
    
    
 
 

