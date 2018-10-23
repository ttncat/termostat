import time
import machine

adc = machine.ADC()
temperature_pin = adc.channel(pin='G31')

def getTemperature():
    # LM35: 10mV/ºC
    return 1100.0 * temperature_pin() / 4096 / 10

while True:
    temperature = getTemperature()
    print('[INFO] Temperature: %5.1f' % temperature)
    time.sleep(10)
