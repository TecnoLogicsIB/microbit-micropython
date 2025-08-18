# comprovació correspondència dels pins S de la placa Robot_bit amb els canals del PCA9685 intern

from microbit import *
# from microbit import i2c, sleep

PCA9685_ADDRESS = 0x40  # Adreça I2C del xip PCA9685 (0x40 per defecte)

# Funció interna per escriure un valor a un registre concret del PCA9685
def write_register(reg, value):  
    i2c.write(PCA9685_ADDRESS, bytes([reg, value]))

def set_pwm_freq(freq):
    prescale_val = int(25000000.0 / (4096 * freq) - 1)
    write_register(0x00, 0x10)     # Sleep
    write_register(0xFE, prescale_val)  # Set prescale
    write_register(0x00, 0xA1)     # Wake + auto-increment

def set_pwm(channel, on, off):
    base = 0x06 + 4 * channel
    i2c.write(PCA9685_ADDRESS, bytes([base, on & 0xFF]))
    i2c.write(PCA9685_ADDRESS, bytes([base+1, (on >> 8) & 0xFF]))
    i2c.write(PCA9685_ADDRESS, bytes([base+2, off & 0xFF]))
    i2c.write(PCA9685_ADDRESS, bytes([base+3, (off >> 8) & 0xFF]))

def set_servo_angle(channel, angle):
    pulse = int(500 + (angle / 180.0) * 2000)  # microsegons
    pwm_val = int(pulse * 4096 / 20000)        # per 20ms
    set_pwm(channel, 0, pwm_val)

# Inicialitzar el xip
set_pwm_freq(50)

# Provar tots els canals del 0 al 15
for channel in range(16):
    display.scroll(str(channel))  # Mostra quin canal s'està provant
    set_servo_angle(channel, 0)
    sleep(1000)
    set_servo_angle(channel, 90)
    sleep(1000)
    set_servo_angle(channel, 180)

    sleep(1000)
