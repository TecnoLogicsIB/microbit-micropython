# control de servos amb el PCA9685 de la placa robot:bit
# desfasada per el mòdul robotbit, que permet controlar també LEDs i motors CC

from microbit import i2c, sleep  # Importem comunicació I2C i funció de pausa

ADR = 0x40  # Adreça del xip PCA9685 per controlar servos
PORTS = {   # Diccionari que associa ports S1–S8 als canals 8–15 del xip
    1: 8, 2: 9, 3: 10, 4: 11,
    5: 12, 6: 13, 7: 14, 8: 15
}

ini = False      # Indica si ja hem inicialitzat la freqüència PWM
angles = {}      # Guarda l’últim angle assignat a cada port

# Escriu un valor a un registre del xip
def reg(r, v):
    i2c.write(ADR, bytes([r, v]))

# Configura la freqüència PWM (per a servos ha de ser 50 Hz)
def freq(f):
    p = int(25000000 / (4096 * f) - 1)  # Càlcul del prescaler per aconseguir la freq. desitjada
    reg(0x00, 0x10)   # Posem el xip en mode "sleep" per poder canviar la freqüència
    reg(0xFE, p)      # Escrivim el valor de prescaler
    reg(0x00, 0xA1)   # Tornem a "wake up" amb auto-increment activat

# Envia un senyal PWM al canal indicat amb valors "on" i "off"
def pwm(c, on, off):
    b = 0x06 + 4 * c                # Registre base del canal c
    i2c.write(ADR, bytes([b, on & 255]))       # Byte baix de "on"
    i2c.write(ADR, bytes([b+1, on >> 8]))      # Byte alt de "on"
    i2c.write(ADR, bytes([b+2, off & 255]))    # Byte baix de "off"
    i2c.write(ADR, bytes([b+3, off >> 8]))     # Byte alt de "off"

# Converteix un angle (0–180) en una durada de pols i envia el senyal
def angle(c, a):
    p = int(500 + a / 180 * 2000)           # Durada del pols en microsegons (entre 500 i 2500 us)
    v = int(p * 4096 / 20000)               # Converteix microsegons a valor de 12 bits
    pwm(c, 0, v)                             # Envia PWM amb "on = 0" i "off = v"

# Mou el servo del port p a l’angle a (de cop, sense animació)
def mou_servo(p, a):
    global ini
    if not ini:                       # Si encara no hem inicialitzat, ho fem
        freq(50)                     # Freqüència estàndard de servos = 50 Hz
        ini = True
    if p in PORTS:                # Comprovem que el port sigui vàlid (entre 1 i 8)
        angle(PORTS[p], a)    # Convertim port a canal i enviem l’angle
        angles[p] = a             # Guardem l’últim angle assignat a aquest port

# Mou el servo suaument fins a l’angle final, pas a pas
def mou_servo_suau(p, a_fi, v=10):
    if p not in PORTS:                              # Si el port no és vàlid, sortim
        return
    a_ini = angles.get(p, a_fi)                   # Recuperem l’angle anterior, o usem el final si no en tenim
    pas = 1 if a_fi > a_ini else -1              # Determinem si hem d’incrementar o decrementar
    for a in range(a_ini, a_fi + pas, pas):  # Recorrem els angles un a un
        mou_servo(p, a)                              # Movem el servo a l’angle actual
        sleep(v)                                           # Esperem uns mil·lisegons per suavitzar el moviment

