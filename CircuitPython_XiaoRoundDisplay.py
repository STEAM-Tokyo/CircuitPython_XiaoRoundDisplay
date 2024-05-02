#Author: Mitsuharu Aoyama
#Date: May 2024

# Dependencies:
#   adafruit_register
#   gc9a01
#   adafruit_bus_device

# Hardware:
# Round Display for XIAO


# Round Display for XIAO has CHSC6540 capacitive touch controller.
# Datasheet: https://szzxv.com/static/upload/file/20220301/1646141990530969.pdf

import board
import digitalio
import displayio
import gc9a01
from adafruit_register import i2c_bit
from adafruit_bus_device.i2c_device import I2CDevice

#Author: Mitsuharu Aoyama
#Date: May 2024

# Dependencies:
#   adafruit_register
#   gc9a01
#   adafruit_bus_device

# Hardware:

# Round Display for XIAO has CHSC6540 capacitive touch controller.
# Datasheet: https://szzxv.com/static/upload/file/20220301/1646141990530969.pdf

# GC9A01 display settings

# FourWire pins
tft_dc  = board.D3
tft_cs  = board.D1
# gc9a01 pins and settings
tft_bl  = board.D6  # Backlight
dw = 240  # display width
dh = 240  # display height

# CHSC6540 Capacitive Touch
CHSC6540_I2C_ADDRESS = 0x2e
CHSC6540_READ_POINT_LEN = 5
irq_pin = board.D7

# Screen size of the Round Display for XIAO 
xmax = 240
ymax = 240

class XiaoRoundDisplay():
    def __init__(self, i2c_bus, spi_bus, rotation):
        # Bus
        self._i2c = i2c_bus
        self._spi = spi_bus

        # Touch Interrupt ReQuest
        self._irq = digitalio.DigitalInOut(irq_pin) if irq_pin else None
        if self._irq:
            self._irq.switch_to_input(pull=digitalio.Pull.UP)

        self._buffer = bytearray(CHSC6540_READ_POINT_LEN)

        # Display
        self._spi = spi_bus
        self.rotation = rotation
        print("Touch panel Rotation={} degree".format(rotation))

    def display(self):
        # GC9A01 display
        # IMPORTANT: You need to release_displays before creating display_bus
        displayio.release_displays()
        self.display_bus = displayio.FourWire(
                        self._spi,
                        command=tft_dc,
                        chip_select=tft_cs
                        )    
        d = gc9a01.GC9A01(
                    self.display_bus,
                    width=dw,
                    height=dh,
                    backlight_pin=tft_bl
                    ,rotation=self.rotation
                    )
        return d

    def rotate(self, x, y):
        self.x = x
        self.y = y
        if self.rotation == 0:
            return x, y
        if self.rotation == 90:
            return y, (dw - x)
        if self.rotation == 180:
            return (dw - x), (dh - y)
        if self.rotation == 270:
            return (dh - y), x      

    def is_touched(self):
        if self._irq:
            return not self._irq.value
        return self.touch_read() is not None

    def touch_read(self):
        if self._irq and not self._irq.value:
            self.i2c_dev = I2CDevice(self._i2c, CHSC6540_I2C_ADDRESS)
            with self.i2c_dev:
                self.i2c_dev.readinto(self._buffer)

            results = [i for i in self._buffer]
            
            if results[0]:  # first byte is non-zero when touched
                x = results[2]  # 3rd byte is x
                y = results[4]  # 5th byte is y
                x1, y1 = self.rotate(x, y)
                return x1, y1  # Return (x1, y1) tuple
            return None
