#Hack for Borken Coral Enviro Board
# 6 August 2023
# Manish Mahajan

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageDraw
from time import sleep
import argparse
import itertools
import os

from HDC2010 import HDC2080
from opt3001 import opt3001

def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 0), msg, fill='white')
def _none_to_nan(val):
    return float('nan') if val is None else val

def main():
    # Pull arguments from command line.
    parser = argparse.ArgumentParser(description='Enviro Kit Demo')
    parser.add_argument('--display_duration',
                        help='Measurement display duration (seconds)', type=int,
                        default=5)
    parser.add_argument('--upload_delay', help='Cloud upload delay (seconds)',
                        type=int, default=300)
    args = parser.parse_args()
    # Create instances of sensors, display and Cloud IoT.
    hdc = HDC2080()
    opt = opt3001.OPT3001(0x45)
    opt.write_config_reg(opt3001.I2C_LS_CONFIG_CONT_FULL_800MS)
 
    serial = spi(device=0, port=0)
    display = ssd1306(serial,gpio=noop(),height=32,rotate=2)
    while True:
    # Indefinitely update display and upload to cloud.
        sensors = {}
        read_period = int(args.upload_delay / (2 * args.display_duration))
        for read_count in itertools.count():
            # First display temperature and RH.
            sensors['temperature'] = hdc.readTemperature()
            sensors['humidity'] = hdc.readHumidity()
            msg = 'Temp: %.2f C\n' % _none_to_nan(sensors['temperature'])
            msg += 'RH: %.2f %%' % _none_to_nan(sensors['humidity'])
            update_display(display, msg)
            print(msg+"\n")
            sleep(args.display_duration)
            # After 5 seconds, switch to light and pressure.
            sensors['ambient_light'] = opt.read_lux_float()
            sensors['pressure'] = None #sensor does not work
            msg = 'Light: %.2f lux\n' % _none_to_nan(sensors['ambient_light'])
            msg += 'Pressure: %.2f kPa' % _none_to_nan(sensors['pressure'])
            update_display(display, msg)
            print(msg+"\n")
            sleep(args.display_duration)
if __name__ == '__main__':
    main()
