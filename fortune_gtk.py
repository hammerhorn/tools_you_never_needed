#!/usr/bin/env python3
"""
Fortune front-end
"""
import argparse
import subprocess
import sys

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ImportError:
    sys.exit('\nGtk+3.0 library not available.\n')
import pyperclip

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


def _parse_args():
    """
    ./bin_text.py -d filename
    """
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args() if __name__ == '__main__' else None

_parse_args()

if not Gtk.init_check():
    sys.exit()

class FortuneWindow(Gtk.Window):
    """
    This window generates fortunes when the button is pressed.
    """
    def __init__(self):
        super().__init__(title='Fortune Cookie')
        self.set_border_width(10)
        self.set_icon_from_file('icons/cookie.png')
        self.connect('destroy', Gtk.main_quit)

        self.fortune = ""

        self.label = Gtk.Label()

        self.show_new_fortune(None)

        # New Fortune button
        self.button = Gtk.Button.new_with_mnemonic(label='New _fortune (Alt+F)')
        self.button.connect("clicked", self.show_new_fortune)

        # Copy button
        copy_button = Gtk.Button.new_with_mnemonic(
            label='_Copy to the clipboard (Alt+C)')
        copy_button.connect("clicked", self.copy_clicked)

        # A bar to keep our buttons in
        button_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_bar.pack_start(self.button, True, True, 0)
        button_bar.pack_start(copy_button, False, False, 0)

        # Main layout
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.pack_start(self.label, False, False, 0)
        self.box.pack_start(button_bar, True, True, 0)
        self.add(self.box)

        self.show_new_fortune(None)

    def copy_clicked(self, _):
        """copy current fortune to the system clipboard"""
        # I think it is possible to do this using only GTK
        pyperclip.copy(self.fortune)

    def show_new_fortune(self, _):
        """
        When the button is pressed, the label is set to a new
        fortune and the window is resized to fit snuggly around
        everything.
        """
        self.fortune = str(subprocess.check_output('fortune', shell=True), 'UTF-8')

        self.label.set_label(self.fortune)

        self.resize(1, 1)

        # I don't want it to start out selected
        #self.label.set_selectable(True)

WINDOW = FortuneWindow()

if __name__ == '__main__':

    #Run the app
    WINDOW.show_all()
    Gtk.main()
