# -*- coding: utf-8 -*-
#
# This file is part of Zoe Assistant
# Licensed under MIT license - see LICENSE file
#

from zoe import *

import smtplib
import json
import pdb
import time

#ttyACM0


if os.path.exists('/dev/ttyACM0') == True:
    print("conectando")
    import serial
    ser = serial.Serial('/dev/ttyACM0', 115200)
    serial_connected = 1
    time.sleep(3)


print("tras sleep")
#breakpoint()
@Agent('Pico')
class PicoAgent:

    @Intent("pico.led")
    def change_led(self, intent):
        pdb.set_trace()

        estado = intent["led"]

        ser.write(b'l\n')

        

    @Intent("pico.get_led")
    def get_led(self, intent):
        pdb.set_trace()
        ser.write(b"r\n")

        pico_data = ser.readline()
        pico_data = pico_data.decode("utf-8", "ignore")
        
        return {
                "intent": "tila.read",
                "chat": intent["chat"],
                "message": pico_data
            }

    
    @Intent("pico.get_temp")
    def get_temp(self,intent):

        ser.write(b"t\n")

        pico_data = ser.readline()
        pico_data = pico_data.decode("utf-8", "ignore")
        
        return {
                "intent": "tila.read",
                "chat": intent["chat"],
                "message": pico_data
            }
