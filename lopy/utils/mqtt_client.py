# Simple Python client to show node activity from ttn MQTT brooker with credentials
# Author: R.Schimmel
# www.schimmel-bisolutions.nl
#
# pip install paho-mqtt

import sys
import json
from pygments import highlight, lexers, formatters
import paho.mqtt.client as mqtt

# configuration
app_id = "test"
access_key = "ttn-account-v2.ALT....."

# callback functions
def on_connect(client, userdata, flags, rc):
    print("Subscribing...")
    # subscribe for all devices of user
    client.subscribe('+/devices/+/up')

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

def on_message(client, userdata, msg):
    formatted_json = json.dumps(json.loads(msg.payload), indent=4)
    colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.username_pw_set(app_id, access_key)

print("Connecting...")
client.connect("eu.thethings.network", 1883, 60)

# and listen to server
client.loop_forever()
