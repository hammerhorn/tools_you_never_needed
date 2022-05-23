#!/usr/bin/env python3
"""
A gui app to help me understand my old <music.Pitch> class
"""
import decimal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gtkstuff
import soxmusic

#output_count = 0


# Gonna go all out with classes on this one lol
class InputFrame(Gtk.Frame):
    def __init__(self, mnemonic='Alt+_C', **kwargs):
        super().__init__(**kwargs)
        self.box = Gtk.Box(border_width=10, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.button = Gtk.Button.new_with_mnemonic(mnemonic)
        self.box.pack_end(self.button, True, False, 0)
        self.add(self.box)

class OutputFrame(Gtk.Frame):
    def __init__(self, name="Pitch name", **kwargs):
        super().__init__(**kwargs)
        self.label = Gtk.Label()
        self.box = Gtk.Box(border_width=10)
        self.box.pack_start(self.label, False, None, 0)
        self.add(self.box)

class PitchBox(Gtk.Box):
    def __init__(self, button_mnem='Alt+_C', name='PitchBox', **kwargs):
        super().__init__(border_width=10, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.pitch = soxmusic.Pitch() # maybe change this later
        self.input_frame = InputFrame(label=name, mnemonic=button_mnem)
 #       output_count += 1
        self.output_frame = OutputFrame(label=name)
        self.autoplay = False
        self.pack_start(self.output_frame, False, None, 0)
        self.pack_start(self.input_frame, False, None, 0)

class LabelledComboBox(Gtk.Box):
    def __init__(self,text="Make a choice:", combo_list=None):
        super().__init__()
        self.label = Gtk.Label()
        self.label.set_markup(text)
        if not combo_list:
            combo_list = []
        list_store = Gtk.ListStore(str)
        for item in combo_list:
            list_store.append([item])

        self.combobox = Gtk.ComboBox.new_with_model(list_store)
        self.combobox.set_active(0)
        self.update_combo(self.combobox)
        self.combobox.connect("changed", self.update_combo)

        renderer_text = Gtk.CellRendererText()
        self.combobox.pack_start(renderer_text, True)
        self.combobox.add_attribute(renderer_text, "text", 0)
        self.pack_end(self.combobox, False, None, 0)
        self.pack_end(self.label, False, None, 0)
        
    def update_combo(self, combo):
        """
        update selected item in response to combobox
        """
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.selected_item = model[tree_iter][0]

class NotenameBox(PitchBox):
    def __init__(self):
        super().__init__(name='by note name', button_mnem='play (_note name)')

        # MAKE THE WIDGETS
        #self.input_frame.lettername_entrybox = gtkstuff.LabelledEntryBox(
        #    'Note name:', orientation=Gtk.Orientation.HORIZONTAL)
        #self.input_frame.lettername_entrybox.entry.set_width_chars(3)
        #self.input_frame.lettername_entrybox.entry.set_text('C')
        self.output_frame.set_label('Pitch #1')
        notename_list = [i[0] for i in soxmusic.NOTENAMES]
        self.input_frame.lettername_entrybox = LabelledComboBox(
            'note name:', notename_list)
        self.input_frame.lettername_entrybox.combobox.connect(
            "changed", self.on_note_changed)
        self.input_frame.octave_entrybox = gtkstuff.LabelledSpinButtonBox(
            label_markup="octave:",
            lo=-1,
            hi=10,
            step=1,
            default=4,
            orientation=Gtk.Orientation.HORIZONTAL)
        self.input_frame.octave_entrybox.spinbutton.set_alignment(xalign=1)
        self.input_frame.octave_entrybox.spinbutton.set_width_chars(3)
        self.input_frame.octave_entrybox.spinbutton.connect(
            "value-changed", self.on_note_changed)

        self.input_frame.cents_entrybox = gtkstuff.LabelledSpinButtonBox(
            label_markup="cents:",
            lo=-50,
            hi=50,
            step=1,
            default=0,
            orientation=Gtk.Orientation.HORIZONTAL)
        self.input_frame.cents_entrybox.spinbutton.set_alignment(xalign=1)
        self.input_frame.cents_entrybox.spinbutton.set_width_chars(3)
        #self.input_frame.cents_entrybox.spinbutton.connect(
        #    "value-changed", self.on_note_changed)
        self.input_frame.button.connect("clicked", self.on_click)

        # MAKE ADDITIONAL LAYOUT BOXES
        self.input_frame.entries = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # PACK THEM
        self.input_frame.entries.pack_start(
            self.input_frame.lettername_entrybox, False, None, 0)
        self.input_frame.entries.pack_start(
            self.input_frame.octave_entrybox, False, None, 0)
        self.input_frame.entries.pack_start(
            self.input_frame.cents_entrybox, False, None, 0)
        self.input_frame.box.pack_start(
           self.input_frame.entries, False, None, 0)

        self.pack_start(self.input_frame, False, None, 0)
        self.pack_start(self.output_frame, False, None, 0)
        self.update_output_label(None)

    def update_output_label(self, _):
        self.pitch = soxmusic.Pitch(
            self.input_frame.octave_entrybox.spinbutton.get_value(),
            self.input_frame.lettername_entrybox.selected_item,
            float(self.input_frame.cents_entrybox.spinbutton.get_value()))
        self.output_frame.label.set_markup(
            '<span font="serif" size="large"><b>'\
            f'{self.pitch.__str__()}</b></span>')

    def on_note_changed(self, _):
        self.update_output_label(None)
        if self.autoplay:
            self.pitch.play()
        

    def on_click(self, _):
        """
        define the note by notename
        """
        self.update_output_label(None)
        print('boop', end='', flush=True)
        self.pitch.play()

class FrequencyBox(PitchBox):
    def __init__(self):
        super().__init__(name='by frequency (hertz)', button_mnem='play (_frequency)')
        self.output_frame.set_label('Pitch #2')
        self.input_frame.frequency_entrybox = gtkstuff.LabelledSpinButtonBox(
            label_markup='frequency (Hz):',
            lo=-8,
            hi=32000.,
            step=.01,
            default=440.,
            orientation=Gtk.Orientation.HORIZONTAL)
        self.input_frame.frequency_entrybox.spinbutton.set_alignment(xalign=1)
        self.input_frame.frequency_entrybox.spinbutton.connect(
            "value-changed", self.on_note_changed)
        self.input_frame.button.connect("clicked", self.on_click)
        self.input_frame.box.pack_start(self.input_frame.frequency_entrybox, False, None, 0)
        self.input_frame.box.pack_start(self.input_frame.button, False, None, 0)
        self.update_output_label(None)

    def update_output_label(self, _):
        self.pitch = soxmusic.Pitch(
            freq=self.input_frame.frequency_entrybox.spinbutton.get_value())
        self.output_frame.label.set_markup(
            f'<span font="serif" size="large"><b>{self.pitch.__str__()}'\
            '</b></span>')
        #print(self.autoplay)
        #if self.autoplay:
        #    self.pitch.play()

    def on_click(self, _):
        """define the note by frequency"""
        self.update_output_label(None)
        print('beep', end='', flush=True)
        self.pitch.play()

    def on_note_changed(self, _):
        self.update_output_label(None)
    #    decimal.getcontext().prec = 2
    #    freq_dec = decimal.Decimal(self.pitch.freq)
    #    #if  
    #    if self.autoplay:# and (freq_dec - decimal.Decimal(int(self.pitch.freq)) == 0.0):
    #        self.pitch.play()

class PitchTestBox(Gtk.Box):
    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL, spacing=10, border_width=10)
        #self.pitchcount = 0
        # MAKE THE WIDGETS
        #title = Gtk.Label()
        #title.set_markup("<span font='serif' size='x-large'><i>Pitch Test</i></span>")

        #instructions = Gtk.Label()
        #instructions.set_markup(
         #   "<u>INSTRUCTIONS</u>: please turn off the JACK server if it is running.\n"
         #   "('b'=flat sign, '#'=sharp sign)")
        self.notename_box = NotenameBox()#'Pitch #1')
        self.frequency_box = FrequencyBox()#'Pitch #2')

        # MAKE LAYOUT BOXES
        methods_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.autoplay = False
        self.autoplay_switch = Gtk.Switch()
        self.autoplay_switch.connect("notify::active", self.on_switch_activated)
        self.autoplay_switch.set_active(False)
        switchbox = Gtk.Box(border_width=30, orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        switchbox.pack_start(self.autoplay_switch, False, None, 0)
        switchbox.pack_start(Gtk.Label('auto-play (note name and octave only)'), False, None,0)
        right_column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_column.pack_start(self.frequency_box, False, None, 0)
        right_column.pack_start(switchbox, True, False, 0)

        # PACK THEM
        methods_box.pack_start(self.notename_box, False, None, 0)
        methods_box.pack_start(right_column, False, None, 0)

        #self.pack_start(title, False, None, 0)
        #self.pack_start(Gtk.Separator(), False, None, 0)        
        #self.pack_start(instructions, False, None, 0)
        self.pack_start(methods_box, False, None, 0)
        
    def on_switch_activated(self, switch, gparam):
        if self.autoplay_switch.get_active():
            self.notename_box.autoplay = True
            #self.frequency_box.autoplay = True
            self.notename_box.input_frame.lettername_entrybox.label.set_markup(r'<b>note name</b>:')
            self.notename_box.input_frame.octave_entrybox.label.set_markup(r'<b>octave</b>:')
        else:
            self.notename_box.autoplay = False
            #self.frequency_box.autoplay = False
            self.notename_box.input_frame.lettername_entrybox.label.set_markup('note name:')
            self.notename_box.input_frame.octave_entrybox.label.set_markup(r'octave:')
def main():
    # MAKE A MAIN WINDOW AND RUN THE THING
    window = Gtk.Window(title="<soxmusic.Pitch>-tester")        
    window.connect('delete-event', Gtk.main_quit)
    window.add(PitchTestBox())
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
