# robotbit.py — micro:bit + Robot:bit (PCA9685)
# Ús unificat a 50 Hz per a: SERVOS, LEDS (source) i MOTORS (velocitat)

from microbit import i2c, sleep  # I2C i pausa

ADR = 0x40  # Adreça del PCA9685

# --- Ports S1–S8 → canals 8–15 (per a servos/LEDs) ---
PORTS = {
    1: 8, 2: 9, 3: 10, 4: 11,
    5: 12, 6: 13, 7: 14, 8: 15
}

ini = False         # inicialització feta (posa 50 Hz un cop)
angles = {}         # últim angle per port (servo)
CURRENT_HZ = 50     # treballarem sempre a 50 Hz

# --- Baix nivell PCA9685 ---
def reg(r, v):
    i2c.write(ADR, bytes([r & 0xFF, v & 0xFF]))

def pwm(c, on, off):
    b = 0x06 + 4 * c
    i2c.write(ADR, bytes([b,   on & 255]))
    i2c.write(ADR, bytes([b+1, on >> 8]))
    i2c.write(ADR, bytes([b+2, off & 255]))
    i2c.write(ADR, bytes([b+3, off >> 8]))

def freq(f):
    # Prescaler: 25 MHz / (4096 * f) - 1
    p = int(25000000 / (4096 * f) - 1)
    reg(0x00, 0x10)      # MODE1: SLEEP
    reg(0xFE, p)         # PRE_SCALE
    reg(0x01, 0x04)      # MODE2: OUTDRV (push-pull) → LEDs 'source' i motors
    reg(0x00, 0x21)      # MODE1: AI + ALLCALL, wake
    sleep(5)
    reg(0x00, 0xA1)      # MODE1: RESTART + AI + ALLCALL

def _init_once():
    global ini
    if not ini:
        freq(CURRENT_HZ)  # un sol lloc: 50 Hz per a tot
        ini = True

# --- SERVOS (sense canvis de comportament) ---
def angle(c, a):
    p_us = int(500 + a / 180 * 2000)  # 500..2500 us
    v = int(p_us * 4096 / 20000)      # període 20 ms a 50 Hz
    pwm(c, 0, v)

def mou_servo(p, a):
    _init_once()
    if p in PORTS:
        angle(PORTS[p], a)
        angles[p] = a

def mou_servo_suau(p, a_fi, v=10):
    if p not in PORTS:
        return
    a_ini = angles.get(p, a_fi)
    pas = 1 if a_fi > a_ini else -1
    for a in range(a_ini, a_fi + pas, pas):
        mou_servo(p, a)
        sleep(v)

# --- LEDS ON/OFF (cablejat SOURCE: càtode a GND, ànode→R→S) ---
def led_on(p):
    _init_once()
    if p in PORTS:
        c = PORTS[p]
        pwm(c, 4096, 0)   # FULL ON → S=HIGH (LED encès en 'source')

def led_off(p):
    _init_once()
    if p in PORTS:
        c = PORTS[p]
        pwm(c, 0, 4096)   # FULL OFF → S=LOW (LED apagat)

def led(p, v):  # interfície 0/255 pels alumnes
    led_on(p) if v >= 128 else led_off(p)

# === MOTORS DC — velocitat (sense invertir sentit), C0..C7 ===
# M1=(C0,C1), M2=(C2,C3), M3=(C4,C5), M4=(C6,C7)
# EN = PWM de velocitat ; PH = fase fixa HIGH/LOW
MOTOR_CH = {
    1: (0, 1),  # M1: EN=C0, PH=C1
    2: (2, 3),  # M2: EN=C2, PH=C3
    3: (4, 5),  # M3: EN=C4, PH=C5
    4: (6, 7),  # M4: EN=C6, PH=C7
}

# --- AFEGEIX AQUI LES CONSTANTS I L'ESTAT ---
MOTOR_PHASE_HIGH = False   # ja t'ha funcionat així
MOTOR_KICK_MS = 120        # durada de l’impuls d’arrencada (ms)
MOTOR_KICK_DUTY = 255      # intensitat del kickstart (0..255)
MOTOR_START_DUTY = 140     # duty mínim per assegurar arrencada
_motor_spinning = {1: False, 2: False, 3: False, 4: False}

def _digital(ch, high):
    # Helper per posar un canal del PCA a HIGH/LOW constant
    if high:
        pwm(ch, 4096, 0)   # HIGH
    else:
        pwm(ch, 0, 4096)   # LOW

def motor_vel(m, v):
    """
    Velocitat del motor m (1..4) amb v en 0..255, a 50 Hz.
    - Kickstart en passar de parat a >0.
    - Llindar d'arrencada (MOTOR_START_DUTY) només just al moment d'arrencar.
    - Direcció fixa (PHASE segons MOTOR_PHASE_HIGH).
    """
    _init_once()  # assegura 50 Hz
    if m not in MOTOR_CH:
        return
    en, ph = MOTOR_CH[m]
    _digital(ph, MOTOR_PHASE_HIGH)   # direcció fixa

    # Clamp
    if v <= 0:
        pwm(en, 0, 4096)            # aturat (coast)
        _motor_spinning[m] = False
        return
    if v > 255:
        v = 255

    # Si està parat, fem 'kick' i apliquem un mínim d'arrencada
    if not _motor_spinning[m]:
        if MOTOR_KICK_DUTY >= 255:
            pwm(en, 4096, 0)        # 100% (FULL ON)
        else:
            kick = (MOTOR_KICK_DUTY * 4095 + 127) // 255
            pwm(en, 0, kick)
        sleep(MOTOR_KICK_MS)

        v_eff = max(v, MOTOR_START_DUTY)
        duty = (v_eff * 4095 + 127) // 255
        pwm(en, 0, duty)
        _motor_spinning[m] = True
        return

    # Ja gira: apliquem el valor demanat tal qual
    duty = (v * 4095 + 127) // 255
    pwm(en, 0, duty)

def atura_motor(m):
    _init_once()
    if m not in MOTOR_CH:
        return
    en, ph = MOTOR_CH[m]
    pwm(en, 0, 4096)   # EN a LOW (coast)
    _motor_spinning[m] = False

def atura_tots():
    for m in (1, 2, 3, 4):
        atura_motor(m)

