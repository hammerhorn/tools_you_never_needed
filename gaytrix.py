#!/usr/bin/env python3
"""
something neat to look at made with curses
"""
import curses
import random
#import time

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(False)


def main(scr):
    scr.nodelay(True)

    scr.clear()
    scr.refresh()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    while True: #scr.getch() == curses.ERR:
        maxy, maxx = scr.getmaxyx()

        random_symbol = chr(random.randint(33, 126))
        random_x = random.randint(0, maxx-2)
        random_y = random.randint(0, maxy-1)
        if random.randint(0, 9) == 0:
            scr.addstr(
                random_y,
                random_x,
                random_symbol,
                curses.color_pair(1)|curses.A_BOLD)
        else:
            scr.addstr(
                random_y,
                random_x,
                random_symbol,
                curses.color_pair(1))
#        time.sleep(0.00001)
        scr.refresh()
#        if scr.getch() != -1:
#            break

curses.wrapper(main)
#main(stdscr)

curses.endwin()
