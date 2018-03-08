#!/usr/bin/python

#Call ShiftN with dtraightforward process, then call photo_geocode on corrected photo

import sys
import os

shiftn_path = 'D:\Programs\ShiftN\ShiftN.exe'

os.system('{shiftn_path} {photo} {photo_basename}_ShiftN.jpg'.format(shiftn_path = shiftn_path))
os.system('python photo_geocode.py {photo_basename}_ShiftN.jpg'.format(shiftn_path = shiftn_path))
