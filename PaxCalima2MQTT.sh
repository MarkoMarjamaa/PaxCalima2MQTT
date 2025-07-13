#! /bin/bash
echo "Scrip starting"
/usr/bin/sudo /bin/hciconfig hci1 down
/bin/sleep 1
/usr/bin/sudo /bin/hciconfig hci1 up
/bin/sleep 1
/usr/bin/python3 -u /home/pi/PaxCalima2MQTT/PaxCalima2MQTT.py
