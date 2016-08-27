#!/usr/bin/env python3
# encoding: utf8
# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
import argparse
import os
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk


def folders(path):
    for entry in scandir(path):
        if not entry.name.startswith(path) and entry.is_dir():
            yield entry.name

def files(path):
    for entry in scandir(path):
       if not entry.name.startswith('.') and entry.is_file():
           yield entry.path


def files_path(path):
    for entry in scandir(path):
       if not entry.name.startswith('.') and entry.is_file():
           yield entry.path, entry.name

def getArgs(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help="directory from which you wish upload images\
                        [defaults to current directory]\n")
    return parser.parse_args(argv)


if __name__ == '__main__':

    args = getArgs()

    directory = args.directory

for d in folders(directory):
    print(d)

print('---')

for f in files(directory):
    print(f)

print('---')

# for f in files_path(directory):
    # print('%s/%s' % f)
    # print('/'.join(str(e) for e in f))
