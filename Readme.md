# fix-google-takeout

## Warning
Use at your own risk. Backup your photos. 

## Overview
Google takeout (https://takeout.google.com/settings/takeout) for photos mangles the datetime EXIF data for some reason. The original datetime is available in metadata json sidecar files that accompany the images. This program attempts to use that metadata to fix the datetime in the jpeg's EXIF data.

## Installation
Prerequisites: python3

git clone this repo and run `make`

## Execution
```
./fix-google-takeout -h

usage: fix-google-takeout [-h] [--show] [-r] target

Fix DateTimeOriginal EXIF tag for Google Takeout images based on data in colocated json files

positional arguments:
  target           file or directory to fix

optional arguments:
  -h, --help       show this help message and exit
  --show           show (don't fix) the current DateTime
  -r, --recursive  fix all files in all subdirectories
```
