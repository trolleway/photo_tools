#!/usr/bin/env python3
# -*- coding: utf8 -*-



import os, subprocess,  sys, shutil, argparse

from PIL import Image
exiftool_path = '/opt/exiftool/exiftool'

def mpo_convert(folder,format):
   assert os.path.isdir(folder)
   if format=='jpg_pairs':
        convert_jpg_pairs(folder)
   elif format=='tif_multipage':
        convert_tiff_multipage(folder)

def convert_tiff_multipage(folder):
    # loop through all files in the folder
    for file in os.listdir(folder):
        # check if the file is an mpo file
        if file.endswith(".mpo") or file.endswith(".MPO"):
            # remove the file extension
            base = file[:-4]
            # create a subfolder with the same name as the file
            dstdir=os.path.join(folder, 'tifs')
            os.makedirs(dstdir, exist_ok=True)
            # open the mpo file as an image
            src_filename = os.path.join(folder, file)
            im = Image.open(src_filename)
            # get the number of frames in the mpo file
            nframes = im.n_frames
            # loop through each frame
            assert nframes==2
            im1=im
            im.seek(0)
            dst_filename=os.path.join(dstdir, f"{base}.tif")
            im1.save(dst_filename, 
                     format="TIFF", 
                     #append_images=[im2], 
                     compression='jpeg',
                     quality=96,
                     save_all=True)
            # copy exif
            # pil fails while saving some tags to tif
            
            cmd = [exiftool_path, '-overwrite_original', 
    '-preserve','-TagsFromFile', src_filename,
                   '-all:all>all:all', dst_filename]
            subprocess.run(cmd)
         
def convert_jpg_pairs(folder):
                
    # loop through all files in the folder
    for file in os.listdir(folder):
        # check if the file is an mpo file
        if file.endswith(".mpo") or file.endswith(".MPO"):
            # remove the file extension
            base = file[:-4]
            # create a subfolder with the same name as the file
            dstdir=os.path.join(folder, 'jpegs')
            os.makedirs(dstdir, exist_ok=True)
            # open the mpo file as an image
            im = Image.open(os.path.join(folder, file))
            # get the number of frames in the mpo file
            nframes = im.n_frames
            # loop through each frame
            for i in range(nframes):
                # seek to the frame
                im.seek(i)
                # save the frame as a tiff file in the subfolder
                im.save(os.path.join(dstdir, f"{base}_{i+1}.jpg"))
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="Convert MPO stereo photo file to tiff or jpg")

    parser.add_argument('dir', type=str, help='Catalog with photos')
    parser.add_argument('format', type=str, choices=['jpg_pairs','tif_multipage'], help='output file formats')

    

    args = parser.parse_args()
    mpo_convert(args.dir,args.format)