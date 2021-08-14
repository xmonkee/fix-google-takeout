# fix-google-takeout

## Warning
Probably buggy, use at your own risk. Backup your photos. 

## Overview
Google takeout (https://takeout.google.com/settings/takeout) for photos mangles the datetime EXIF data for some reason. The original datetime is available in metadata json files that accompany that download. This program attempts to use that metadata to fix the datetime in the jpeg's EXIF data.

## Installation
Prerequisites: python3
git clone this repo and run `make`

## Execution
./fix-google-takeout /path/to/extracted/photos
