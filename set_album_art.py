"""
    Simple CLI tool to embed AlbumArt.jpg in the MP3 files tags contained in
    the same folder.
"""
import os
import argparse
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


def set_file_art(file_path, art_path):
    """
        Set art_path as cover image of file_path.
    """
    audio = ID3(file_path)
    with open(art_path, 'rb') as art:
        audio['APIC'] = APIC(
            encoding=3, # 3 is for utf-8
            mime='image/jpeg',
            type=3, # 3 is for the cover image
            desc=u'Cover',
            data=art.read()
        )
    audio.save(None)


def main(folder_path):
    """
        List file of folder_path and loop through them setting the cover image.
    """
    path = os.path.expanduser(folder_path)
    audio_files = [
        os.path.join(path, f)
        for f in os.listdir(path) if 'mp3' in f
    ]
    art_path = os.path.join(path, 'AlbumArt.jpg')
    if not os.path.isfile(art_path):
        print('No cover art found! Plese be sure to add an AlbumArt.jpg or \
               in the same folder of the MP3 files.')
        return
    for file_path in audio_files:
        set_file_art(file_path, art_path)
    print('Done!')


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Embed AlbumArt.jpg cover art in all MP3s of the specified\
                     folder.',
        epilog='Source code: https://github.com/Pitasi',
    )
    PARSER.add_argument(
        'folder',
        help='Path of the folder containing MP3 files and AlbumArt.jpg',
    )
    ARGS = PARSER.parse_args()
    main(ARGS.folder)
