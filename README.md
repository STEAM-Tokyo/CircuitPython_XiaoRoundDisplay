# Round Display for XIAO Touch Driver for CircuitPython
Seeed Studio Round Display for XIAO has the capacitive touch function. This CircuitPython driver enables you to get the touched (X, Y) coordinates.

## Installation
Simply copy the Xiao_Round_Display_Touch.py to the lib folder of your board.

## Usage

```py
import board
import busio
import time
from Xiao_Round_Display_Touch import CapTouch

# Touch init
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
irq_pin = board.D7
touch = CapTouch(i2c, irq_pin=irq_pin)

while True:
    if touch.is_touched():
        print("Touched: ", touch.touch_read())
        time.sleep(0.1)
```
