#!/usr/bin/env python3
#coding=utf8
"""
Simple C/C++/FORTRAN90 Interpreter/Interactive Code Runner

User can test lines of code, by inputting them and hitting EOF (^D or ^Z)
to compile and run bits of code on the fly.

This can be helpful for trying out and testing small bits of code.
"""
#standard library
import argparse
import atexit
import os
import readline  # pylint: disable=unused-import
import subprocess
import sys

#local
import misc

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--cpp',
        action='store_true',
        help='set language to C++ (default language is C)')
    parser.add_argument(
        '--f90', action='store_true', help='set language to Fortran 90')
    return parser.parse_args() if __name__ == '__main__' else None

def _set_language(args):
    """
    supports C, C++, or Fortran-90.
    """
    if args.f90:
        if args.cpp:
            sys.exit('Please choose one language.\n')
        else:
            lang = 'f90'
    elif args.cpp:
        lang = 'cpp'
    else:
        lang = 'c'
    return lang


###############
#  CONSTANTS  #
###############
EXTENSION = 'c'

if __name__ == '__main__':
    ARGS = _parse_args()
    EXTENSION = _set_language(ARGS)

def cleanup():
    """
    Remove temporary files.
    """
    for cleanup_file in (f'tmp.{EXTENSION}', 'a.out'):
        try:
            os.remove(cleanup_file)
        except OSError:
            pass

atexit.register(cleanup)

# make this a dictionary
if EXTENSION == 'cpp':
    TITLE = 'C++ LOOP'
elif EXTENSION == 'f90':
    TITLE = 'FORTRAN 90 LOOP'
else:
    TITLE = 'C LOOP'



##########
#  MAIN  #
##########
def main():
    """
    Preprocessor "include" statements are the only thing the interpreter
    remembers from previously-input commands.  ^C will discard all data,
    erase all data files, and end the program.
    """

    include_dict = {
        'f90': '',
        'cpp': '#include <iostream>\n',
        'c'  : '#include <stdio.h>\n'}

    startblock_dict = {
        'f90': 'PROGRAM Interactive\nIMPLICIT NONE\n',
        'c'  : 'int main(int argc, char* argv[])\n{\n',
        'cpp': 'using namespace std;\nint main(int argc, char* argv[])\n{\n'}

    prompt_dict = {
        'f90': '+',
        'cpp': '%%',
        'c': '%'}

    endblock_dict = {
        'f': 'END PROGRAM Interactive',
        'c': '\n\treturn 0;\n}'}

    compiler_dict = {
        'f90': 'gfortran',
        'c': 'gcc',
        'cpp': 'g++'}

    includes = include_dict[EXTENSION]

    print(misc.welcome_str(
        title=TITLE, year=2018, author=__author__))

    try:
        while True:
            block = startblock_dict[EXTENSION]
            prompt = prompt_dict[EXTENSION]
            print(prompt, end='', flush=True)

            while True:
                try:
                    # turn on green text
                    print('[32m[1m', end='', flush=True)
                    line = input().lstrip().rstrip('\n')

                    # This is the bit that is missing from the C version
                    if len(line) == 0:
                        print()
                    #print(f"length of line is {len(line)}")
                    if line.startswith('#include'):
                        includes = ''.join((includes, line, '\n'))
                    else:
                        block = ''.join((block, f'\t{line}\n'))

                except EOFError:
                    block = ''.join((block, endblock_dict[EXTENSION[0]]))
                    break

            filename = ''.join(('./tmp.', EXTENSION))
            with open(filename, 'w') as file_ptr:
                file_ptr.write(f'{includes}\n{block}')

            command_list = [compiler_dict[EXTENSION]]
            if EXTENSION == 'c':  # and 'math.h' in includes:
                command_list.extend([' -lm', ' -lncurses', ' -lreadline'])
            command_list.extend((' ./tmp.', EXTENSION))
            command = ''.join(command_list)

            # turn off green text
            print('[0m', end='', flush=True)
            try:
                return_val = subprocess.check_call(command, shell=True)
            except subprocess.CalledProcessError:
                return_val = None

            if return_val == 0:
                proc = subprocess.Popen('./a.out', shell=True)
                proc.wait()
            print('')

    except KeyboardInterrupt:
        print('\b\b\b', end='', flush=True)

if __name__ == '__main__':
    main()
