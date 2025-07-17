from microbit import *  

llindar_llum = 400      

def llum_entrada( ): 
    presencia = pin14.read_digital( )
    llum = pin2.read_analog( )             # llegeix el senyal analògic (entre 0 i 1023) pel pin 2
    if presencia and llum < llindar_llum:
        pin15.write_digital (1)                                        # mostra la lectura per la consola
    else:
        pin15.write_digital (0) 

while True:
    llum_entrada( )
    sleep (100)     
