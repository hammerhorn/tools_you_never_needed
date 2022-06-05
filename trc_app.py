#!/usr/bin/env python3
#coding=utf8
"""
Graphical front-end using GTK.  Generate tone rows for twelve-tone
serialism, using class <tonerow.Tonerow>.

I've converted it to Gtk.Application style rather than script style with
as little work on my part as possible.
"""
import argparse
import atexit
import os
import shutil
import subprocess
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

import tonerow
import trc_gtk

atexit.register(tonerow.Tonerow.clean)

def _parse_args():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args() if __name__ == '__main__' else None

class App(Gtk.Application):
    """
    It's an Application now, so I can now use Gio.Notification.  Also
    this means that only one instance can be running at any given time.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.kriso.tonerow", **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = trc_gtk.TonerowWindow(application=self)
            self.window.set_title(f'Tonerow Computer: {self.window.row.seq}')
            self.window.file_save.connect("activate", self.save)
            self.window.file_save_midi.connect("activate", self.save_midi)
            self.window.file_save_abc.connect("activate", self.save_abc)
            self.window.file_save_png.connect("activate", self.save_png)
            self.window.file_exit.connect("activate", self.quit)
            self.window.show_all()
            self.window.present()

    def save(self, _):
        """
        save as plain text, duodecimal notation
        """
        self.window.row.write_txt(self.window.row.basename, 'row')
        self._notify_filesave('row')

    def save_midi(self, _):
        proc = subprocess.Popen(
	        'abc2midi __data__/tmp.abc -Q 140', shell=True)
        proc.wait()
        shutil.copy(
            '__data__/tmp1.mid',
            f'{os.getcwd()}/{self.window.row.basename}.mid')
        self._notify_filesave('mid')

    def save_abc(self, _):
        shutil.copy(
            '__data__/tmp.abc',
            f'{os.getcwd()}/{self.window.row.basename}.abc')
        self._notify_filesave('abc')

    def save_png(self, _):
        shutil.copy(
            '__data__/tmp-cropped.png',
            f'{os.getcwd()}/{self.window.row.basename}.png')
        self._notify_filesave('png')

    def _notify_filesave(self, file_extension):
        notification = Gio.Notification()  # Make a decorator?
        notification.set_body(
            f'{self.window.row.basename}.{file_extension} saved')
        notification.set_title('')
        notification.set_priority(Gio.NotificationPriority.HIGH)
        self.send_notification(None, notification)        

    def quit(self, _):
        super().quit()

def main():
    """
    Run the application
    """
    _parse_args()
    app = App()
    app.run(sys.argv)

if __name__ == "__main__":
    main()
