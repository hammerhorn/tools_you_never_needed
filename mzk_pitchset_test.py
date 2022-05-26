#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import soxmusic

class PitchSetWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="<soxmusic.PitchSet>-tester")
        self.connect('delete-event', Gtk.main_quit)

        equal_divisions_label = Gtk.Label(label='equal divisions of one octave:')
        self.equal_divisions_spinbutton = Gtk.SpinButton.new_with_range(1, 100, 1)
        self.equal_divisions_spinbutton.set_value(12)
        self.equal_divisions_spinbutton.connect("value-changed", self.new_pitchset)
        self.output_label = Gtk.Label()

        self.new_pitchset(None)

        play_button = Gtk.Button(label='Play with SoX')
        play_button.connect("clicked", self.play_pitchset)

        main_box = Gtk.Box(
            border_width=10, orientation=Gtk.Orientation.VERTICAL)
        header_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_bar.pack_start(equal_divisions_label, False, None, 0)
        header_bar.pack_start(self.equal_divisions_spinbutton, False, None, 0)
        header_bar.pack_start(play_button, False, None, 0)
        main_box.pack_start(header_bar, False, None, 0)
        main_box.pack_start(self.output_label, False, None, 0)

        self.add(main_box)

    def play_pitchset(self, _):
        self.pitchset.play()
        self.pitchset.play_chord(wform='tri')

    def new_pitchset(self, _):
        self.pitchset = soxmusic.PitchSet(
            et=self.equal_divisions_spinbutton.get_value())
        self.output_label.set_markup(
            f"<span font='monospace'>{self.pitchset}</span>")
        self.resize(1, 1)

window = PitchSetWindow()
window.show_all()
Gtk.main()
