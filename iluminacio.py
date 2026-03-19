from microbit import *
llindar_llum = 400
estat_led = "apagat"
comptador = 0

def llum_exterior():
    global estat_led, comptador
    
    presencia = pin15.read_digital()
    llum = pin1.read_analog()
    
    if presencia and llum < llindar_llum:
        pin14.write_digital(1)
        estat_led= "ences"
        
    elif not presencia and estat_led == "ences":
        comptador +=1
        if comptador == 20:
            #pin14.write_digital(0)
            estat_led = "apagat"
            comptador = 0
            
    else:  
        pin14.write_digital(0)
    
    print (comptador,'|', estat_led)

def llum_interior():
    ocupacio = pin8. read_digital()
    llum = pin1.read_analog()    
    if ocupacio and llum < llindar_llum:
        #pwm = int((llindar_llum - llum) * 1023 / llindar_llum)
        pin12.write_digital(1)
        pin13.write_digital(1)
    else:
        #pwm = 0
        pin12.write_digital(0)
        pin13.write_digital(0)
    #pin12.write_analog (pwm)
    #pin13.write_analog (pwm)        