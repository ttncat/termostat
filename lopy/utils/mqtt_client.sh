# Bash mosquitto client for TTN
# Uses mqsquitto_sub and jq:
#
# sudo apt install mosquitto-clients jq
#

USER="test"
PASS="ttn-account-v2.ALT..."

mosquitto_sub -h eu.thethings.network -u $USER -P $PASS -t "+/devices/+/up" | jq --unbuffered
