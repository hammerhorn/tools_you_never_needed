#!/usr/bin/env python3
"""
Calculate values related to apparent temperature and relative and absolute
humidity
"""
import ambientconditions

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def main():
    """ Main loop"""
    print(
        "\n***Enter a blank value to start over, ^C to quit***")

    while True:
        try:
            conditions = ambientconditions.Ambient(
                float(input("\rtemperature (°F): ")),
                float(input("relative humidity: ")))

            print(
                f"\nabsolute humidity at std. pressure = "\
                f"{conditions.ab_hum:.2f} g/m³"\
                f"\ndew point = {conditions.dew_point * 1.8 + 32:.2f}°F "\
                "(over 60°F is hot riding a bike)")

            if conditions.app_heat_index:
                print(f"Approximate heat index(±1.3) = "\
                      f"{conditions.app_heat_index:.2f}°F")
            print(f"vapor pressure deficit = {conditions.vp_deficit:.2f} kPa "\
                  "(ideal range is 0.4-1.6 kPa)\n")

        except KeyboardInterrupt:
            break
        except ValueError:
            pass

if __name__ == "__main__":
    main()
