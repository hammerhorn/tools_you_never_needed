#!/usr/bin/env python3
"""
Prints the IP address of the LAN gateway
"""
# Standard Library
import os
import sys

# Third-party modules
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ImportError:
    sys.exit('\nGtk+3.0 library not available.\n')

# Local modules
import cows
import gtkstuff
import newterminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

#COWS_FOLDER = '/usr/share/cowsay/cows'
#COW_LIST = [cow[:-4] for cow in  os.listdir(COWS_FOLDER)]
#COW_LIST.sort()

class CowsWindow(Gtk.Window):
    """
    window with a ComboInputBox for choosing cow ascii art
    """
    def __init__(self):
        super().__init__(title='Cowsay Cow Browser', default_width=250)
        self.set_border_width(10)
        self.set_icon_from_file('icons/cow.png')
        self.comboinputbox = gtkstuff.ComboInputBox(
            combo_list=cows.COW_LIST,
            label1="Cows available:",
            label2="Message:")
        self.comboinputbox.entry.set_text('Hello')
        self.comboinputbox.button.connect("clicked", self.on_click)
        self.add(self.comboinputbox)

    def on_click(self, _):
        """
        when the button is clicked, let's launch the selected cow in a
        new terminal window
        """
        dir_name = os.getcwd()
        if dir_name != '/':
            dir_name = f'{dir_name}/'

        # run cowsay in a new terminal window in your default terminal
        newterminal.runcommand(
            f'cowsay -f {self.comboinputbox.selected_item} '\
            f'"{self.comboinputbox.entry.get_text()}"', hold=True)

def main():
    """
    This can be called from python interpreter
    without requiring other explicit imports
    """
    window = CowsWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
