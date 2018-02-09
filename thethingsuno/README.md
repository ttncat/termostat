# Termostat amb The Things Uno

Exemple de comunicació bidireccional sobre TTN amb un The Things Uno.

[![license](https://img.shields.io/github/license/ttncat/termostat.svg)](LICENSE)
[![twitter](https://img.shields.io/twitter/follow/ttncat.svg?style=social)](https://twitter.com/intent/follow?screen_name=ttncat)

## Hardware

#### Components

* The Things Uno amb mòdul RN2483 de Microchip (https://shop.thethingsnetwork.com/index.php/product/the-things-uno/)
* Sensor de temperatura analògic TMP35/LM35
* Mòdul de relé
* Botó
* Cables i/o protoboard per fer les connexions

#### Cablejat

TODO

## Firmware

El The Things Uno és un Arduino Leonardo amb un mòdul RN2483 de Microchip connectat al segons HardwareSerial (Serial1), per tant l'IDE d'Arduino té suport per defecte per aquesta placa seleccionant "Arduino Leonardo" al llistat de targes. Caldrà instal·lar la llibreria "The Things Network" des del 'Gestor de llibreries'. Aquest pas no és necessari si es fa servir PlatformIO.

El primer que cal fer és configurar les dades per connectar-nos a TTN. Duplica l'arxiu `credentials.sample.h` amb el nom `credentials.h` i edita'l introduint-hi les dades apropiades segons el *backend* the TTN.

Després compila i puja el codi al The Things Uno. Ho pots fer fent servir PlatformIO amb `pio run -t upload` o amb l'IDE d'Arduino.

Per defecte el codi envia un missatge amb la temperatura i l'estat del relé cada 60 segons i espera resposta per canviar l'estat del relé. També es pot forçar l'enviament prement el botó.

Tots els paràmetres de configuració (temps entre missatges, GPIOs dels diferents components...) estan al principi del codi principal (thermostat.ino).
