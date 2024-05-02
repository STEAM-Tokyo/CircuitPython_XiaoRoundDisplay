import time
import board
import busio
from CircuitPython_XiaoRoundDisplay import XiaoRoundDisplay
import displayio
from adafruit_pcf8563.pcf8563 import PCF8563
import digitalio
import adafruit_sdcard
import storage
import os

# You need to release_displays after soft-rebooting the board
displayio.release_displays()

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
i2c = busio.I2C(board.SCL, board.SDA)

# PCF8563　Realtime clock settings
rtc = PCF8563(i2c)
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# GC9A01 display and Touch panel common settings
rotation = 0  # 0, 90, 180 or 270 degree

# Round Display for XIAO object
xrd = XiaoRoundDisplay(i2c, spi, rotation)
screen = xrd.display()  # Screen object

# displaytio settings
bitmap = displayio.Bitmap(screen.width, screen.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
# Create a Group
group = displayio.Group()
# Add the TileGrid to the Group
group.append(tile_grid)
# Add the Group to the Display
screen.root_group = group

# RTC
# Set datetime
t = time.struct_time((2024, 4, 30, 22, 13, 0, 1, -1, -1))
rtc.datetime = t
# Get date and time
print(
        "The date is {} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
        )
    )
print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))

# SD Card
# IMPORTRANT: You should create the SD card object AFTER initializing Display
try:
    cs = digitalio.DigitalInOut(board.D2)  # SD_CS = board.D2
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, '/sd')
    print(os.listdir('/sd'))
except:
    print("No SD card found.")
    pass

print("You can touch the screen to draw.")
while True:
    if xrd.is_touched():
        t = xrd.touch_read()
        if t is not None:
            x, y = t
            bitmap[x, y] = 1
    time.sleep(0.001)
