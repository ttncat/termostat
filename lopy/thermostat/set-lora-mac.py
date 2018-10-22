# Utility to change the LoRa MAC of the device
# based on the WiFi MAC
# Do not use it with original PyCom boards!

import machine
import ubinascii

mac = bytearray(machine.unique_id())
mac[3:3] = bytearray(b'\xFF\xFF')

fo = open("/flash/sys/lpwan.mac", "wb")
fo.write(mac)
fo.close()

print('LPWAN MAC:', ubinascii.hexlify(mac).decode('ascii'))
print('Reboot board to set MAC')
