from pyb import SPI, Pin
from st7735 import TFT, TFTColor

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

tft = TFT(spi, dc, reset, cs, 128, 160)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

minX = -2.0
maxX = 1.0
width = 160
height = 128
aspectRatio = 1.25

chars = " .,-:;i+hHM$*#@ "
clen = len(chars)
colours = [
    TFTColor(0xF0, 0x20, 0x20),
    TFT.RED,
    TFT.MAROON,
    TFT.GREEN,
    TFT.FOREST,
    TFT.BLUE,
    TFT.NAVY,
    TFT.CYAN,
    TFT.YELLOW,
    TFT.PURPLE,
    TFT.WHITE,
    TFT.GRAY,
    TFT.RED,
    TFT.MAROON,
    TFT.GREEN,
    TFT.FOREST,
    TFT.BLACK,
]

rangeX = maxX - minX
yScale = (rangeX) * (float(height) / width) * aspectRatio

for y in range(height):
    line = ""
    ytemp = y * yScale / height - yScale / 2
    for x in range(width):
        c = complex(minX + x * (rangeX) / width, ytemp)
        z = c
        colour = 0
        while abs(z) <= 2 and colour < clen:
            colour += 1
            z = z * z + c
        tft.pixel([y, x], colours[colour])
        line += chars[colour % clen]
    print(line)
