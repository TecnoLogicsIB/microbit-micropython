from microbit import *
import radio
import music

radio.config(group=67)
radio.on()

ultim_usuari_sos = ""

#music.set_volume(255)
# music.stop()

while True:
    msg = radio.receive()
    
    # rep SOS
    if msg and msg.startswith("SOS:"):
        ultim_usuari_sos = msg[4:]
        display.scroll("SOS U" + ultim_usuari_sos)
    
    # professor desbloqueja amb boto A
    if button_a.was_pressed() and ultim_usuari_sos != "":
        radio.send("UNLOCK:" + ultim_usuari_sos)
        display.scroll("OK")
        
    sleep(50)