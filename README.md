# README.md


## What is it?

This is my repository for code I have used in managing my Flickr and mac OS Photos. Mostly extracting images from Photos and uploading them to Flickr.

It consists of code from separate projects.

- [export_photos.py](https://github.com/AaronVanGeffen/ExportPhotosLibrary) and also [ExportPhotosLibrary.py](https://github.com/tymmej/ExportPhotosLibrary) for exporting Photos to folders.
- [flickr_up.py](https://github.com/nisiyama/Flickr-Cli) - for uploading images to Flickr.

So the code isn't mine I just store it here as a backup of my project. I have modfied this code a little for my needs. 

## Export Photos Library

I have used [export_photos.py](https://github.com/AaronVanGeffen/ExportPhotosLibrary) with some minor changes. Mostly some files inside Photos Library.photoslibrary had different names and locations.

There are other working versions of this code on Github for example [ExportPhotosLibrary.py](https://github.com/tymmej/ExportPhotosLibrary) with minor differences in logic and dependencies. I like [export_photos.py](https://github.com/AaronVanGeffen/ExportPhotosLibrary). It works fine.

## Flickr-Cli

[Flickr-Cli](https://github.com/jmahmood/Flickr-Cli) is a tool for uploading images to Flickr from comandline.[^1] 

[^1]: Uploading images from directory to Flickr, not syncing with Flickr,  remember that there is a difference. Try [folders2flickr
](https://github.com/richq/folders2flickr) or [flickr-uploader](https://github.com/trickortweak/flickr-uploader) if you are looking for syncing. Somehow I didn't like the code, I think it carries too much baggage (Flickr-Cli seems like much modern code)

I have started from **Flickr-Cli** branch by [nishiyama](https://github.com/jmahmood/Flickr-Cli/pulls/nisiyama), who has added some interesting features to **Flickr-Cli**.

    command line specification of photos to be uploaded
    recursive uploading of photos in directories.
    obtaining photoset name and tags from text files in each photo directory.
    output upload log (-l option) e.g. +,/path/to/succeded/photo -,/path/to/failed/photo

And then I started making mistakes on my own account.

## Done

- convert to python3, quite easy
```
    2to3 -w *.py
    pip3 install -r requirements.txt
```
- fixed bug in joining tags from file EXIF with tags from tags.txt
```
    self.tags = (' '.join('"' + item + '"' for item in tags))
```
- now using argparse insead of optparse

I have been playing with argparse with fuzzy vision of what I want from it in the (not too distant) future . ~~Some options are not handled by argparse but implemented in a code.~~

- log file is now opened for appending not writing so it is not flushed on each run. Just remember to delete logfile if you want to start anew.
```
                 # fd = open(path, 'w', 1)
                 fd = open(path, 'a', 1)
```
- on second and following runs (using the same logfile) we are uploading only imges that has't been already uploaded. It is usefull cause there are always some fails when uploading large folders, we could also no safely stop the upload without starting over from zero.

## ToDo (some day)

- optimize is_uploaded(x, file)

- filtering files to upload using regex

- after uploading try re-uploading failed files automatically

- put log file (history) in each directory (subdirectory?) by default

- add dry run

- add .ignore file for files like '.DS_Store' etc.
