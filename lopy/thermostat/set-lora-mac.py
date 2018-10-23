# Utility to change the LoRa MAC of the device
# Do not use it with original PyCom boards!

import sys
import machine
import ubinascii

sys.exit()

try:
    import config
    mac = ubinascii.unhexlify(config.DEV_EUI.replace(' ',''))
except (ImportError, AttributeError):
    mac = bytearray(machine.unique_id())
    mac[3:3] = bytearray(b'\xFF\xFF')

fo = open("/flash/sys/lpwan.mac", "wb")
fo.write(mac)
fo.close()

print('LPWAN MAC:', ubinascii.hexlify(mac).decode('ascii'))
print('Reboot board to perform changes')
