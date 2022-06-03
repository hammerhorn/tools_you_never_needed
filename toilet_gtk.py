#!/usr/bin/env python3
"""
Browse fonts for toilet or figlet type programs
"""
import argparse
import os
import sys

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ImportError:
    sys.exit('\nGtk+3.0 library not available.\n')

import figlet
import gtkstuff
import newterminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def _parse_args():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args() if __name__ == '__main__' else None

class ToiletWindow(Gtk.Window):
    """
    window with gtkstuff.comboinputbox and radio buttons for choosing
    filters
    """
    def __init__(self, **kwargs):
        super().__init__(title='Toilet Font Browser', border_width=10, **kwargs)
        self.set_icon_from_file('icons/toilet.png')
        self.connect('delete-event', Gtk.main_quit)

        # Combo, Entry, Button
        self.comboinputbox = gtkstuff.ComboInputBox(
            combo_list=figlet.get_font_list(),
            label1='Fonts available:',
            label2='Message:')
        self.comboinputbox.entry.set_text('Hello')
        self.comboinputbox.button.connect("clicked", self.on_click)

        # Radio Buttons
        self.button1 = Gtk.RadioButton(label='plain')
        self.button1.connect("toggled", self.on_selected)
        self.button2 = Gtk.RadioButton(group=self.button1, label='rainbow')
        self.button2.connect("toggled", self.on_selected)
        self.button3 = Gtk.RadioButton(group=self.button1, label='metal')
        self.button3.connect("toggled", self.on_selected)
        radio_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        radio_button_box.pack_start(self.button1, True, True, 0)
        radio_button_box.pack_start(self.button2, True, True, 0)
        radio_button_box.pack_start(self.button3, True, True, 0)

        self.modifier = ''

        self.main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_layout.pack_start(self.comboinputbox, True, True, 0)
        self.main_layout.pack_start(Gtk.Separator(), False, None, 0)
        self.main_layout.pack_start(radio_button_box, True, True, 0)
        self.add(self.main_layout)

    def on_selected(self, widget, data=None): # pylint: disable=unused-argument
        """
        This will be for the radio buttons
        """
        selection = widget.get_label()
        selection_key = {'plain':'', 'rainbow':'-F gay', 'metal':'-F metal'}
        self.modifier = selection_key[selection]


    def on_click(self, _):
        """
        open toilet in a new terminal window
        """
        dir_name = os.getcwd()
        if dir_name != '/':
            dir_name = f'{dir_name}/'
        command_to_run = f'toilet {self.modifier} -f '\
            f'{self.comboinputbox.selected_item} '\
            f'"{self.comboinputbox.entry.get_text()}"'

        # This function runs a command in a new window
        newterminal.runcommand(command_to_run)


_parse_args()

def main():
    """
    This can be called from python interpreter
    without requiring other explicit imports
    """
    window = ToiletWindow()
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
