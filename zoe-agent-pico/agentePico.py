# -*- coding: utf-8 -*-
#
# This file is part of Zoe Assistant
# Licensed under MIT license - see LICENSE file
#

from zoe import *

import smtplib
import json

#ttyACM0


if os.path.exists('ttyACM0') == True:
    print("conectando")
    import serial
    ser = serial.Serial('ttyACM0', 115200)
    serial_connected = 1
    time.sleep(3)


print("tras sleep")
#breakpoint()
@Agent('Pico')
class PicoAgent:

    @Intent("pico.led")
    def change_led(self, intent):
        breakpoint()

        estado = intent["led"]

        ser.write(bytes("l".encode('ascii')))

        

    @Intent("pico.get_led")
    def get_led(self, intent):
        breakpoint()
        ser.write(bytes("r".encode('ascii')))

        pico_data = ser.readline()
        pico_data = pico_data.decode("utf-8", "ignore")
        
        return {
                "intent": "tila.read",
                "chat": intent["chat"],
                "messsage": pico_data
            }

    
    @Intent("pico.get_temp")
    def get_temp(self,intent):

        ser.write(bytes("t".encode('ascii')))

        pico_data = ser.readline()
        pico_data = pico_data.decode("utf-8", "ignore")
        
        return {
                "intent": "tila.read",
                "chat": intent["chat"],
                "messsage": pico_data
            }