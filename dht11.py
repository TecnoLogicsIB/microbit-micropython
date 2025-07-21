from microbit import *
import utime

class DHT11:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        buf = bytearray(5)
        self.pin.write_digital(0)
        utime.sleep_ms(20)
        self.pin.write_digital(1)
        utime.sleep_us(40)
        self.pin.read_digital()

        while self.pin.read_digital() == 1:
            pass
        while self.pin.read_digital() == 0:
            pass
        while self.pin.read_digital() == 1:
            pass

        for i in range(40):
            while self.pin.read_digital() == 0:
                pass
            t = utime.ticks_us()
            while self.pin.read_digital() == 1:
                pass
            if utime.ticks_diff(utime.ticks_us(), t) > 50:
                buf[i // 8] = (buf[i // 8] << 1) | 1
            else:
                buf[i // 8] = (buf[i // 8] << 1)

        checksum = sum(buf[0:4]) & 0xFF
        if buf[4] != checksum:
            return None, None

        humidity = buf[0]
        temperature = buf[2]
        return temperature, humidity
