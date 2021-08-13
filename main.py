import sys
from os import path
import json
import piexif
from datetime import datetime
from dateutil.parser import parse
from PIL import Image, ExifTags


def get_exif_tag_code(tag_name):
    # This is how we know that the tag code for DateTimeOriginal is 36867
    for k, v in ExifTags.TAGS.items():
        if v == tag_name:
            return k
    return None

def get_json_filename(fpath):
    if path.exists(fpath+'.json'):
        return fpath+'.json'
    pre, ext = path.splitext(fpath)
    if path.exists(pre+'.json'):
        return pre+'.json'
    return None


def get_datetime_from_filename(fpath):
    pre, ext = path.splitext(fpath)
    try:
        dtime = parse(pre)
        return dtime
    except Exception as e:
        return None
    

def get_datetime_from_json(fpath):
    json_fname = get_json_filename(fpath)
    if not json_fname:
        return None
    with open(json_fname) as jf:
        try:
            timestamp = json.load(jf)["photoTakenTime"]["timestamp"]
            return datetime.fromtimestamp(float(timestamp))
        except KeyError:
            return None

def get_new_datetime(fpath):
    return get_datetime_from_json(fpath) or get_datetime_from_filename(fpath)


def update_datetime_if_missing(fpath):
    exif_dict = piexif.load(fpath)
    original_datetime = exif_dict['Exif'].get(36867)
    if not original_datetime:
        new_datetime = get_new_datetime(fpath)
        if not new_datetime:
            print("%s: No new timestamp found" % fpath)
        print("%s: Updating %s" % (fpath, new_datetime))
        exif_dict['Exif'][36867] = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
        piexif.insert(piexif.dump(exif_dict), fpath)
    else:
        print("%s: Keeping at %s" % (fpath, original_datetime))

fpath = sys.argv[1]
update_datetime_if_missing(fpath)
