#!/usr/bin/env python3
#coding=utf8
"""
Accurate Coffee Timer.  Takes an argument is the form SS, :SS, MM:, or
MM:SS.  Default time is 5m30s.  -n disables ascii-art display, -q disables
beeping sound at the end.
"""
import argparse
import sys
import time

from termcolor import cprint

import soxmusic
import misc
import termctl
from figlet import Figlet

__author__ = 'Chris Horn <hammerhorn@gmail.com'
__license__ = 'GPL'


################
#  PROCEDURES  #
################
def _parse_args():
    """
    -h                 get help on these options
    -q, --quiet        suppress audible alert
    -n, --no-figlet    suppress ascii art
    TIME_STR       (seconds), :(seconds), (minutes):, or (minutes):(seconds)
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-q', '--quiet', help='no sound', action='store_true')
    parser.add_argument('-n', '--no-figlet', help='disable figlet display', action='store_true')

    #supposedly there is an equivalent generator expression which would be
    #better

    #make the positional argument optional
    if [i for i in sys.argv[1:] if not i.startswith('-')]:
        parser.add_argument('time_str', type=str)
    return parser.parse_args()


def alert():
    """
    Print a visual alert using the toilet(/figlet) command.
    Print an audible alert using espeak speech synthesizer.
    """
    out_str = 'Done' if ARGS.no_figlet else FIG_WRITER.output('Done', get_str=True)
    cprint(out_str, 'red')
    print(f'Finished at {misc.current_time()}.')

    if not ARGS.quiet:
        soxmusic.Note(soxmusic.Pitch(freq=1000), 0.5).play(voice='sin')
        misc.speak("Time's up.")


###############
#  CONSTANTS  #
###############
ARGS = _parse_args() if __name__ == '__main__' else None

try:
    TIME_STR = ARGS.time_str
except AttributeError:
    TIME_STR = '330'

if TIME_STR[0] == ':':
    TIME_STR = f'0{TIME_STR}'

SECONDS = float(TIME_STR) if TIME_STR.isdigit() else float(
    misc.mmss_convert(TIME_STR))
_SINCE = time.time()
#FIG_WRITER = Figlet(font='pagga')
FIG_WRITER = Figlet(font='future')

##########
#  MAIN  #
##########
def main():
    """
    Starts the countdown timer, continually double-checking against clock
    time to maintain accuracy.
    """
    remaining = SECONDS
    time_str = misc.mmss_convert(int(remaining))

    termctl.hide_cursor()
    while remaining >= 0:
        out_str = f'\r{time_str.strip():>5s}' if ARGS and ARGS.no_figlet else FIG_WRITER.output(
            f'\r{time_str.strip():>5s}', get_str=True)
        cprint(out_str, 'green')
        time.sleep(.25)
        remaining = SECONDS - time.time() + _SINCE
        time_str = misc.mmss_convert(int(remaining))
        spacing = 1 if ARGS.no_figlet else 6
        if remaining < 0 or int(remaining) == 599:
            termctl.clear(spacing)
        else:
            termctl.cursor_v(spacing)
    alert()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\b\b  \r\nInterrupted at {misc.current_time()}.')
    finally:
        termctl.unhide_cursor()
