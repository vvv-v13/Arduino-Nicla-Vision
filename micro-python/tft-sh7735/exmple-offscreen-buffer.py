from framebuf import FrameBuffer, RGB565
from pyb import SPI, Pin
from st7735 import TFT

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

buf = bytearray(128*160*2)
fb = FrameBuffer(buf, 128, 160, RGB565)

tft._setwindowloc((0, 0), (127, 159))

size = 20
(xmax, ymax) = (128-size, 160-size)
(x, y) = (size, size)
(vx, vy) = (1, 1)

while True:
    fb.fill(0)
    fb.ellipse(x, y, size, size, 0xffff, True)
    x += vx
    if x == xmax or x == size:
        vx = -vx
    y += vy
    if y == ymax or y == size:
        vy = -vy
    tft._writedata(buf)
