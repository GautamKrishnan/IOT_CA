import time
from paho.mqtt.client import Client
 
def on_message(c, userdata, mesg):
    print "%s Data: %s" % (mesg.topic, mesg.payload)
 
client = Client(client_id="my_id", userdata="user1")
client.connect("172.17.249.19")
client.on_message = on_message
client.subscribe("Moisture")
while True:
    client.loop()
    time.sleep(1)
