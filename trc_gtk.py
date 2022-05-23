#!/usr/bin/env python3
"""
graphical front end for testing class <tonerow.Tonerow>
"""
# Standard Library
import argparse
import logging
import textwrap

# Third-party
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf


# Local modules
import tonerow

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def _parse_args():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args() if __name__ == '__main__' else None


class TonerowWindow(Gtk.Window):
    """
    Main window that will hold all our buttons
    """
    def __init__(self, **kwargs):

        # Make a window
        super().__init__(**kwargs)
        self.connect("delete-event", Gtk.main_quit)

        # Make a tonerow
        self.row = tonerow.Tonerow()
        self.set_title(f'Tonerow Computer: {self.row.seq}')

        # This will be changed to a Gtk.Notebook in the future
        self.view = 'list'
        logging.debug('Now view mode = "%s"', self.view)

        # Menu
        self.main_menu_bar = Gtk.MenuBar()

        file_menu_dropdown = Gtk.MenuItem(label='File')
        file_menu = Gtk.Menu()
        file_menu_dropdown.set_submenu(file_menu)
        
        file_new = Gtk.MenuItem(label='New/Shuffle')
        file_new.connect("activate", self.shuffle)
        file_menu.append(file_new)           
        file_open = Gtk.MenuItem(label='Open')
        file_menu.append(file_open)        
        file_save = Gtk.MenuItem(label='Save')
        file_save.connect("activate", self.save)
        file_menu.append(file_save)
        file_menu.append(Gtk.SeparatorMenuItem())        
        file_exit = Gtk.MenuItem(label='Quit')
        file_exit.connect("activate", Gtk.main_quit)
        file_menu.append(file_exit)
        
        edit_menu_dropdown = Gtk.MenuItem(label='Edit')
        edit_menu = Gtk.Menu()
        edit_menu_dropdown.set_submenu(edit_menu)
        edit_retro = Gtk.MenuItem(label='backwards') # AKA Retrograde
        edit_retro.connect("activate", self.reverse)
        edit_menu.append(edit_retro)
        edit_invert = Gtk.MenuItem(label='upside-down')# AKA Invert
        edit_invert.connect("activate", self.invert)
        edit_menu.append(edit_invert)                
        edit_clockwise = Gtk.MenuItem(label='clockwise 90°')
        edit_clockwise.connect("activate", self.rotate)
        edit_menu.append(edit_clockwise)                
        edit_menu.append(Gtk.SeparatorMenuItem())
        edit_zero = Gtk.MenuItem(label='Zero')
        edit_zero.connect("activate", self.zero)
        edit_menu.append(edit_zero)
                
        view_menu_dropdown = Gtk.MenuItem(label='View')
        view_menu = Gtk.Menu()
        view_menu_dropdown.set_submenu(view_menu)
        view_matplot = Gtk.MenuItem(label='matplot')
        view_matplot.connect("activate", self.plot)
        view_menu.append(view_matplot)                

        play_menu_dropdown = Gtk.MenuItem(label='Play')
        play_menu = Gtk.Menu()
        play_menu_dropdown.set_submenu(play_menu)
        play_midi = Gtk.MenuItem(label='Play MIDI')
        play_midi.connect("activate", self.play_midi)
        play_menu.append(play_midi)
        play_sox = Gtk.MenuItem(label='Play with SoX')
        play_sox.connect("activate", self.play)
        play_menu.append(play_sox)
        
        help_menu_dropdown = Gtk.MenuItem(label='Help')
        help_menu = Gtk.Menu()
        help_menu_dropdown.set_submenu(help_menu)
        help_about = Gtk.MenuItem(label='About')
        help_about.connect("activate", self.show_about)
        help_menu.append(help_about)
        
        self.main_menu_bar.append(file_menu_dropdown)
        self.main_menu_bar.append(edit_menu_dropdown)
        self.main_menu_bar.append(view_menu_dropdown)
        self.main_menu_bar.append(play_menu_dropdown)
        self.main_menu_bar.append(help_menu_dropdown)
        
        self.info_label = Gtk.Label()
        self.info_label.set_selectable(self)

        #Radio Buttons - this will be replaced by a Gtk.Notebook
        self.listfreqs_button = Gtk.RadioButton(label='List View')
        self.listfreqs_button.connect("toggled", self.toggle_views)
        
        self.grid_button = Gtk.RadioButton(
            group=self.listfreqs_button, label='Diagram View')
        self.grid_button.connect("toggled", self.toggle_views)
        
        self.abc_button = Gtk.RadioButton(
            group=self.listfreqs_button, label='View ABC Code')
        self.abc_button.connect("toggled", self.toggle_views)
 
        self.staff_image = Gtk.Image()
        self.row.create_ps()
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            f'__data__/{self.row.basename}-cropped.png')
        self.staff_image.set_from_pixbuf(self.pixbuf)

        self.change_views()
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        view_radiobox = Gtk.Box(
            border_width=10,
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10)

        view_radiobox.pack_start(self.listfreqs_button, True, False, 0)
        view_radiobox.pack_start(self.grid_button, True, False, 0)
        view_radiobox.pack_start(self.abc_button, True, False, 0)

        main_box.pack_start(self.main_menu_bar, False, None, 0)       
        main_box.pack_start(self.staff_image, False, None, 0)
        main_box.pack_start(self.info_label, True, True, 0)
        main_box.pack_start(view_radiobox, True, True, 10)
        
        self.add(main_box)

    def save(self, _):
         self.row.save_p_file(self.row.generate_basename())

    def shuffle(self, _):
        """shuffle the current row in place"""
        self.row.shuffle()
        logging.debug('Row is now %s', self.row.seq)
        self.update_output(None)

    def plot(self, _):
        """open the row as a line graph in matplotlib"""
        self.row.plot(quiet=True)

    def reverse(self, _):
        """reverse the sequence in place"""
        self.row.reverse()
        logging.debug('Row is now %s', self.row.seq)
        self.update_output(None)

    def zero(self, _):
        """adjust the row in place so that the first number is a zero"""
        self.row.zero()
        self.update_output(None)

    def invert(self, _):
        """invert the row (flip with respect to the horizontal axis)"""
        self.row.invert()
        self.update_output(None)

    def rotate(self, _):
        """rotate the row 90 degrees (clock-wise?)"""
        self.row.rotate()
        self.update_output(None)

    def listfreqs(self, _):
        """
        serif font would be nice, but maybe more boxes for formatting
        """
        self.info_label.set_markup(
            f'<span font="monospace">\n'\
            f'{textwrap.dedent(self.row.listfreqs(get_str=True))}\n</span>')

    def open_postscript(self, _):
        """
        open in postscript reader as staff notation; uses xdg-open and abc2ps
        """
        self.row.open_staff()

    def update_output(self, _):
        """
        some of this formatting stuff should be fixed inside the class
        but be sure not to break other things
        """
        logging.debug("update_output START")
        self.set_title(f'Tonerow Computer: {self.row.seq}')
        self.change_views()
        self.row.create_ps()
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            f'__data__/{self.row.generate_basename()}-cropped.png')
        self.staff_image.set_from_pixbuf(self.pixbuf)
        logging.debug("update_output END")

    def change_views(self):
        if self.view == 'diagram':
            reformatted_diagram = self.row.draw(
                get_str=True,
                cntrl_chrs=False,
                heading=False)[1:].replace(
                    '[*]',
                    '<span bgcolor="grey">   </span>').replace('.', ' ')
            self.info_label.set_markup(
                f'<span font="monospace">'\
                f'{reformatted_diagram}'\
                '</span>')
        elif self.view == 'list':
            self.listfreqs(None)
        elif self.view == 'abc':
            self.info_label.set_markup(
                f'<span font="monospace">'\
                f'\n\n{self.row.generate_abc_str()}\n\n\n\n\n'\
                '</span>')
         
    def play_midi(self, _):
        """play the row with your midi player"""
        self.row.play_midi()

    def play(self, _):
        """play the row with your midi player"""
        self.row.play()

    def toggle_views(self, widget, data=None):
        selection = widget.get_label()        
        selection_dict = {
            'List View': 'list',
            'Diagram View': 'diagram',
            'View ABC Code': 'abc'
            }
        self.view = selection_dict[selection]
        logging.debug('Selection is %s, switching to %s', selection, self.view)            
        self.change_views()

    def show_about(self, _):
        """
        show About dialog
        """
        dialog = Gtk.AboutDialog()
        dialog.set_title("About Tonerow Computer GTK")
        dialog.set_program_name("Tonerow Computer GTK")
        dialog.set_version("0.0")
        dialog.set_comments(
            "Tool for generating and manipulating tonerows for musical "\
            "serialism.")
        dialog.set_authors(["Chris Horn <hammerhorn@gmail.com>"])
        dialog.set_license("Distributed under the GNU GPL(v3) license.\n")
        dialog.connect('response', lambda dialog, data: dialog.destroy())
        dialog.show_all()

_parse_args()
        
def main():
    """create a window and run the program"""
    main_window = TonerowWindow()
    main_window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()