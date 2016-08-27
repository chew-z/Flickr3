#!/usr/bin/env python3
# encoding: utf8

import re
import os
from configparser import ConfigParser
import argparse


def check_log(flickr, options):
    # searches log with regex - not used at the moment
    logfile = options.log
    filtr = options.regex
    count = 0
    with open(logfile, 'r') as f:
        for line in f.readlines():
            o = re.search(filtr, line)
            if o:
                count += 1
                print (o.group(1))
        if count < 1:
            print("No match found: ", count)
        else:
            print("Matched", count, "lines.")


def is_excluded(path):
    name = os.path.basename(path)
    return (name == 'tags.txt') or (name == 'title.txt')


def is_uploaded(x, logfile):
    # is file x already marked in logfile as uploaded
    line = '+,' + x
    with open(logfile) as file:
        if line in file.read():
            print("Image", x, "already uploaded")
            return True
    return False


def upload_dir(flickr, directory, options):
    # simplified version for testing
    logfile = options.log
    file = options.filename

    print(logfile)
    print(file)

    try:
        files = [('%s/%s' % (directory, x)) for x in os.listdir(directory)]
    except OSError:
        files = []
    print([x for x in files if (os.path.isfile(x) and not is_uploaded(x, logfile))])


def is_valid_file(parser, arg):
    # try: ... except IOError would be better
    if not os.path.isfile(arg):
        # parser.error("The file %s does not exist!" % arg)
        raise argparse.ArgumentTypeError("{0} does not exist".format(arg))
        # raise argparse.ArgumentError(self, "{0} does not exist".format(arg))
    else:
        return open(arg, 'r', encoding='UTF-8')  # return an open file handle


def is_file_valid(parser, arg):
    # alternative to testing file exitence - not tested
    try:
        if os.path.isfile(arg):
            return open(arg, 'r', encoding='UTF-8')
        raise argparse.ArgumentTypeError("{0} does not exist".format(arg))
    except IOError as e:
        # You passed a path that does not exist, or you do not have access to
        # it.
        raise argparse.ArgumentTypeError("{0} does not exist".format(arg))


def getArgs(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help="directory from which you wish upload images")
    # parser.add_argument('-d', '--directory', nargs=1, dest="directory",
    #                     help="directory from whichectory you wish upload images",
    #                     metavar="DIRECTORY")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 2.0')
    parser.add_argument("-q", "--quiet", action="store_false", dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")
    parser.add_argument("-p", "--photoset", dest="photoset",
                        help="name of photoset on flickr.")
    parser.add_argument("-t", "--tags", action="append", dest="tags",
                        help="tags to apply to images")
    recursive = parser.add_mutually_exclusive_group()
    recursive.add_argument('-r', '--recursive', action="store_true",
                           dest="recursive", default=False,
                           help="recursively copy all subdirectories to different photosets")
    recursive.add_argument('-R', '--RECURSIVE', action="store_true",
                           dest="same_recursive", default=False,
                           help="recursively copy all subdirectories to the same photoset. \nOverrides -rr")

    parser.add_argument('-l', '--log', '--logfile', dest="log", default=None,
                        help="log uploaded files")
    parser.add_argument('-c', '--check', action='store_true',
                        help='check logfile for failed uploads')
    parser.add_argument('-re', '--regex',
                        help='regex for filtering files', default='^(.*)$')
    # parser.add_argument("-f", dest="filename", required=False,
    #                     metavar="FILE", type=lambda x: is_valid_file(parser, x),
    #                     help="input file ")
    # FileType objects understand the pseudo-argument '-'
    # and automatically convert this into sys.stdin for readable FileType objects
    # and sys.stdout for writable FileType objects
    # parser.add_argument('-f', '--file', dest="filename", required=True,
    #                     type=argparse.FileType('r', encoding='UTF-8'),
    #                     help="input file (for filtering uploads)")

    return parser.parse_args(argv)


if __name__ == '__main__':

    # print (sys.version)
    config = ConfigParser()
    config.read('flickr.config')
    # filtr = config.get('flickr', 'filtr_regex')
    # print ("Regex: ", filtr)
    args = getArgs()

#    args = parser.parse_args()
    # print(args.directory, args.photoset, args.tags)
    # print(args.verbose, args.check, args.recursive, args.same_recursive)
    # print(args.log, args.regex)
    # print(args.filename)

    # if args.check:
    #     # check_log(None, args)
    #     upload_dir(None, args.directory, args)
    # else:
    #     print("Check is not required")

    upload_dir(None, args.directory, args)
    args.filename.close()
