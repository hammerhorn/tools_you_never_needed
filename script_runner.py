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

import runbashcommand

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
        super().__init__(title=f'ScriptRunner: {self.selected_dir.split("/")[-1]}')
        self.set_icon_from_file('icons/runner.png')
        self.connect('delete-event', Gtk.main_quit)

        # overhead menus
        self.create_menu()

        # Accel Group
        #accelgroup = Gtk.AccelGroup()

        # This stuff is for the ComboBox
        self.scriptnames_liststore = Gtk.ListStore(str)
        self.selected_script = self.create_combobox()

        # maybe this is not efficient
        with open(self.selected_script, 'r') as fp:
            lines_in_file = len(fp.readlines())

        # spinbutton
        self.line_number = Gtk.SpinButton.new_with_range(1, lines_in_file, 1)
        self.line_number.set_width_chars(3)
        self.line_number.set_alignment(xalign=1)
        self.line_number.set_value(1)#lines_in_file)

        # Run button launches the selected program
        self.run_button = Gtk.Button.new_with_mnemonic('_Run')
        self.run_button.connect("clicked", self.run_clicked)

        # Edit button opens the program in the default text editor
        edit_button = Gtk.Button.new_with_mnemonic(label='_Edit')
        edit_button.connect("clicked", self.edit_clicked)

        # Lint button opens pylint
        lint_button = Gtk.Button.new_with_mnemonic(label='pylin_t\n(Alt+T)')
        lint_button.connect("clicked", self.lint_clicked)

        # Doc button opens pydoc
        doc_button = Gtk.Button.new_with_mnemonic(label='py_doc\n(Alt+D)')
        doc_button.connect("clicked", self.doc_clicked)

        # 'Run in terminal' checkbox (Checkbox can be replaced with
        # 'Run in terminal' button if desired)
        self.switch_label = Gtk.Label()
        self.switch_label.set_markup(f'<small>in terminal window</small>')
        self.term_state = True

        self.checkbutton = Gtk.CheckButton()
        self.checkbutton.connect("toggled", self.on_checkbutton_toggled)
        self.checkbutton.set_active(True)

        # args Entry for adding command-line arguments to the selected
        # script
        self.args_entry = Gtk.Entry()

        # Line number to open for Editing
        line_number_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        line_number_label = Gtk.Label()
        line_number_label.set_markup('<small>line number:</small>')
        line_number_label.set_xalign(0)
        line_number_box.pack_start(line_number_label, False, False, 0)
        line_number_box.pack_start(self.line_number, False, False, 0)

        # OVERALL LAYOUT
        # Make boxes
        self.top_row = Gtk.Box()
        self.command_row = Gtk.Box(spacing=10, border_width=10)
        self.bottom_row = Gtk.Box(spacing=10)

        self.middle_and_bottom = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.main_layout = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL)

        # Command frame
        #command_frame = Gtk.Frame(label='command line')
        self.command_row.pack_start(self.combobox, False, False, 0)
        self.command_row.pack_start(self.args_entry, True, True, 0)
        #command_frame.add(self.command_row)

        # Switch box
        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.switch_box.pack_start(self.switch_label, False, None, 0)
        self.switch_box.pack_start(self.checkbutton, False, None, 0)

        # Run button frame
        run_frame = Gtk.Frame(label='Alt+R')
        run_box = Gtk.Box(
            border_width=10, orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10)
        run_box.pack_start(self.run_button, False, False, 0)
        run_box.pack_start(self.switch_box, False, False, 0)
        run_frame.add(run_box)

        # Edit frame
        edit_frame = Gtk.Frame(label='Alt+E')
        edit_box = Gtk.Box(
            border_width=10, orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10)
        edit_box.pack_start(edit_button, False, False, 0)
        #edit_box.pack_start(line_number_box, False, False, 0)
        edit_frame.add(edit_box)

        # Other buttons area
        other_buttons = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        other_buttons.pack_start(lint_button, True, False, 0)
        other_buttons.pack_start(doc_button, True, False, 0)

        # Pack boxes
        self.top_row.pack_start(self.main_menu_bar, False, False, 0)
        #self.bottom_row.pack_start(run_frame, True, True, 0)
        #self.bottom_row.pack_start(edit_frame, True, True, 0)
        #self.bottom_row.pack_start(other_buttons, True, True, 0)
        self.command_row.pack_start(line_number_box, False, None, 0)
        self.middle_and_bottom.pack_start(self.command_row, False, False, 0)
        #self.middle_and_bottom.pack_start(self.bottom_row, True, True, 0)
        self.middle_and_bottom.set_border_width(10)
        self.main_layout.pack_start(self.top_row, False, False, 0)
        self.main_layout.pack_start(self.middle_and_bottom, True, True, 0)
        self.add(self.main_layout)


    def update_spinbutton(self, _):
        """
        refresh the max line length possible using the spinbutton
        This does not play nicely with terminator.
        """
        with open(self.selected_script, 'r') as fp:
            lines_in_file = len(fp.readlines())
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

        file_cd = Gtk.MenuItem(label='Open directory')
        file_cd.connect("activate", self.file_cd_clicked)
        file_menu.append(file_cd)

        file_refresh = Gtk.MenuItem(label='Refresh script list')
        file_refresh.connect("activate", self.refresh_combobox)
        file_menu.append(file_refresh)

        file_menu.append(Gtk.SeparatorMenuItem())

        file_exit = Gtk.MenuItem(label='Quit')
        file_exit.connect("activate", Gtk.main_quit)
        file_menu.append(file_exit)

        self.main_menu_bar.append(file_menu_dropdown)

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
        try:
            self.combobox.set_active(script_list.index(current_script))
        except:
            pass

        self.set_title(f'ScriptRunner: {self.selected_dir.split("/")[-1]}')

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
        #_clean()
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
            self.set_title(f'ScriptRunner: {self.selected_dir.split("/")[-1]}')
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
            if self.term_state:
                # Find a more portable way to set the title
                runbashcommand.runbashcommand(command_str)
            else:
                # if the checkbox is unselected, run the program without
                # opening up a new terminal window
                proc = subprocess.Popen(f'{command_str}&', shell=True)
                proc.wait()

            self.refresh_combobox(None)

    def edit_clicked(self, _):
        """
        when the edit button is clicked, let's open the selected file in
        the default editor in a new terminal window
        """
        # As long as you use a separate module (runbashcommand) you
        # won't have issues like before
        entry_text = self.line_number.get_text()
        runbashcommand.runbashcommand(f'editor +{entry_text} {self.selected_script}')
        self.update_spinbutton(None)

    def lint_clicked(self, _):
        """
        when lint button is clicked, let's open pylint on the file in a
        new window of your default terminal emulator
        """
        self.refresh_combobox(None)
        if self.selected_script:
            runbashcommand.runbashcommand(f'pylint {self.selected_script}|less')
            #try:
                #proc = subprocess.Popen(''.join((
                #    f'x-terminal-emulator -T "LINT: {self.selected_script}" ',
                #    f'-e "pylint {self.selected_script}|less"')), shell=True)
                #proc.wait()
            #except:
            #    return

    def doc_clicked(self, _):
        """
        when pydoc button is clicked, let's open pydoc on the file in a
        new window of your default terminal emulator
        """
        self.refresh_combobox(None)
        if self.selected_script:
            mod_name = '.'.join(self.selected_script.split('.')[:-1])
            runbashcommand.runbashcommand(f'pydoc3 "{mod_name}"')
            #try:
            #    proc = subprocess.Popen(''.join((
            #        f'x-terminal-emulator -T "PYDOC: {mod_name} module" ',
            #        f'-e "pydoc3 \'{mod_name}\'"')), shell=True)
            #    proc.wait()
            #
            #except:
            #    return

    def on_checkbutton_toggled(self, _):
        self.term_state = self.checkbutton.get_active()

    def show_about(self, _):
        """
        show About dialog
        """
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_icon_from_file('icons/runner.png')
        about_dialog.set_title("About ScriptRunner")
        about_dialog.set_program_name("ScriptRunner")
        about_dialog.set_version("0.0")
        about_dialog.set_comments(
            "Simple, light-weight development environment for writing Python3 "\
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
