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

tft = TFT(spi,  dc, reset, cs, 128, 160)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

f = open('tux-128x160.bmp', 'rb')

if f.read(2) == b'BM':  # header
    dummy = f.read(8)  # file size(4), creator bytes(4)
    offset = int.from_bytes(f.read(4), 'little')
    hdrsize = int.from_bytes(f.read(4), 'little')
    width = int.from_bytes(f.read(4), 'little')
    height = int.from_bytes(f.read(4), 'little')
    if int.from_bytes(f.read(2), 'little') == 1:  # planes must be 1
        depth = int.from_bytes(f.read(2), 'little')
        # compress method == uncompressed
        if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:
            print("Image size:", width, "x", height)
            rowsize = (width * 3 + 3) & ~3
            if height < 0:
                height = -height
                flip = False
            else:
                flip = True
            w, h = width, height
            if w > 128:
                w = 128
            if h > 160:
                h = 160
            tft._setwindowloc((0, 0), (w - 1, h - 1))
            for row in range(h):
                if flip:
                    pos = offset + (height - 1 - row) * rowsize
                else:
                    pos = offset + row * rowsize
                if f.tell() != pos:
                    dummy = f.seek(pos)
                for col in range(w):
                    bgr = f.read(3)
                    tft._pushcolor(TFTColor(bgr[2], bgr[1], bgr[0]))
spi.deinit()
