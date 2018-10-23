import ubinascii
from network import LoRa

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# Welcome message
print("[INFO] DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))
