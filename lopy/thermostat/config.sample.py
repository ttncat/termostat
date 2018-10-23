# Configure here the credentials for your device
# Remember to run the script first to get the DevEUI so you can
# create the device in the TTN console

from network import LoRa

ACTIVATION = LoRa.OTAA
#ACTIVATION = LoRa.ABP

# OTAA
APP_EUI = ''
APP_KEY = ''

# ABP
DEV_ADDR = ''
NWK_SKEY = ''
APP_SKEY = ''
