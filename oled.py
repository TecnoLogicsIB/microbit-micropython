# oled.py
# Original from https://github.com/fizban99/microbit_ssd1306

from microbit import i2c, Image

ADDR = 0x3C
screen = bytearray(513)  # send byte plus pixels
screen[0] = 0x40

def init():
    cmd = [[0xAE], [0xA4], [0xD5, 0xF0], [0xA8, 0x3F], [0xD3, 0x00],
           [0 | 0x0], [0x8D, 0x14], [0x20, 0x00], [0x21, 0, 127],
           [0x22, 0, 63], [0xa0 | 0x1], [0xc8], [0xDA, 0x12], [0x81, 0xCF],
           [0xd9, 0xF1], [0xDB, 0x40], [0xA6], [0xd6, 1], [0xaf]]
    for c in cmd:
        _send(c)
    clear()    

def clear():
    _pos()
    for i in range(1, 513):
        screen[i] = 0
    _pos()
    i2c.write(ADDR, screen)

def text(x, y, s):
    for i in range(0, min(len(s), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(s[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            screen[ind], screen[ind + 1] = col, col
    _pos(x * 5, y)
    ind0 = x * 10 + y * 128 + 1
    i2c.write(ADDR, b'\x40' + screen[ind0:ind + 1])

def image(filename):
    _pos()
    _send([0xae])
    with open(filename, 'rb') as my_file:
        for i in range(0, 16):
            i2c.write(ADDR, b'\x40' + my_file.read(64))
    _send([0xd6, 0])
    _send([0xa7])
    _send([0xaf])

def _pos(col = 0, page = 0):
    _send([0xb0 | page]) 
    c1, c2 = col * 2 & 0x0F, col >> 3
    _send([0x00 | c1]) 
    _send([0x10 | c2]) 

def _send(c):
    i2c.write(ADDR, b'\x00' + bytearray(c))

