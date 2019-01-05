"""
    Convert an AAX file to MP3, splitted by chapters.
"""
import os
import sys
import re
import argparse
from subprocess import Popen, PIPE
from ffmpeg_split import ffmpeg_split

_SCRIPT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))


def run_cmd(cmd, cwd=None, show_out=False):
    """
        Run a subprocess in the specified cwd.
        Return status code, stdout and stderr.
    """
    process = Popen(
        cmd,
        cwd=cwd,
        stdout=PIPE,
        stderr=sys.stdout if show_out else PIPE,
        universal_newlines=True,
    )
    stdout, stderr = process.communicate()
    return_code = process.returncode
    return (return_code, stdout, stderr)


def get_checksum(input_file):
    """
        Get the .aax checksum using ffprobe.
    """
    _, _, stderr = run_cmd(['ffprobe', input_file])
    checksum = re.findall('checksum == (.*)', stderr)[0]
    return checksum


def get_activation_bytes(input_file=None, checksum=None):
    """
        Get the activation bytes from the .aax checksum using rainbow tables.
        None is returned if the activation bytes can't be computed.
    """
    if (not input_file and not checksum) or (input_file and checksum):
        raise ValueError('Please specify only one of [input_file, checksum]')
    if input_file:
        checksum = get_checksum(input_file)
    _, stdout, _ = run_cmd(
        ['./rcrack', '.', '-h', checksum],
        cwd=os.path.join(_SCRIPT_PATH, 'tables')
    )
    activation_bytes = re.findall('hex:(.*)', stdout)[0]
    return activation_bytes


def aax_to_mp3(activation_bytes, input_file, output_file):
    """
        Convert an AAX to MP3 using ffmpeg with the specified activation bytes.
        The output is printed to the real stdout for showing progress.
    """
    run_cmd([
        'ffmpeg', '-y', '-activation_bytes', activation_bytes,
        '-i', input_file, '-ab', '192k', '-vn', output_file
    ], show_out=True)


def main(
        input_file,
        output_file=None,
        activation_bytes=None,
        split_only=False,
        convert_only=False
):
    """
        Main.
    """
    print('Opening {}'.format(input_file))

    if not split_only:
        if activation_bytes:
            print('Using {} as activation bytes'.format(activation_bytes))
        else:
            activation_bytes = get_activation_bytes(input_file=input_file)
            if not activation_bytes:
                print('An error occured getting the activation_bytes')
                return

        if output_file and not output_file.endswith('.mp3'):
            # add file extension if not already specified
            output_file += '.mp3'
        elif not output_file:
            # Save the .mp3 output in the same folder as the .aax
            output_file = input_file.replace('.aax', '.mp3')

        # Heavier task: conversion from .aax to .mp3
        print('Converting...')
        aax_to_mp3(activation_bytes, input_file, output_file)

    if not convert_only:
        # Split a single .mp3 into multiple files based on chapters,
        # the files are put in a folder with the same name of the original mp3
        print('Splitting chapters...')
        chapters = ffmpeg_split.get_chapters(
            input_file if split_only else output_file
        )
        ffmpeg_split.convert_chapters(chapters)
        try:
            # Try to delete monolithic mp3 after splitting it.
            os.remove(input_file if split_only else output_file)
        except FileNotFoundError:
            pass

    print('All jobs ended!')
    print('Activation bytes: {}'.format(activation_bytes))
    print('To speed up a little, next time you can use:')
    print('python convert.py -a {} yourfilename.aax'.format(activation_bytes))


if __name__ == '__main__':
    """
        Use a parser to get CLI flags.
    """
    PARSER = argparse.ArgumentParser(
        description='Convert an AAX audio file into multiple MP3 file, one for\
                     each chapter.',
        epilog='Source code: https://github.com/Pitasi/aax-to-mp3',
    )
    PARSER.add_argument(
        'file',
        help='AAX audio file to be converted,\
              or MP3 to be splitted if --split-only is used',
    )
    PARSER.add_argument(
        '-o',
        '--output',
        help='output folder for the chapter files, or output file path if\
              --split-only is used',
    )
    PARSER.add_argument(
        '-a',
        '--act-bytes',
        help='activation bytes for decoding the AAX to MP3',
        dest='bytes',
    )
    GROUP = PARSER.add_mutually_exclusive_group()
    GROUP.add_argument(
        '-s',
        '--split-only',
        help='split a MP3 file into chapters without converting it',
        action='store_true',
    )
    GROUP.add_argument(
        '-c',
        '--convert-only',
        help='convert the AAX file to MP3 without splitting it into chapters',
        action='store_true',
    )
    ARGS = PARSER.parse_args()

    main(
        ARGS.file,
        output_file=ARGS.output,
        activation_bytes=ARGS.bytes,
        split_only=ARGS.split_only,
        convert_only=ARGS.convert_only
    )
