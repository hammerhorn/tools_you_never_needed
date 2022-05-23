#!/usr/bin/env python3
"""defining colors different ways"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

import runbashcommand
from colorful import color

class ColorSpectraBox(Gtk.Box):
    """all these spinbuttons maybe should be scales"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)#, spacing=10)
        self.create_menu()

        self.color_obj = None

        self.ansi_colorbutton = Gtk.ColorButton()
        self.ansi_spinbutton = Gtk.SpinButton.new_with_range(0, 255, 1)
        self.ansi_spinbutton.connect("value-changed", self.ansi_spinner_changed)
        self.ansi_spinner_changed(None)
        ansi_row = Gtk.Box(border_width=10, spacing=10)
        ansi_row.pack_start(Gtk.Label(label='ANSI'), False, None, 0)
        ansi_row.pack_start(self.ansi_colorbutton, False, None, 0)
        ansi_row.pack_start(self.ansi_spinbutton, False, None, 0)

        self.rgb_colorbutton = Gtk.ColorButton()
        self.r_spinbutton = Gtk.SpinButton.new_with_range(0, 255, 1)
        self.r_spinbutton.connect("value-changed", self.rgb_spinner_changed)
        self.g_spinbutton = Gtk.SpinButton.new_with_range(0, 255, 1)
        self.g_spinbutton.connect("value-changed", self.rgb_spinner_changed)
        self.b_spinbutton = Gtk.SpinButton.new_with_range(0, 255, 1)
        self.b_spinbutton.connect("value-changed", self.rgb_spinner_changed)
        self.rgb_spinner_changed(None)
        rgb_row = Gtk.Box(border_width=10, spacing=10)
        rgb_row.pack_start(Gtk.Label(label='RGB'), False, None, 0)
        rgb_row.pack_start(self.rgb_colorbutton, False, None, 0)
        rgb_row.pack_start(self.r_spinbutton, False, None, 0)
        rgb_row.pack_start(self.g_spinbutton, False, None, 0)
        rgb_row.pack_start(self.b_spinbutton, False, None, 0)

        self.kelvin_colorbutton = Gtk.ColorButton()
        self.kelvin_spinbutton = Gtk.SpinButton.new_with_range(250, 10000, 10)
        self.kelvin_spinbutton.connect(
            "value-changed", self.kelvin_spinner_changed)
        self.kelvin_spinner_changed(None)
        kelvin_row = Gtk.Box(border_width=10, spacing=10)
        kelvin_row.pack_start(Gtk.Label(label='Kelvin'), False, None, 0)
        kelvin_row.pack_start(self.kelvin_colorbutton, False, None, 0)
        kelvin_row.pack_start(self.kelvin_spinbutton, False, None, 0)

        self.pack_start(self.main_menu_bar, False, None, 0)
        self.pack_start(ansi_row, False, None, 0)
        self.pack_start(rgb_row, False, None, 0)
        self.pack_start(kelvin_row, False, None, 0)

    def create_menu(self):
        """
        set up the overhead menus
        """
        # Main container for menus
        self.main_menu_bar = Gtk.MenuBar()

        # File menu
        file_menu = Gtk.Menu()
        file_menu_dropdown = Gtk.MenuItem(label='File')
        file_menu_dropdown.set_submenu(file_menu)
        file_exit = Gtk.MenuItem(label='Quit')
        file_exit.connect("activate", Gtk.main_quit)
        file_menu.append(file_exit)

        run_menu = Gtk.Menu()
        run_menu_dropdown = Gtk.MenuItem(label='Tables')
        run_menu_dropdown.set_submenu(run_menu)
        run_colors1_sh = Gtk.MenuItem(label='colors1.sh')
        run_colors1_sh.connect("activate", self.run_colors1_sh_clicked)
        run_menu.append(run_colors1_sh)
        run_colors2_sh = Gtk.MenuItem(label='colors2.sh')
        run_colors2_sh.connect("activate", self.run_colors2_sh_clicked)
        run_menu.append(run_colors2_sh)
        run_colortrans_py = Gtk.MenuItem(label='colortrans.py')
        run_colortrans_py.connect("activate", self.run_colortrans_py_clicked)
        run_menu.append(run_colortrans_py)

        # Help menu
        help_menu = Gtk.Menu()
        help_menu_dropdown = Gtk.MenuItem(label='Help')
        help_menu_dropdown.set_submenu(help_menu)
        help_about = Gtk.MenuItem(label='About')
        help_about.connect("activate", self.show_about)
        help_menu.append(help_about)

        self.main_menu_bar.append(file_menu_dropdown)
        self.main_menu_bar.append(run_menu_dropdown)
        self.main_menu_bar.append(help_menu_dropdown)

    def show_about(self, _):
        """
        show About dialog
        """
        dialog = Gtk.AboutDialog()
        dialog.set_icon_from_file('icons/rainbowflag.png')
        dialog.set_title("About Colors and EM Radiation")
        dialog.set_program_name("Colors and EM Radiation")
        dialog.set_version("0.0")
        dialog.set_comments(
            "Tool for converting color names from one format to another")
        dialog.set_authors(["Chris Horn <hammerhorn@gmail.com>"])
        dialog.set_logo(
            GdkPixbuf.Pixbuf.new_from_file_at_size("icons/rainbowflag.png", 64, 64))
        dialog.set_license("Distributed under the GNU GPL(v3) license.\n")
        dialog.connect('response', lambda dialog, data: dialog.destroy())
        dialog.show_all()

    def run_colors1_sh_clicked(self, _):
        runbashcommand.runbashcommand("bash colors1.sh")

    def run_colors2_sh_clicked(self, _):
        runbashcommand.runbashcommand("bash colors2.sh")

    def run_colortrans_py_clicked(self, _):
        runbashcommand.runbashcommand("python colortrans.py")

    def ansi_spinner_changed(self, _):
        self.color_obj = color.Color(int(self.ansi_spinbutton.get_value()), 'ansi')
        red_percent = int(self.color_obj.hexstring[1:3], 16) / 255.
        green_percent = int(self.color_obj.hexstring[3:5], 16) / 255.
        blue_percent = int(self.color_obj.hexstring[5:7], 16) / 255.
        gdk_color = Gdk.RGBA(red=red_percent, green=green_percent, blue=blue_percent)
        self.ansi_colorbutton.set_rgba(gdk_color)

    def rgb_spinner_changed(self, _):
        red = int(self.r_spinbutton.get_value())
        green = int(self.g_spinbutton.get_value())
        blue = int(self.b_spinbutton.get_value())
        hexstr = f'#{red:02x}{green:02x}{blue:02x}'
        self.color_obj = color.Color(hexstr, 'hex')
        red_percent = red / 255.
        green_percent = green / 255.
        blue_percent = blue /255.
        gdk_color = Gdk.RGBA(red=red_percent, green=green_percent, blue=blue_percent)
        self.rgb_colorbutton.set_rgba(gdk_color)

    def kelvin_spinner_changed(self, _):
        #try:
        self.color_obj = color.Color(int(self.kelvin_spinbutton.get_value()), 'kelvin')
        #except ValueError:
        print(int(self.kelvin_spinbutton.get_value()))
        red_percent = int(self.color_obj.hexstring[1:3], 16) / 255.
        green_percent = int(self.color_obj.hexstring[3:5], 16) / 255.
        blue_percent = int(self.color_obj.hexstring[5:7], 16) / 255.
        gdk_color = Gdk.RGBA(
            red=red_percent, green=green_percent, blue=blue_percent)
        self.kelvin_colorbutton.set_rgba(gdk_color)

def main():
    window = Gtk.Window(title='Color and the EM Spectrum GTK')
    window.connect('delete-event', Gtk.main_quit)
    window.add(ColorSpectraBox())
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
