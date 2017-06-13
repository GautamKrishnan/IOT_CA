import time
import sys
import os
from paho.mqtt.client import Client
 
def on_message(c, userdata, mesg):
    print "Moisture Data: %s %s" % (mesg.topic, mesg.payload)
    stringList = (mesg.payload).split(',')
    string = "sudo python /home/pi/Lcd.py '%s %s'"%(stringList[0], stringList[1])
    os.system(string)
 
client = Client(client_id="my_id", userdata="user1")
client.connect("172.17.249.19")
client.on_message = on_message
client.subscribe("Moisture")
while True:
    client.loop()
    time.sleep(1)
