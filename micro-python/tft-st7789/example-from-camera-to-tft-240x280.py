import sensor
import time

from machine import Pin, SPI

# 1.69" TFT Display Module IPS LCD LED Screen 240X280 SPI Interface ST7789 Controller 3.3V

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


spi = SPI(4, baudrate=int(1000000000 / 66), polarity=1, phase=1)


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

    spi.write(img)

    cs.high()


# Reset the LCD.
reset.low()
time.sleep_ms(100)
reset.high()
time.sleep_ms(100)

write_command(0x01)  # Soft reset


write_command(0x11)  # Sleep Exit
time.sleep_ms(120)


# Interface Pixel Format
write_command(0x3A, 0x55)
time.sleep_ms(120)

write_command(0x21)  # Invert colors
time.sleep_ms(120)


@micropython.asm_thumb
def byteswap(r0, r1): # bytearray, len(bytearray)
    mov(r3, 1)
    lsr(r1, r3) # divide len by 2
    mov(r4, r0)
    add(r4, 1) # dest address
    label(LOOP)
    ldrb(r5, [r0, 0])
    ldrb(r6, [r4, 0])
    strb(r6, [r0, 0])
    strb(r5, [r4, 0])
    add(r0, 2)
    add(r4, 2)
    sub(r1, 1)
    bpl(LOOP)


# Display On
write_command(0x29)
time.sleep_ms(120)

sensor.reset()  # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565)  # must be this
sensor.set_framesize(sensor.HVGA)  # must be this
sensor.set_windowing(240, 320)
sensor.skip_frames(time=2000)  # Let new settings take affect.
clock = time.clock()  # Tracks FPS.

while True:
    clock.tick()  # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()  # Take a picture and return the image.

    img_byte_array = img.bytearray()
    byteswap(img_byte_array,len(img_byte_array))

    write_command(0x2C)  # Write image command...
    write_image(img)

    # swap back for IDE
    byteswap(img_byte_array,len(img_byte_array))


    print(clock.fps())  # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
