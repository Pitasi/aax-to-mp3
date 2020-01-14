# AAX to MP3 script

This script is the simplest way to convert a AAX audio file type to a more
readable MP3 format. It uses `ffmpeg` and these [rainbow
tables](https://github.com/inAudible-NG/tables) to decrypt the file.

By default, the file is also splitted into multiple MP3s by chapters.

This little script aims to automize some tasks and to get the possibility of
using common audio players to reproduce Audible's audiobooks.


# Requirements

First of all: Python 3. You probably already have it, if you don't please
search on internet how to install it in your system.

Then clone this repo and the submodules, with:
```sh
$ git clone --recurse-submodules -j8 https://github.com/Pitasi/aax-to-mp3
```

Modern versions of `ffmpeg` and `ffprobe` are needed in the PATH. In Arch Linux
it's easily done by:
```sh
$ sudo pacman -S ffmpeg
```
I'm sure every distro has something like that.

If you want to use the `set_album_art.py` script
(which is not really part of the conversion, it just set the MP3 album cover 
image) you must install the `mutagen` module:
https://mutagen.readthedocs.io/en/latest/

For Arch Linux:
```sh
$ sudo pacman -S python-mutagen
```


# How to use the script
```
$ python convert.py -h

usage: convert.py [-h] [-o OUTPUT] [-a BYTES] [-s | -c] file

Convert an AAX audio file into multiple MP3 file, one for each chapter.

positional arguments:
  file                  AAX audio file to be converted, or MP3 to be splitted
                        if --split-only is used

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output folder for the chapter files, or output file
                        path if --split-only is used
  -a BYTES, --act-bytes BYTES
                        activation bytes for decoding the AAX to MP3
  -s, --split-only      split a MP3 file into chapters without converting it
  -c, --convert-only    convert the AAX file to MP3 without splitting it into
                        chapters

```

The basic usage is something like this:
```sh
$ python convert.py ~/path/to/file.aax
```

it will process `file.aax` extracting you `activation bytes` (a sort of a 
password needed to decrypt the file), convert to the MP3 format, then split this
file into many smaller ones (one for each chapter).

After that I usually download the cover image from Audible (i.e. 
https://www.audible.it/pd/B07CMD6CFX) and save it as `AlbumArt.jpg` in the same
folder of the chapter files.
Then by running:
```sh
$ python set_album_art.py path/to/chapters
```
the image is embedded inside the files and recognized by every audiobooks
reader.

# Docker
In some cases the pre built docker image may be useful to use. For example 
when running on an unsupported environment (macOS).
```
docker run -v <path to>/file.aax:/tmp adamcathersides/aax-mp3:latest -o /tmp/file.aax /tmp/file.mp3
```

# In case of problems
Fill an issue and I will try to help you!

Also, pull requests are welcome here.
