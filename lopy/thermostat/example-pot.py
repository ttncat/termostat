import time
import machine
import pycom

# Disable heartbeat
pycom.heartbeat(False)

# Initialize GPIO
adc = machine.ADC()
pot = adc.channel(pin='G3')

while True:
    value = int(255 * pot() / 4096) & 0xFF;
    pycom.rgbled(value << 16)
    time.sleep(0.1)
