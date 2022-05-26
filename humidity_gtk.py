#!/usr/bin/env python3
'''
gui humidity calcultor: absolute humidity, dew point, heat index,
                        vapor pressure deficit
'''
# Third-party
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Local modules
import ambientconditions
import gtkstuff

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

heading_list = []


class LabelledSpinButtonBox(gtkstuff.LabelledSpinButtonBox):
    '''
    consists of a text entry box with a text label above it
    '''
    def __init__(self, **kwargs):
        super().__init__(
            label_markup=f'<small><b>{text}</b></small>',
            orientation=Gtk.Orientation.VERTICAL, spacing=2, **kwargs)

class HumidityWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Humidity Calculator")
        self.set_border_width(10)
        self.set_icon_from_file('icons/cloud.png')
        self.connect('destroy', Gtk.main_quit)

        #Fahrenheit box
        self.temp_f_box = LabelledSpinButtonBox(
            -135.8, 131.1, .1, 70, 'Temperature(°F):')
        self.temp_f_box.spinbutton.connect("value-changed", self.on_click)

        #Humidity box
        self.humidity_box = LabelledSpinButtonBox(0.1, 99.9, .1, 45, 'Relative humidity(%):')
        self.humidity_box.spinbutton.connect("value-changed", self.on_click)

        self.headings = Gtk.Label()
        self.output = Gtk.Label()

        bottom_left = Gtk.Box()
        bottom_left.pack_start(self.headings, True, True, 0)

        bottom_right = Gtk.Box()
        bottom_right.pack_start(self.output, True, True, 10)

        top_box = Gtk.Box(spacing=10)
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        bottom_box.set_border_width(15)
        big_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)

        top_box.pack_start(self.temp_f_box, True, True, 0)
        top_box.pack_start(self.humidity_box, True, True, 0)

        bottom_box.pack_start(bottom_left, True, True, 0)
        bottom_box.pack_start(bottom_right, True, True, 0)
        bottom_box_frame = Gtk.Frame()
        bottom_box_frame.add(bottom_box)

        big_box.pack_start(top_box, True, True, 0)
        big_box.pack_start(bottom_box_frame, True, True, 0)

        self.add(big_box)

    def on_click(self, _):
        '''
        when button is clicked, plugs the two input values into all the equations
        and outputs the results
        '''
        heading_list = ["<span font='serif' size='large'>absolute humidity"\
                        "</span> (<i>std. pressure</i>) =",
                        "<span font='serif' size='large'>dew point</span> (<i>"\
                        "over 60 is hot if you're sweating</i>) ="]
        conditions = ambientconditions.Ambient(
            float(self.temp_f_box.spinbutton.get_text()),
            float(self.humidity_box.spinbutton.get_text())
        )
        fahr_dewpoint = conditions.dew_point * 1.8 +32
        approx = conditions.app_heat_index
        output_list = [
            f'\n<b>{conditions.ab_hum:.2f} g/m³</b>',
            f'<b>{fahr_dewpoint:.1f}°F</b>']
        if fahr_dewpoint >= 60.0:
            output_list[1] = f'<span color="red">{output_list[1]}</span>'
        if approx:
            heading_list.append(
                f"<span font='serif' size='large'>approximate heat index"\
                "</span>(<i>±1.3</i>) =")
            output_list.append(f"<b><span color='red'>{approx:.2f}°F</span></b>")
        heading_list.append(
            '<span font="serif" size="large">vapor pressure deficit</span> '\
            '(<i>0.4-1.6 kPa is acceptable</i>) =')

        self.headings.set_markup('\n'.join(heading_list))
        self.headings.set_justify(Gtk.Justification.RIGHT)

        vpd = conditions.vp_deficit
        vpd_string = f'<b>{vpd:.2f} kPa</b>'
        if vpd > 1.6 or vpd < .4:
            vpd_string = f'<span color="red">{vpd_string}</span>'
        output_list.append(vpd_string)

        # compile all results (will be placed in the right column)
        output_str = '\n'.join(output_list)
        self.output.set_markup(f"{output_str}\n")
        self.output.set_xalign(0)

def main():
    app_window = HumidityWindow()
    app_window.on_click(None)
    app_window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
