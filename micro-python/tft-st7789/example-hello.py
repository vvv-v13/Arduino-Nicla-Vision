from pyb import SPI, Pin

import st7789py as st7789
import vga2_16x32 as font
import time

# 1.69" TFT Display Module IPS LCD LED Screen 240X280 SPI Interface ST7789 Controller 3.3V

width = 280
height = 240

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

spi = SPI(4, SPI.MASTER, baudrate=int(1000000000 / 66), polarity=0, phase=0)


# Initialize display
display = st7789.ST7789(spi, width, height, reset=reset, dc=dc, cs=cs, rotation=0)

def write_command_byte(c):
    cs.low()
    dc.low()
    spi.send(c)
    cs.high()


def write_data_byte(c):
    cs.low()
    dc.high()
    spi.send(c)
    cs.high()


def write_command(c, *data):
    write_command_byte(c)
    if data:
        for d in data:
            write_data_byte(d)


# Reset the LCD.
reset.low()
time.sleep_ms(100)
reset.high()
time.sleep_ms(100)

write_command(0x11)  # Sleep Exit

# Memory Data Access Control
# Write 0xC8 for BGR mode.
# write_command(0x36, 0xC0)

# Interface Pixel Format
write_command(0x3A, 0x05)

# Display On
write_command(0x29)


display.fill(st7789.BLACK)
display.text(font, "SPI ST7789", 10, 10, color=0xF800)
display.text(font, "Display", 10, 50, color=0x07E0)
display.text(font, "Example", 10, 80, color=0x001F)
display.text(font, "Say hello!", 10, 170)
time.sleep(1)
display.text(font, "Say ...   ", 10, 170)
time.sleep(1)
display.text(font, "Say hello!", 10, 170)

