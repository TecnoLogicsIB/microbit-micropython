from microbit import *
from robotbit import mou_servo_suau
import music
import radio

porta_oberta, porta_tancada = 30, 120
pin_correcte = ['A', 'A', 'B', 'A']
pin_introduit = []
caracters = 4     # num de caràcters a la llista que conté el pin correcte
intents = 0
estat_porta = 'tancada'
incidence = False

radio.config(group=67)
radio.on
mou_servo_suau (8, porta_tancada)

def introdueix_pin():
    if button_a.was_pressed():
        pin_introduit.append('A')
        display.set_pixel (2,2,9)
        music.pitch (1200, 20)
        display.set_pixel (2,2,0)
        print(pin_introduit)
    if button_b.was_pressed():
        pin_introduit.append('B')
        display.set_pixel (2,2,9)
        music.pitch (1200, 20)
        display.set_pixel (2,2,0)
        print(pin_introduit)

def comprova_pin():
    global pin_introduit, intents, estat_porta
    if len (pin_introduit) == caracters:
        if pin_introduit == pin_correcte:      
            display.show (Image.YES)
            music.play (music.POWER_UP)
            mou_servo_suau (8, porta_oberta, 20)     # obre porta
            estat_porta = 'oberta'
            display.clear()
            intents = 0    # reinici
        else:
            display.show (Image.NO)
            music.play (music.FUNERAL)
            display.clear()
            intents +=1
        pin_introduit = []    # reinici

def tanca_porta():
    if microphone.current_event() == SoundEvent.LOUD:
        mou_servo_suau (8, porta_tancada, 20)    # tanca porta
        estat_porta = 'tancada'

def bloqueja():
    global incidence
    display.show(Image.SKULL)
    music.pitch (1200, 200)
    display.clear()
    music.pitch (820, 200)
    if not incidence:
        radio.on()
        radio.send("SOS:" + str(5))
        incidence =True

def desbloqueja():
    global intents, incidence
    msg = radio.receive()
    if msg and msg == "UNLOCK" + str(5):
        # reinicia el sistema:
        radio.off()
        intents = 0
        incidence = False
        music.stop()
        display.clear()
    
def funcionament_porta():
    if intents <3:
        introdueix_pin()
        comprova_pin()
        if estat_porta == 'oberta':
            tanca_porta()
    else:
        bloqueja()
        desbloqueja()

