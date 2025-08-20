from microbit import i2c

def scan():
    found = []
    for addr in range(0x08, 0x78):
        try:
            i2c.read(addr, 1)
            found.append(addr)
        except:
            pass
    print("I2C:", [hex(a) for a in found])
scan()