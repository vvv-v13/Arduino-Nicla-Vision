# 1.8" 128x240 TFT LCD display with ST7735 driver

import sensor
import time
import struct
from machine import Pin, SPI

# TFT       Nicla Vision
# ----------------------
# LED/BLK   VDDIO_EXT
# SCK       SCLK
# SDA       COPI
# A0/DC     D1
# RESET     D0
# СS        CS
# GND       GND
# VCC       VDDIO_EXT


cs = Pin("CS", Pin.OUT_OD)
reset = Pin("D0", Pin.OUT_PP)
dc = Pin("D1", Pin.OUT_PP)


# NOTE: The SPI clock frequency will not always be the requested frequency. The hardware only supports
# frequencies that are the bus frequency divided by a prescaler (which can be 2, 4, 8, 16, 32, 64, 128 or 256).
spi = SPI(4, baudrate=int(1000000000 / 66), polarity=0, phase=0)


def write_command_byte(c):
    cs.low()
    dc.low()
    spi.write(bytes([c]))
    cs.high()


def write_data_byte(c):
    cs.low()
    dc.high()
    spi.write(bytes([c]))
    cs.high()


def write_command(c, *data):
    write_command_byte(c)
    if data:
        for d in data:
            write_data_byte(d)


def write_image(img):
    cs.low()
    dc.high()
    reversed_img = struct.unpack('H' * (img.size() // 2), img)
    reversed_array = struct.pack('>' + 'H' * len(reversed_img), *reversed_img)
    spi.write(reversed_array)
    cs.high()


# Reset the LCD.
reset.low()
time.sleep_ms(100)
reset.high()
time.sleep_ms(100)

write_command(0x11)  # Sleep Exit
time.sleep_ms(120)

# Memory Data Access Control
# Write 0xC8 for BGR mode.
write_command(0x36, 0xC0)

# Interface Pixel Format
write_command(0x3A, 0x05)

sensor.reset()  # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565)  # must be this
sensor.set_framesize(sensor.QQVGA2)  # must be this
sensor.skip_frames(time=2000)  # Let new settings take affect.
clock = time.clock()  # Tracks FPS.

while True:
    clock.tick()  # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()  # Take a picture and return the image.

    write_command(0x2C)  # Write image command...
    write_image(img)

    # Display On
    write_command(0x29)

    print(clock.fps())  # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
