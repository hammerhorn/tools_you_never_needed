#!/usr/bin/env python3
"""
Enter the number of bills of each denomination and it gives you the total
dollar amount.  Runs graphical version by default if GTK3 is available.
"""
# Standard Library
import argparse
import os
import sys

# Local modules
import cash
import termctl

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def _parse_args():
    """
    Parse arguments:
    --nox suppresses graphical window
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--nox', action='store_true', help='for the text-only version')
    return parser.parse_args() if __name__ == '__main__' else None

def nox():
    '''
    Enter the number of bills of each denomination to get the total
    '''
    total = 0
    print()
    for denom in cash.DENOMINATIONS:
        while True:
            try:
                val = input(f"{denom:>3}'s: ")
                if val == '':
                    val = 0
                total += int(val) * denom
                break
            except ValueError:
                termctl.clear(1)

        print(f"\n\n${total:.2f}\n")
        termctl.cursor_v(3)
        termctl.clear(0)
        termctl.cursor_v(1)
    print(f'\n${total:.2f}')
    input("Press <Enter> to exit.")
    termctl.clear(1)
    print()
    sys.exit()

ARGS = _parse_args()

# this could be rearranged.  how do you throw an exception?
if 'DISPLAY' not in os.environ or (ARGS and ARGS.nox):
    nox()

try:
    import gi

    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ImportError:
    nox()


class CashCounterBox(Gtk.Box):
    """
    very minimal window template
    """
    def __init__(self, **kwargs):
        super().__init__(
            spacing=10, orientation=Gtk.Orientation.VERTICAL, **kwargs)

        # Make the buttons
        zerobutton = Gtk.Button.new_with_mnemonic('_Clear')
        zerobutton.connect("clicked", zero_out)

        button_box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.HORIZONTAL)
        button_box.pack_start(zerobutton, True, True, 0)

        # ...And the output area
        self.output = Gtk.Label()
        output_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        output_box.set_border_width(25)
        output_box.pack_start(self.output, False, False, 0)
        output_frame = Gtk.Frame()
        output_frame.set_border_width(5)
        output_frame.add(output_box)

        # Layout

        # Make the boxes
        left_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        right_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        top_box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.HORIZONTAL)

        # And pack them
        for label in label_list:
            left_box.pack_start(label, True, True, 0)

        for entry in entry_list:
            right_box.pack_start(entry, True, True, 0)

        top_box.pack_start(left_box, True, True, 0)
        top_box.pack_start(right_box, True, True, 0)

        self.pack_start(top_box, True, True, 0)
        self.pack_start(output_frame, False, False, 0)
        self.pack_start(button_box, False, False, 0)

def count_up(_):
    '''
    calculate the sum and write it onto the window
    '''
    total = 0
    for count in range(6):
        total += int(entry_list[count].get_text()) * cash.DENOMINATIONS[count]
    CASHCOUNTERBOX.output.set_markup(
        f'<span size="x-large"><b>${total}</b></span>')
    APP_WINDOW.set_title(f'${total}')


def zero_out(_):
    '''
    zero all fields
    '''
    for entry in entry_list:
        entry.set_text('0')
    CASHCOUNTERBOX.output.set_markup('<span size="x-large"><b>$0</b></span>')
    APP_WINDOW.set_title(f'Cash Counter')

label_list = []
entry_list = []

for denom in cash.DENOMINATIONS:
    # Make the labels
    new_label = Gtk.Label()
    new_label.set_markup(f"<small><b>${denom}'s:</b></small>")
    new_label.set_xalign(1)
    label_list.append(new_label)

    # Make the entry boxes
    new_entry = Gtk.SpinButton.new_with_range(0, 999, 1)
    new_entry.set_value(0)
    new_entry.connect("value-changed", count_up)
    new_entry.set_alignment(xalign=1)
    entry_list.append(new_entry)

# Make the main window
APP_WINDOW = Gtk.Window(border_width=10, title='Cash Counter', default_width=175)
APP_WINDOW.set_icon_from_file('icons/money.png')
APP_WINDOW.connect('destroy', Gtk.main_quit)
CASHCOUNTERBOX = CashCounterBox()
APP_WINDOW.add(CASHCOUNTERBOX)

if __name__ == '__main__':
    APP_WINDOW.show_all()
    Gtk.main() # Run the app
