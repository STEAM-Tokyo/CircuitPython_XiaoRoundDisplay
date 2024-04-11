# Round Display for XIAO Touch Driver for CircuitPython
[Seeed Studio Round Display for XIAO](https://wiki.seeedstudio.com/get_start_round_display/) has the capacitive touch function. This CircuitPython driver enables you to get the touched (X, Y) coordinates.

<img src="https://files.seeedstudio.com/wiki/round_display_for_xiao/rounddisplay.jpg" width="600">

## Installation
Simply copy the Xiao_Round_Display_Touch.py to the lib folder of your board.

## Usage example

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
        print("Touched: ", touch.touch_read())  # touch_read() returns (x, y) as a tuple.
        time.sleep(0.1)
```

# Round Display for XIAO用タッチドライバ
[Seeed Studio Round Display for XIAO](https://wiki.seeedstudio.com/get_start_round_display/) には静電容量タッチパネルが搭載されています。このCircuitPythonのドライバを使うことで、タッチした(X, Y)座標を取得することができます。

## インストール
本レポジトリのXiao_Round_Display_Touch.pyをCircuitPythonがインストールされたマイコンにコピーしてください。

## 使い方の例
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
        print("Touched: ", touch.touch_read())  # touch_read()はタッチした座標をタプル(x, y)として返します。
        time.sleep(0.1)
```
