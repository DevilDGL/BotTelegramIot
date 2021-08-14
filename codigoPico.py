import uselect
import sys
import machine
from machine import Pin
import utime
import _thread

# Built-in temperature sensor 
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
# Built-in led
led = Pin(15, Pin.OUT)

def send_temperature():
   while True:
      reading = sensor_temp.read_u16() * conversion_factor
      temperature = 27 - (reading - 0.706)/0.001721
      return temperature

def getConfig():
   # Set up an input polling object
   spoll = uselect.poll()
   # Register the polling object to the Standard Input file
   spoll.register(sys.stdin, uselect.POLLIN)

   # Read 1 byte from stdin
   sch = sys.stdin.readline() if spoll.poll(0) else None

   spoll.unregister(sys.stdin)
   return sch


if __name__ == '__main__':
   while True:
      new_ch = getConfig()

      if new_ch in [None,'']:
         continue
      elif new_ch == 'l\n':
         led.toggle()
      elif new_ch == 'r\n':
         print(led.value())
      elif new_ch == 't\n':
         print(send_temperature())
      utime.sleep(1)
