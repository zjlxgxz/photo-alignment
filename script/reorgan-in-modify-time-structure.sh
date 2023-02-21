#!/bin/bash

# This script moves files from SRC_DIR to empty TGT_DIR by their modified time:
# The orginal purpose it to re-org photo backups in messy-organized folders
# TGT_DIR/YYYY/MM/dd/file1.jpg
# 1. It checks white space in folder/file names, and replace white spaces 
#   with underscores
# 2. It create files and use gmv, if any path conflict occurs (same name), it 
#   will use ~number~ as the suffix after file extension to avoid overwriting.

SRC_DIR=/Volumes/ssd-0/old-photo-organize/MyPhotoVideoAudio
TGT_DIR=/Volumes/ssd-0/old-photo-organize/re-org
# cd "$TGT_DIR"
# setfile -d "01/13/2021 24:59:59" ./test.t

echo 'checking filename with space'
# find $SRC_DIR -type f -not -path '*/.*' -exec rename "s/\s/_/g" {} \;
find $SRC_DIR -depth -name "* *" -not -path '*/.*' -execdir rename 's/ /_/g' "{}" \;

# for file in $(find $SRC_DIR -type f -name "* *" -print0); do
#     echo $file
# done

echo 'checked space '

for file in $(find $SRC_DIR -type f -not -path '*/.*' ); do
    # Top tear folder name
    year=$(stat -f "%Sm" -t "%Y" $file)
    month=$(stat -f "%Sm" -t "%m" $file)
    day=$(stat -f "%Sm" -t "%d" $file)
    filename=$(basename $file) 
    # Secondary folder name
    # subfolderName=$(stat -f "%Sm" -t "%d-%m-%Y" $file)
    # echo "$file $filename $year $month $day"

    tgt_folder_path="$TGT_DIR/$year/$month/$day"
    tgt_file_path="$tgt_folder_path/$filename"
    echo " $file => $tgt_file_path"

    if [ ! -d "$tgt_folder_path" ]; then
        mkdir -p "$tgt_folder_path"
        echo "starting new folder: $tgt_folder_path"
    fi
    # echo "gmv --backup=numbered $file $tgt_file_path"
    gmv --backup=numbered $file $tgt_file_path
done
