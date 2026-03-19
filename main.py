from microbit import *
import iluminacio
import porta

while True:
    if button_a.is_pressed() and button_b.is_pressed():
        break

    iluminacio.llum_exterior()
    iluminacio.llum_interior()
    porta.funcionament_porta( )

    sleep (100)
