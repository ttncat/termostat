/*

The Things Uno Thermostat

Copyright (C) 2018
Xose Pérez <xose dot perez at gmail dot com>
for The Things Network Catalunya (http://thethingsnetwork.cat)

Requires TheThingsUno library (https://github.com/TheThingsNetwork/arduino-device-lib)

---------------------------------------------------------------------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/

#include <TheThingsNetwork.h>
#include <TheThingsMessage.h>
#include "credentials.h"

#define APP_PORT        12      // Application port
#define SEND_EVERY      60000   // Send message very 60 seconds
#define REQUIRE_ACK     0       // Require ACK
#define RETRIES         3       // Number of retries if message fails
#define RETRY_AFTER     5000    // Wait these many ms before retrying

#define TMP35_GPIO      A1      // Analog GPIO for the TMP35
#define BUTTON_GPIO     4       // Digital GPIO for the button
#define RELAY_GPIO      5       // Digital GPIO for the relay
#define RELAY_INVERSE   1       // Relay uses inverse logic

TheThingsNetwork ttn(Serial1, Serial, TTN_FP_EU868);
devicedata_t data = api_DeviceData_init_default;
bool relay_status = false;      // Default status OFF

void ttn_join() {

    // Show device status
    ttn.showStatus();

    // Join network
    #if LORA_MODE == LORA_MODE_OTAA
        bool connected = ttn.join(appEui, appKey);
    #else
        bool connected = ttn.personalize(devAddr, nwkSKey, appSKey);
    #endif

    if (connected) {
        Serial.println("[INFO] Network joined!");
    } else {
        Serial.println("[ERROR] Something went wrong, could not join network");
        while (1) {}
    }

    ttn.onMessage(ttn_receive);

}

void ttn_send() {

    // Get temperature
    unsigned long reading = analogRead(TMP35_GPIO);
    float millivolts = (reading / 1023.0) * 3300;       // 10 bits ADC, 3.3V reference
    float celsius = millivolts / 10;                    // 10mV/C

    // Console info
    Serial.print("[INFO] Sending message, payload: ");
    Serial.print(celsius);
    Serial.print("C, relay ");
    Serial.println(relay_status ? "ON" : "OFF");

    // Encoding message
    // First byte will have the int degrees plus 100
    // Second byte will have the hundreths of degree
    // Third byte will be the relay status in ASCII
    // So 18.75, relay ON will be {0x76, 0x4B, 0x31}
    //     -5.2, relay OFF will be {0x5F, 0x14, 0x30}
    //
    // Use this decoder function in the TTN console:
    //
    // function Decoder(bytes, port) {
    //    var decoded = {};
    //    if (12 == port) {
    //       var value = (bytes[0] - 100) + (bytes[1] / 100);
    //       decoded.temperature = value;
    //       decoded.relay = (0x31 == bytes[2]);
    //    }
    //    return decoded;
    // }
    //
    unsigned char buffer[3];
    buffer[0] = int(celsius + 100) & 0xFF;
    buffer[1] = int(100 * (celsius - int(celsius))) & 0xFF;
    buffer[2] = relay_status ? '1' : '0';

    // Send message
    unsigned char tries = 0;
    while (true) {

        ttn_response_t response = ttn.sendBytes(buffer, sizeof(buffer), APP_PORT);

        if (response == TTN_SUCCESSFUL_TRANSMISSION) {
            Serial.println("[INFO] Message sent correctly!");
            return;
        }

        tries++;
        if (RETRIES == tries) break;

        Serial.println("[ERROR] Error, trying again...");
        delay(RETRY_AFTER);

    }

    Serial.println("[ERROR] Error sending message :(");

}

void ttn_receive(const uint8_t *payload, size_t length, port_t port) {
    if (APP_PORT == port) {
        bool relay = ('1' == payload[0]);
        Serial.print("[INFO] Turning relay ");
        Serial.println(relay ? "ON" : "OFF");
        digitalWrite(RELAY_GPIO, RELAY_INVERSE ? !relay : relay);
        relay_status = relay;
    }
}

void setup() {

    // Configure ports
    Serial1.begin(57600);
    Serial.begin(115200);

    // Wait a maximum of 10s for Serial Monitor
    while (!Serial && millis() < 10000);
    Serial.println("[INFO] @ttncat thermostat");

    // Setup button, relay & sensor
    pinMode(BUTTON_GPIO, INPUT_PULLUP);
    pinMode(RELAY_GPIO, OUTPUT);
    pinMode(TMP35_GPIO, INPUT);
    digitalWrite(RELAY_GPIO, RELAY_INVERSE ? !relay_status : relay_status);

    // Join TTN network
    ttn_join();

}

void loop() {

    // Automatic send every SEND_EVERY millis
    static unsigned long last = 0;
    if (millis() - last > SEND_EVERY) {
        last = millis();
        ttn_send();
    }

    // Manual send using the button
    static bool button_status = true; // not-pressed status (button has pull-up)
    if (digitalRead(BUTTON_GPIO) != button_status) {

        delay(50);  // debounce

        if (digitalRead(BUTTON_GPIO) != button_status) {

            // If status was true now it's false so button pressed
            if (button_status) {
                last = millis();
                ttn_send();
            }

            // Update status cache
            button_status = !button_status;

        }

    }

}
