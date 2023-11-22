#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, subprocess, logging, argparse, sys

exiftool_path = 'exiftool'

def image2datetime(path):
    with open(path, "rb") as image_file:
        if not path.lower().endswith('.stl'):
            try:
                image_exif = Image(image_file)

                dt_str = image_exif.get("datetime_original", None)
                dt_obj = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
            except:
                dt_obj = None
                cmd = [exiftool_path, path,
                        "-datetimeoriginal", "-csv"]
                exiftool_text_result = subprocess.check_output(cmd)
                tmp = exiftool_text_result.splitlines()[1].split(b",")
                if len(tmp) > 1:
                    dt_str = tmp[1]
                    dt_obj = datetime.strptime(
                        dt_str.decode("UTF-8"), "%Y:%m:%d %H:%M:%S"
                    )
        elif path.lower().endswith('.stl'):
            dt_obj = None

        if dt_obj is None:
            return None
        return dt_obj


def move_photos_to_date_folders(directory:str):
    # get list of files
    files=list()
    for filename in os.listdir(directory):
        is not os.path.isdir(filename):
            files.append(filename)
    # READ DATE
    for file in filenames:
        dt_obj = image2datetime(file)
        if dt_obj is None:
            continue
        yyyymmdd=dt_obj.strftime("%Y-%m-%d")

        # CREATE DIRECTORY
        new_folder_path = os.path.join(directory,yyyymmdd)
        if not os.path.exists(new_folder_path):
            os.mkdirs(new_folder_path)
        
        # MOVE
        shutil.move(filename, new_folder_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="Move photos to subfolders by date, like 2032-05-26")

    parser.add_argument('dir', type=str, required=True, help='Catalog with photos')

    args = parser.parse_args()
    move_photos_to_date_folders(args.dir)