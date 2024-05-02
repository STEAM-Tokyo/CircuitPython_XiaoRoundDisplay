日本語の説明文は下のほうにあります。

# Round Display for XIAO Touch Driver for CircuitPython
[Seeed Studio Round Display for XIAO](https://wiki.seeedstudio.com/get_start_round_display/) has GC9A01 LCD with the capacitive touch function.
By using this CircuitPython driver, you can create the display object and also get the touched (X, Y) coordinates.
You can set the screen rotation by 90 degrees.

<img src="https://files.seeedstudio.com/wiki/round_display_for_xiao/rounddisplay.jpg" width="600">

## Installation
Simply copy the CircuitPython_XiaoRoundDisplay.py to the lib folder of your board.

## Dependencies
Requires following libraries.
- adafruit_bus_device
- adafruit_register
- gc9a01 (distributed in the community bundle)

[CircuitPython.org](https://circuitpython.org/libraries/)

## Usage example

```py
import time
import board
import busio
from CircuitPython_XiaoRoundDisplay import XiaoRoundDisplay
import displayio

# You need to release_displays after soft-rebooting the board
displayio.release_displays()

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
i2c = busio.I2C(board.SCL, board.SDA)

# GC9A01 display and Touch panel common settings
rotation = 0  # 0, 90, 180 or 270 degree

# Round Display for XIAO object
xrd = XiaoRoundDisplay(i2c, spi, rotation)
screen = xrd.display()  # Screen object

# displayio settings
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

print("You can touch the screen to draw.")
while True:
    if xrd.is_touched():
        t = xrd.touch_read()
        if t is not None:
            x, y = t
            bitmap[x, y] = 1
    time.sleep(0.001)
```

# Round Display for XIAO用CircuitPythonドライバ
[Seeed Studio Round Display for XIAO](https://wiki.seeedstudio.com/get_start_round_display/) にはGC9A01ディスプレイと静電容量タッチパネルが搭載されています。
このCircuitPythonのドライバを使うことで、GC9A01のディスプレイオブジェクトを作成するとともに、タッチした(X, Y)座標を取得することができます。
また、90度単位で画面の回転を設定できます。

## インストール
本レポジトリのCircuitPython_XiaoRoundDisplay.pyをCircuitPythonがインストールされたマイコンにコピーしてください。

## 依存関係
下記CircuitPythonライブラリのインストールが必要です。
- adafruit_bus_device
- adafruit_register
- gc9a01 (Community Bundleに含まれています。)

[ライブラリ配布元](https://circuitpython.org/libraries/)

## 使い方の例
```py
import time
import board
import busio
from CircuitPython_XiaoRoundDisplay import XiaoRoundDisplay
import displayio

# ボードをソフトリブートした後にはrelease_displaysが必要
displayio.release_displays()

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
i2c = busio.I2C(board.SCL, board.SDA)

# GC9A01とタッチパネルの共通設定
rotation = 0  # 0, 90, 180 or 270 度

# Round Display for XIAO オブジェクト
xrd = XiaoRoundDisplay(i2c, spi, rotation)
screen = xrd.display()  # Screen object

# displayio設定
bitmap = displayio.Bitmap(screen.width, screen.height, 2)

# 黒と白のパレットを作成
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

# BitmapとPaletteを使ってTileGridを作成
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
# Groupを作成
group = displayio.Group()
# TileGridをGroupに追加
group.append(tile_grid)
# GroupをDisplayに追加
screen.root_group = group

print("You can touch the screen to draw.")
while True:
    if xrd.is_touched():
        t = xrd.touch_read()
        if t is not None:
            x, y = t
            bitmap[x, y] = 1
    time.sleep(0.001)
```
