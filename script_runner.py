#!/usr/bin/env python3
"""
Run, edit, lint, and view auto-documentation for Python scripting.
Currently uses x-termal-emulator, so only works with Debian-based OSes.
"""
# Standard Library
import os
import subprocess
import sys

# Third-Party
import gi
import termcolor

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

import newterminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

MODULE_NAME = termcolor.colored(
    sys.argv[0].split('/')[-1].split('.')[0], attrs=['underline'])

def _load_script_names():
    """
    maybe magic module should be used?
    """
    script_list = [
        s for s in os.listdir(os.getcwd())
        if (s.endswith('.py') and not (s.startswith('.') or s.startswith('_')))
    ]
    script_list.sort()
    return script_list

class ScriptRunnerWindow(Gtk.Window):
    """
    main window for this app, has a ComboBox, Entry, Switch, and some Buttons
    """
    def __init__(self):
        """
        main window and all of the widgets needed
        """
        # Define Main Window
        self.selected_dir = os.getcwd()
        self.line_number = None
        super().__init__(title=f'Runner: {self.selected_dir}')#.split("/")[-1]}')
        self.set_icon_from_file('icons/runner.png')
        self.connect('delete-event', Gtk.main_quit)

        # overhead menus
        self.create_menu()

        # This stuff is for the ComboBox
        self.scriptnames_liststore = Gtk.ListStore(str)
        self.selected_script = self.create_combobox()

        # maybe this is not efficient
        with open(self.selected_script, 'r') as filepointer:
            lines_in_file = len(filepointer.readlines())

        # spinbutton
        self.line_number = Gtk.SpinButton.new_with_range(1, lines_in_file, 1)
        self.line_number.set_width_chars(3)
        self.line_number.set_alignment(xalign=1)
        self.line_number.set_value(1)

        self.args_entry = Gtk.Entry()

        # Line number to open for Editing
        line_number_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        line_number_label = Gtk.Label()
        line_number_label.set_markup('<small>edit line:</small>')
        line_number_label.set_xalign(0)


        line_number_box.pack_start(line_number_label, False, False, 0)
        line_number_box.pack_start(self.line_number, False, False, 0)

        main_row = Gtk.Box(border_width=10, spacing=10, orientation=Gtk.Orientation.HORIZONTAL)

        self.main_layout = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL)

        main_row.pack_start(self.combobox, False, False, 0)
        main_row.pack_start(self.args_entry, True, True, 0)
        main_row.pack_start(line_number_box, False, None, 0)

        # Pack boxes
        self.main_layout.pack_start(self.main_menu_bar, False, False, 0)
        self.main_layout.pack_start(main_row, False, False, 0)
        self.add(self.main_layout)

    def update_spinbutton(self, _):
        """
        refresh the max line length possible using the spinbutton
        This does not play nicely with terminator.
        """
        with open(self.selected_script, 'r') as filepointer:
            lines_in_file = len(filepointer.readlines())
        if self.line_number:
            self.line_number.set_range(1, lines_in_file)
            self.line_number.set_value(1)

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

        file_cd = Gtk.MenuItem(label='Change directory')
        file_cd.connect("activate", self.file_cd_clicked)
        file_menu.append(file_cd)

        file_refresh = Gtk.MenuItem(label='Refresh script list')
        file_refresh.connect("activate", self.refresh_combobox)
        file_menu.append(file_refresh)

        file_menu.append(Gtk.SeparatorMenuItem())

        file_run = Gtk.MenuItem(label='Run')
        file_run.connect("activate", self.run_clicked)
        file_menu.append(file_run)

        file_run_in_term = Gtk.MenuItem(label='Run in terminal')
        file_run_in_term.connect("activate", self.run_in_term_clicked)
        file_menu.append(file_run_in_term)

        file_menu.append(Gtk.SeparatorMenuItem())

        file_exit = Gtk.MenuItem(label='Quit')
        file_exit.connect("activate", Gtk.main_quit)
        file_menu.append(file_exit)

        self.main_menu_bar.append(file_menu_dropdown)


        # Edit menu
        edit_menu = Gtk.Menu()
        edit_menu_dropdown = Gtk.MenuItem(label='Edit')
        edit_menu_dropdown.set_submenu(edit_menu)

        edit_edit = Gtk.MenuItem(label='Edit')
        edit_edit.connect("activate", self.edit_clicked)
        edit_menu.append(edit_edit)
        self.main_menu_bar.append(edit_menu_dropdown)

        # Tools menu
        tools_menu = Gtk.Menu()
        tools_menu_dropdown = Gtk.MenuItem(label='Tools')
        tools_menu_dropdown.set_submenu(tools_menu)

        tools_lint = Gtk.MenuItem(label='pylint')
        tools_lint.connect("activate", self.lint_clicked)
        tools_menu.append(tools_lint)

        tools_doc = Gtk.MenuItem(label='pydoc')
        tools_doc.connect("activate", self.doc_clicked)
        tools_menu.append(tools_doc)

        self.main_menu_bar.append(tools_menu_dropdown)

        # Help menu
        help_menu = Gtk.Menu()
        help_menu_dropdown = Gtk.MenuItem(label='Help')
        help_menu_dropdown.set_submenu(help_menu)

        help_about = Gtk.MenuItem(label='About')
        help_about.connect("activate", self.show_about)
        help_menu.append(help_about)

        self.main_menu_bar.append(help_menu_dropdown)

    def create_combobox(self):
        """
        set up the combobox
        """
        self.combobox = Gtk.ComboBox.new_with_model(self.scriptnames_liststore)
        self.combobox.connect("changed", self.update_selected_script)
        renderer_text = Gtk.CellRendererText()

        for script_name in _load_script_names():
            self.scriptnames_liststore.append([script_name])

        self.combobox.pack_start(renderer_text, True)
        self.combobox.add_attribute(renderer_text, "text", 0)
        self.combobox.set_active(0)
        return _load_script_names()[0]

    def refresh_combobox(self, _):
        """
        refresh the list of scripts upon user request
        """
        current_script = self.selected_script
        self.scriptnames_liststore.clear()
        script_list = _load_script_names()
        for script_name in script_list:
            self.scriptnames_liststore.append([script_name])
        # try:
        self.combobox.set_active(script_list.index(current_script))
        # except:
        #    pass

        self.set_title(f'Runner: {self.selected_dir}')#.split("/")[-1]}')

    def update_selected_script(self, combo):
        """
        update the selected script when the combobox is changed
        """
        tree_iter = combo.get_active_iter()
        if tree_iter:
            model = combo.get_model()
            self.selected_script = model[tree_iter][0]

        self.update_spinbutton(None)

    def file_cd_clicked(self, _):
        """
        use a file chooser dialog to change directories and update
        titlebar
        """
        dialog = Gtk.FileChooserDialog(
            title="Please choose a directory...", parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.set_default_size(650, 400)
        dialog.add_button("_Open", Gtk.ResponseType.OK)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.set_default_response(Gtk.ResponseType.OK)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.selected_dir = dialog.get_filename()
            os.chdir(self.selected_dir)
            self.set_title(f'Runner: {self.selected_dir}')#.split("/")[-1]}')
            self.refresh_combobox(_)
        dialog.destroy()

    def run_clicked(self, _):
        """
        write a script that runs the selected script in a new terminal
        window, and run that script.  this is better than a simple
        subprocess because 1) too many quotation marks gets confusing,
        2) now the terminal doesn't need to be closed in order to
        continue using the main program
        """
        # There is probably a better way
        if self.selected_script:
            args = self.args_entry.get_text()
            command_str = f'python3 {self.selected_script} {args}'
            proc = subprocess.Popen(f'{command_str}&', shell=True)
            proc.wait()
            #self.refresh_combobox(None)

    def run_in_term_clicked(self, _):
        if self.selected_script:
            args = self.args_entry.get_text()
            command_str = f'python3 {self.selected_script} {args}'
            newterminal.runcommand(command_str, hold=True)

    def edit_clicked(self, _):
        """
        when the edit button is clicked, let's open the selected file in
        the default editor in a new terminal window
        """
        # As long as you use a separate module (runbashcommand) you
        # won't have issues like before
        entry_text = self.line_number.get_text()
        newterminal.runcommand(
            f'editor +{entry_text} {self.selected_script}', hold=False)
        self.update_spinbutton(None)

    def lint_clicked(self, _):
        """
        when lint button is clicked, let's open pylint on the file in a
        new window of your default terminal emulator
        """
        self.refresh_combobox(None)
        if self.selected_script:
            newterminal.runcommand(
                f'pylint {self.selected_script}|less', hold=False)

    def doc_clicked(self, _):
        """
        when pydoc button is clicked, let's open pydoc on the file in a
        new window of your default terminal emulator
        """
        self.refresh_combobox(None)
        if self.selected_script:
            mod_name = '.'.join(self.selected_script.split('.')[:-1])
            newterminal.runcommand(f'pydoc3 "{mod_name}"', hold=False)

    #def on_checkbutton_toggled(self, _):
    #    self.term_state = self.checkbutton.get_active()

    @staticmethod
    def show_about(_):
        """
        show About dialog
        """
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_icon_from_file('icons/runner.png')
        about_dialog.set_title("About Runner")
        about_dialog.set_program_name("Runner")
        about_dialog.set_version("0.0")
        about_dialog.set_comments(
            "Minimalistic development environment for writing Python3 "\
            "scripts on Debian-based systems.")
        about_dialog.set_authors(["Chris Horn <hammerhorn@gmail.com>"])
        about_dialog.set_logo(
            GdkPixbuf.Pixbuf.new_from_file_at_size("icons/runner.png", 64, 64))
        about_dialog.set_license("Distributed under the GNU GPL(v3) license.\n")
        about_dialog.connect(
            'response', lambda about_dialog, data: about_dialog.destroy())
        about_dialog.show_all()

def main():
    """
    declare window and run program
    """
    window = ScriptRunnerWindow()
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
