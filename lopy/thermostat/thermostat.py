import socket
import time
import ubinascii
import struct

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
lora = LoRa(mode=LoRa.LORAWAN, adr=True, region=LoRa.EU868)

# Welcome message
print("[INFO] @ttncat thermostat example for the LoPy");
print("[INFO] DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))

# ------------------------------------------------------------------------------

# join a network using OTAA (Over the Air Activation)
if (config.ACTIVATION == LoRa.OTAA):
    app_eui = ubinascii.unhexlify(config.APP_EUI.replace(' ',''))
    app_key = ubinascii.unhexlify(config.APP_KEY.replace(' ',''))
    auth = (app_eui, app_key)

# join a network using ABP (Activation by Personalisation)
else:
    dev_addr = struct.unpack(">l", ubinascii.unhexlify(config.DEV_ADDR.replace(' ','')))[0]
    nwk_skey = ubinascii.unhexlify(config.NWK_SKEY.replace(' ',''))
    app_skey = ubinascii.unhexlify(config.APP_SKEY.replace(' ',''))
    auth = (dev_addr, nwk_skey, app_skey)

# join
lora.join(activation=config.ACTIVATION, auth=auth, timeout=0)

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
    t = 1100.0 * temperature_pin() / 4096 / 10 - 50
    t = 0 if t<0 else 40 if t>40 else t
    return t

def getRelayStatus():
    return relay_pin()

def setRelayStatus(status):
    relay_pin(status)

def sendMessage(temperature, relay_status):
    lora_socket.send(bytes([int(temperature + 100), int(100 * (temperature - int(temperature))), ord('1') if 1 == relay_status else ord('0')]))

def receiveMessage():
    data = lora_socket.recv(10)
    if len(data) > 0:
        return data[0] - 48
    return -1

# ------------------------------------------------------------------------------

while True:

    temperature = getTemperature()
    relay_status = getRelayStatus()
    print('[INFO] Temperature: %5.1f | Relay: %s' % (temperature, 'ON' if 1 == relay_status else 'OFF'))
    sendMessage(temperature, relay_status)

    time.sleep(2.5)
    relay_status = receiveMessage()
    if -1 != relay_status:
        print('[INFO] Received: %d' % relay_status)
        setRelayStatus(relay_status)

    time.sleep(60)
