import pandas as pd
import numpy as np 
import glob
import os 
from os.path import isfile as os_file
from os.path import isdir as os_dir
from os.path import basename as os_base

from joblib import Parallel, delayed

from os import stat as os_stat
import pathlib
from tqdm import tqdm as tqdm
import datetime



import imagehash
from PIL import Image
from PIL.ExifTags import TAGS




def convert_time(t_time):
    date_t = datetime.date.fromtimestamp(t_time)
    return date_t.year, date_t.month, date_t.day



def get_file_info(filepath):
        file_extension = pathlib.Path(filepath).suffix
        file_name = os_base(filepath)
        is_dir = os_dir(filepath)
        is_file = os_file(filepath)
        file_size = os.path.getsize(filepath)

        
        ctime = os.path.getctime(filepath)
        ctime_YYYY, ctime_MM, ctime_DD = convert_time(ctime)
        
        mtime = os.path.getmtime(filepath)
        mtime_YYYY, mtime_MM, mtime_DD = convert_time(ctime)
        
        img_hash_str = ""
        try:
            img_hash_str = str(imagehash.average_hash(Image.open(filepath)))
        except Exception as e:
            pass
        
        record = {
            "fname": file_name,
            "ext":file_extension,
            "is_dir": is_dir,
            "is_file":is_file,
            "size":file_size,
            "img_hash_str":img_hash_str,
            "ctime":ctime,
            "ctime_YYYY":ctime_YYYY,
            "ctime_MM":ctime_MM,
            "ctime_DD":ctime_DD,
            "mtime":mtime,
            "mtime_YYYY":mtime_YYYY,
            "mtime_MM":mtime_MM,
            "mtime_DD":mtime_DD,
            "path":filepath,
        }
        return record


def main(basedir, output_path, n_cpus = 6):
    records = []
    records = Parallel(n_jobs=n_cpus)(delayed(get_file_info)(filepath) for filepath in tqdm(glob.iglob(basedir, recursive=True)))
    df_records = pd.DataFrame.from_records(records)
    df_records.to_json(output_path)


if __name__ == '__main__':
    basedir = "/Volumes/ssd-0/old-photo-organize/MyPhotoVideoAudio/**"
    output_path = "/Volumes/ssd-0/old-photo-organize/MyPhotoVideoAudio-meta.json"
    main(basedir, output_path)
    
    basedir = "/Volumes/ssd-0/old-photo-organize/google-photo-dump-20230220/**"
    output_path = "/Volumes/ssd-0/old-photo-organize/google-photo-dump-20230220-meta.json"
    main(basedir, output_path)
