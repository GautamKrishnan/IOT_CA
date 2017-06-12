from I2C_device import *
from paho.mqtt.client import Client
import RPi.GPIO as GPIO
import sys
import time
import datetime

class Relay:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pinList = [22,23,24,25]

    def switch(self, lamp, state):
        pin = self.pinList[lamp]
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, (GPIO.HIGH if state == 0 else GPIO.LOW))

    def getTimeOn(self, moistureValue):
        if ( int(moistureValue) < 75 ):
            onTime = 5
        elif ( int(moistureValue) > 75 and int(moistureValue) < 150 ):
            onTime = 10
        else:
            onTime = 15
        return onTime

class Board:
    def __init__(self, addr=0x48, port=1):
        self.device = I2C_device(addr, port)
 
    def control(self):
        self.device.read_data(0x00)
        return self.device.read_data(0x00)
 
    def light(self):
        self.device.read_data(0x01)
        return self.device.read_data(0x01)
 
    def temperature(self):
        self.device.read_data(0x02)
        return self.device.read_data(0x02)
 
    def moisture(self):
        self.device.read_data(0x03)
        return self.device.read_data(0x03)
 
    def output(self, val):
        self.device.write_cmd_arg(0x40, val)
        

def main():
    relay = Relay()
    board = Board()
  
    print ' Program Started...  '
    print ' Switching on Sensor 1 '
    relay.switch(int(0), int(1))
    print ' Getting data from Sensor 1 '
    time.sleep(30)
    print "%s: moisture:%d" % (time.asctime(),
                               board.moisture())
    moistureValue1 = int(board.moisture())
    print ' Switching off Sensor 1 '
    relay.switch(int(0), int(0))

    time.sleep(2)

    onTimeSen1 = relay.getTimeOn(moistureValue1);

    #MQTT Publisher
    client = Client(client_id="my_id_pub", userdata="user2")
    client.connect("172.17.249.19")
    message = str("The senosor detected moisture level is %d and the corresponding time is %d" % (moistureValue1,onTimeSen1))
    topic = "Moisture"
    client.publish(topic, message)
    
    print ' Relay 3 activated for %d - Implies Flow is on ' % (onTimeSen1)
    relay.switch(int(2), int(1))
    time.sleep(onTimeSen1)
    relay.switch(int(2), int(0))
    print ' Relay 3 is deactivated - Implies Flow is off '
       
if __name__ == "__main__":
    main()
