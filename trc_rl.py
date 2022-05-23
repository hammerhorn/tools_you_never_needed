#!/usr/bin/env python3
"""
Depends: abc2midi, abcm2ps, ghostscript, imagemagick, python-termcolor,
         sox, timidity/timidity++, (configured with a soundfont if
         necessary, e.g., timidity-freepats))
"""
#print("Std Lib")
import argparse
import atexit
import readline
import subprocess
import sys
#import threading

#print("3rd party")
from termcolor import colored

#print("local")
from tonerow import Tonerow
import misc
import termctl
import fileio
import rlif

__author__ = 'Chris Horn <hammerhorn@gmail.com>'


#SQUAD_GOALS = """
#    - generate full 2-d matrix
#    - the ability to input specific rows instead of generating them
#    - Save as text
#    - Save as audio file
#    - save abc, image
#    + Save and open pickle
#    + zeroth note should be down an octave sometimes; this has to do with my
#      lack of octave indication in the abc file
#    + write a new abc file when the row is modified
#    + zero first note
#
#    * Figure out how to write abc without all the redundant natural signs
#     (bug or feature?)"""

def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-n', metavar='LENGTH', help="notes/scale, row, etc....", nargs='?')
    return parser.parse_args() if __name__ == '__main__' else None

ARGS = _parse_args()
TONE_COUNT = int(ARGS.n) if ARGS.n else 12

def welcome():
    """
    print license and dependency info to the screen
    """
    print(
        misc.welcome_str(
            2018, __author__,
            title=colored('TONE ROW COMPUTER', attrs=['bold'])))
    #print(
    #    'Depends: abc2midi, abcm2ps, evince (or other postscript viewer),\n'\
    #    '         python-termcolor, sox, timidity/timidity++, (configured with a\n'\
    #    '         soundfont if necessary, e.g., timidity-freepats)\n')



def main():
    """
    create a tone row and start command shell
    """
    #def new_row():
    welcome()
    rlif.howto()
 
 
    row = Tonerow(TONE_COUNT)

    #new_row()
#    def unpickle():
#        nonlocal row
#        row = fileio.open_p_file(dirname='__data__')


    # There used to be a bug with lambdas here
    cmd_dict = {'abc': lambda: print(row.generate_abc_str()),
                #'clear': termctl.clear,
                'draw': row.draw,#(),  # pylint:disable=unnecessary-lambda
                'invert': row.invert,  # pylint: disable=unnecessary-lambda
                'list': row.listfreqs,  # pylint: disable=unnecessary-lambda
                #'matrix': lambda: row.matrix(),
                'midi': row.play_midi,  # pylint: disable=unnecessary-lambda
                'pickle': lambda: row.save_p_file(f'__data__/{row.generate_basename()}'),
                'play': row.play,  # pylint: disable=unnecessary-lambda
                'plot': row.plot,  # pylint: disable=unnecessary-lambda
                'retro': row.reverse,  # pylint: disable=unnecessary-lambda
                'row': lambda: print(row.__dict__),
                'rotate': row.rotate,  # pylint: disable=unnecessary-lambda
                'shuffle': row.shuffle,
                'staff': row.open_staff,  # pylint: disable=unnecessary-lambda
                #'unpickle': unpickle,
                #'unpickle': lambda: 0,  # deal with this below instead
                #'unpickle': lambda: fileio.open_p_file(dirname='__data__'),
                'zero': row.zero,  # pylint: disable=unnecessary-lambda
                'quit': sys.exit
               }

    # Register our completer function
    readline.set_completer(rlif.SimpleCompleter(cmd_dict.keys()).complete)

    # Use the tab key for completion
    readline.parse_and_bind('tab: complete')

    #print(f'{row.__repr__()}')
    #print(f' {list(cmd_dict.keys())}')

    while True:
        print('>', end='', flush=True)
        raw_command = input()

        cmd_list = raw_command.split(',')
        cmd_list = [i.strip() for i in cmd_list]
        for command in cmd_list:
            if command and command[0] == '!':
                proc = subprocess.Popen(command[1:], shell=True)
                proc.wait()
                continue
            if command == 'unpickle':
                row = fileio.open_p_file(dirname='__data__')
            else:
                try:
                    cmd_dict[command]()
                except KeyError:
                    #if command == 'unpickle':
                    termctl.cursor_v(1)
                    termctl.cursor_h(1)
        #print(f'{list(cmd_dict.keys())}\n')
        rlif.howto()

#atexit.register(misc.end_app)  # Marks this app as having finished its first run
if __name__ == '__main__':
    #if misc.is_first_run():
    #termctl.clear(6)
    main()
