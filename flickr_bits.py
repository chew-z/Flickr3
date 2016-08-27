# Latest main branch has some additional options checks compared to nisiyama

if args:
    print ("ERROR: Aborting due to unrecognized arguments:\n {}".format("\n\t".join(args)))
    sys.exit(0)

if not options.directory:
    print ("ERROR: You must pass a directory.\nflickr_up.py -d ./images")
    sys.exit(0)

if not options.photoset or not options.tags:
    print ("WARNING")

if not options.photoset:
    print ("You did not pass a name for the photoset.\nWe will use the photoset title '{}'".format(photoset))

if not options.tags:
    print ("You did not pass any tags.\nWill look for tags.txt in folders")


# Regex

'^.*\/(.*\.jpeg)$' '^.*\/(.*\.png)$' '^.*\/(.*\.JPG)$'

'^\+,(.*)$' '^-,(.*)$'

#
