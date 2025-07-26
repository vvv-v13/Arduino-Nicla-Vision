from pyb import SPI, Pin
from st7735 import TFT
from sysfont import sysfont

import time

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

spi = SPI(4, SPI.MASTER, baudrate=20000000, polarity=0, phase=0)


def tftprinttest(font):
    tft.fill(TFT.BLACK)
    v = 30
    tft.text((0, v), "Hi World!", TFT.RED, font, 1, nowrap=True)
    v += font["Height"]
    tft.text((0, v), "Hello World!", TFT.YELLOW, font, 2, nowrap=True)
    v += font["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.GREEN, font, 3, nowrap=True)
    v += font["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, font, 4, nowrap=True)
    time.sleep_ms(1500)


def test_main():
    tftprinttest(sysfont)
    time.sleep_ms(100)


if __name__ == "__main__":

    spi = SPI(4, SPI.MASTER, baudrate=20000000, polarity=0, phase=0)

    tft = TFT(spi, dc, reset, cs, 128, 160)
    tft.initr()
    tft.rgb(True)
    test_main()
