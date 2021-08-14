import sys
import re
import os
from os import path
import json
import piexif
import argparse
from datetime import datetime
from dateutil.parser import parse


DATETIMEORIGINAL = 36867
logfile = [None]


def lprint(s):
    print(s)
    logfile[0].write(s+"\n")


def show_datetime(fpath):
    exif_dict = piexif.load(fpath)
    lprint(f"{fpath}: {exif_dict['Exif'].get(DATETIMEORIGINAL)}")
    return None


def get_json_filename(fpath):
    if path.exists(fpath + ".json"):
        return fpath + ".json"
    if path.exists(fpath + ".JSON"):
        return fpath + ".JSON"
    pre, ext = path.splitext(fpath)
    if path.exists(pre + ".json"):
        return pre + ".json"
    if path.exists(pre + ".JSON"):
        return pre + ".JSON"
    if pre.endswith("-edited"):
        pre = re.sub("-edited$", "", pre)
        return get_json_filename(pre + ext)
    return None


def get_new_datetime(fpath):
    json_fname = get_json_filename(fpath)
    if not json_fname:
        return None
    with open(json_fname) as jf:
        try:
            timestamp = json.load(jf)["photoTakenTime"]["timestamp"]
            return datetime.fromtimestamp(float(timestamp))
        except KeyError:
            return None


def update_datetime(fpath):
    exif_dict = piexif.load(fpath)
    original_datetime = exif_dict["Exif"].get(DATETIMEORIGINAL)
    if original_datetime is not None:
        lprint("%s: Keeping at %s" % (fpath, original_datetime))
        return
    new_datetime = get_new_datetime(fpath)
    if not new_datetime:
        lprint("%s: No timestamp found" % fpath)
        return
    lprint("%s: Updating %s" % (fpath, new_datetime))
    exif_dict["Exif"][36867] = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
    piexif.insert(piexif.dump(exif_dict), fpath)


def recursively_operate(target, operation):
    for root, dirs, files in os.walk(target):
        for name in files:
            if name.lower().endswith("jpg") or name.lower().endswith("jpeg"):
                try:
                    operation(path.join(root, name))
                except Exception as e:
                    lprint("Could not operate %s: %s" % (name, str(e)))


def main(target, operation, recursive):
    if path.isdir(target):
        if not recursive:
            print("-r must be specified when targetting a directory")
            return
        recursively_operate(target, operation)
        return
    if path.isfile(target):
        if not target.lower().endswith("jpg") and not target.lower().endswith("jpeg"):
            print("only works for JPGs")
            return
        operation(target)
        return
    print("target is neither file nor directory")


parser = argparse.ArgumentParser(
    prog="fix-google-takeout",
    description="Fix DateTimeOriginal EXIF tag for Google Takeout images based on data in colocated json files",
)
parser.add_argument("target", help="file or directory to fix")
parser.add_argument(
    "--show",
    dest="operation",
    action="store_const",
    const=show_datetime,
    default=update_datetime,
    help="show (don't fix) the current DateTime",
)
parser.add_argument(
    "-r",
    "--recursive",
    dest="recursive",
    action="store_const",
    const=True,
    default=False,
    help="fix all files in all subdirectories",
)

if __name__ == "__main__":
    args = parser.parse_args()
    logfile[0] = open("fix-google-takeout.log", "w")
    main(args.target, args.operation, args.recursive)
    logfile[0].close()
