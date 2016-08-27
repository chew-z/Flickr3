#!/usr/bin/env python3

import os
import argparse
from configparser import ConfigParser
import logging
import re
import webbrowser
import flickrapi
import flickr_cli
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


def read_items(path):
    items = []
    if os.path.exists(path):
        try:
            fd = open(path)
            items = [line.rstrip()
                     for line in fd if re.search(r'^\S.*$', line) is not None]
            fd.close()
        except IOError as e:
            logging.warning(e)
    return items


def make_tags(dir, tags):
    set0 = set(tags or [])
    set1 = set(read_items('%s/tags.txt' % dir))
    return set0.union(set1)


def make_title(dir, pset):
    items = read_items('%s/title.txt' % dir)
    if len(items) > 0:
        return items[0]
    return pset


def photoset_default_title(d):
    name = os.path.basename(os.path.normpath(d))
    return make_title(d, name)


def is_excluded(path):
    name = os.path.basename(path)
    return (name == 'tags.txt') or (name == 'title.txt') or (name == '.DS_Store')


def is_uploaded(x, logfile):
    # is file x already marked in logfile as uploaded
    line = '+,' + x
    with open(logfile) as file:
        if line in file.read():
            print("Image", x, "already uploaded")
            return True
    return False


def upload_dir_rec0(flickr, directory, depth, tags, photoset, options):
    tags0 = tags or make_tags(directory, options.tags) or ""
    photoset0 = photoset or photoset_default_title(directory)
    log = options.log

    try:
        # files = [('%s/%s' % (directory, x)) for x in os.listdir(directory)]
        files = files(directory)
        dirs = folders(directory)
    except OSError:
        files = []
        dirs = []
    # regs = [x for x in files if (os.path.isfile(
    #    x) and not is_excluded(x) and not is_uploaded(x, log))]
    regs = [x for x in files if (not is_excluded(x) and not is_uploaded(x, log))]
    # dirs = [x for x in files if os.path.isdir(x)]
    files = None

    print(directory, tags0, photoset0)

    upload = flickr_cli.DirectoryFilesFlickrUpload(flickr)
    upload(directory=directory, files=regs, pset=photoset0, tags=tags0,
           log=log)
    for subdir in dirs:
        upload_dir_rec0(flickr, subdir, depth + 1, tags, photoset, options)


def upload_dir_rec(flickr, options):
    directory = options.directory
    if options.same_recursive:
        tags = make_tags(directory, options.tags) or ""
        photoset = options.photoset or photoset_default_title(directory)
    else:
        tags = None
        photoset = None

    upload_dir_rec0(flickr, directory, 0, tags, photoset, options)


def upload_dir(flickr, options):
    directory = options.directory
    log = options.log
    tags = make_tags(directory, options.tags) or ""
    photoset = options.photoset or photoset_default_title(directory)

    print(directory, tags, photoset)

    upload = flickr_cli.DirectoryFlickrUpload(flickr)
    upload(directory=directory, pset=photoset, tags=tags,
           log=log)


def divide_files_by_dir(files):
    dir2files = dict()
    for file in files:
        dir = os.path.dirname(file)
        if dir not in dir2files:
            dir2files[dir] = []
        dir2files[dir].append(file)
    return list(dir2files.items())


def upload_files(flickr, directory, files, options):
    tags = make_tags(directory, options.tags) or ""
    photoset = options.photoset or photoset_default_title(directory)
    log = options.log

    print(files, tags, photoset)

    upload = flickr_cli.DirectoryFilesFlickrUpload(flickr)
    upload(directory=directory, files=files, pset=photoset, tags=tags,
           log=log)


def getArgs(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help="directory from which you wish upload images\
                        [defaults to current directory]\n")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 2.0')
    parser.add_argument("-q", "--quiet", action="store_false", dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")
    parser.add_argument("-p", "--photoset", dest="photoset",
                        help="name of photoset on flickr.")
    parser.add_argument("-t", "--tags", action="append", dest="tags",
                        help="tags to apply to images")
    parser.add_argument('-l', '--log', '--logfile', dest="log", default=None,
                        help="log keeps track of uploaded files")
    recursive = parser.add_mutually_exclusive_group()
    recursive.add_argument('-r', '--recursive', action="store_true",
                           dest="recursive", default=False,
                           help="recursively copy all subdirectories to \
                        different photosets")
    recursive.add_argument('-R', '--RECURSIVE', action="store_true",
                           dest="same_recursive", default=False,
                           help="recursively copy all subdirectories to \
                        the same photoset. Overrides -r")

    return parser.parse_args(argv)

if __name__ == '__main__':

    args = getArgs()

    config = ConfigParser()
    config.read('flickr.config')
    api_key = config.get('flickr', 'key')
    secret = config.get('flickr', 'secret')
    flickr = flickrapi.FlickrAPI(api_key, secret)

    if not flickr.token_valid(perms='write'):
        flickr.get_request_token(oauth_callback='oob')
        authorize_url = flickr.auth_url(perms='write')
        webbrowser.open_new_tab(authorize_url)
        verifier = str(input('Verifier code: '))
        flickr.get_access_token(verifier)

    upload_dir_rec(flickr, args)
