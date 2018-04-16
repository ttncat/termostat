# Termostat amb PyCom LoPy

Exemple de comunicació bidireccional sobre TTN amb un PyCom LoPy.

[![license](https://img.shields.io/github/license/ttncat/termostat.svg)](LICENSE)
[![twitter](https://img.shields.io/twitter/follow/ttncat.svg?style=social)](https://twitter.com/intent/follow?screen_name=ttncat)

## Hardware

#### Components

* PyCom LoPy  (https://pycom.io/product/lopy/)
* Sensor de temperatura analògic TMP35/LM35
* Mòdul de relé
* Botó
* Cables i/o protoboard per fer les connexions

#### Cablejat

|Expansion board|TMP35/LM35|Relay|
|---|---|---|
|3V3|VCC (pin 1)||
|G3|OUT (pin 2)||
|GND|GND (pin 3)|GND|
|G10||IN|
|VIN||VCC|

## Firmware

Recommended upload tool is PyMakr plugin for atom (https://docs.pycom.io/chapter/pymakr/installation/atom.html)
