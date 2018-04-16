import socket
import time
import binascii

import pycom
from network import LoRa
import machine

import config

# ------------------------------------------------------------------------------

# Enable LED heartbeat
pycom.heartbeat(True)

# Initialize GPIO
adc = machine.ADC()
temperature_pin = adc.channel(pin='G3')
relay_pin = machine.Pin('G10', mode=machine.Pin.OUT)

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, adr=True)

# Welcome message
print("[INFO] @ttncat thermostat example for the LoPy");
print("[INFO] DevEUI: %s" % (binascii.hexlify(lora.mac()).decode('ascii')))

# ------------------------------------------------------------------------------

# create an OTAA authentication parameters
app_eui = binascii.unhexlify(config.APP_EUI.replace(' ',''))
app_key = binascii.unhexlify(config.APP_KEY.replace(' ',''))

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
print('[INFO] Joining ', end='')
while not lora.has_joined():
    time.sleep(1)
    print('.', end='')
print()
print('[INFO] Joined!')

# create a LoRa socket
lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate (not needed if ADR enabled)
#lora_socket.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket non-blocking
lora_socket.setblocking(False)

# use port 12
lora_socket.bind(12)

# ------------------------------------------------------------------------------

def getTemperature():
    return 1100.0 * temperature_pin() / 4096 / 10 - 50

def getRelayStatus():
    return relay_pin()

def setRelayStatus(status):
    relay_pin(status)

def sendMessage(temperature, relay_status):
    lora_socket.send(bytes([int(temperature + 100), int(100 * (temperature - int(temperature))), ord('1') if 1 == relay_status else ord('0')]))

def receiveMessage():
    data = lora_socket.recv(10)
    print(data)
    if len(data) > 0:
        return data[0] - 48
    return -1

# ------------------------------------------------------------------------------

while True:

    try:
        temperature = getTemperature()
        relay_status = getRelayStatus()
        print('[INFO] Temperature: %5.1f | Relay: %s' % (temperature, 'ON' if 1 == relay_status else 'OFF'))
        sendMessage(temperature, relay_status)
        time.sleep(2.5)
        relay_status = receiveMessage()
        if -1 != relay_status:
            print('[INFO] Received: %d' % relay_status)
            setRelayStatus(relay_status)

    except:
        # Bad idea, but you can do it
        pass

    time.sleep(60)
