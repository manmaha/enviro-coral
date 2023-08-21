#!/usr/bin/python3 -u

from luma.core.interface.serial import i2c, spi, pcf8574, noop
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010

display = ssd1306(serial_interface=spi(),
                                    gpio=noop(), height=32, rotate=2)
#while True:
with canvas(display) as draw:
    draw.rectangle(display.bounding_box, outline="white", fill="black")
    draw.text((30, 40), "Hello World", fill="white")


def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 0), msg, fill='white')

update_display(display,'Hello Manish')
