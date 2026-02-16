# PaxCalima2MQTT
MQTT gateway for Pax Calima fans for Python <=3.9

Install my version of Pycalima ( works with 3.9 and has one new function )

```
#Get the latest to your work directory 
wget https://github.com/MarkoMarjamaa/pycalima/archive/master.zip
unzip master.zip
cd pycalima-master
```

Install as python package
```
pip3 install . 
```

Set mac& pin etc in PaxCalima2MQTT.py
```
broker_address="homeautomation"
discovery_topic="homeassistant"
my_topic="PaxCalima2MQTT"
mac="XX:XX:XX:XX:XX:XX"
pin="XXXXXXXX"
device_name="Projector Room Fan"
device_id="projector_room_fan"
```

This is for only if you have older version of HA and it uses still Python 3.9. I will be porting this to 3.10 once I update HA later. 

Updating values works directly with MQTT and are also updatable in HA
```
      - service: mqtt.publish
        data:
          topic: PaxCalima2MQTT/projector_room_fan/heatdistributorsettings_temperaturelimit/set
          payload: '25'
          retain: false
```

The version I currently use. Set polling time first to 1min, change value, and wait until value changed. Then set polling time back to normal 60min. 
```
      - service: number.set_value
        data:
          value: 1
        target:
          entity_id: number.projector_room_fan_polling_min
      - service: number.set_value
        data:
          value: 22
        target:
          entity_id: number.projector_room_fan_heatdistributorsettings_temperaturelimit
      - wait_template: "{{ states('sensor.projector_room_fan_rpm') | int > 2000 }}"
        timeout: "00:10:00"
      - service: number.set_value
        data:
          value: 60
        target:
          entity_id: number.projector_room_fan_polling_min
```

Installing as service
```
sudo cp paxcalima2mqtt.service /etc/systemd/system
systemctl enable paxcalima2mqtt
systemctl restart paxcalima2mqtt
systemctl status paxcalima2mqtt
```
New version exits python script in case of error, restarts bluetooth adapter and start again. This seems to work with Rpi3&4 bluetooth. ( I only have Pax controlled with Rpi BT so it's ok to restart it ) 

Edit: Works also with Python3.11. 
Bluez-5.47 compile needs this: 
apt-get install libgtk-3-dev

and working paho-version: 
pip install paho-mqtt==1.6.1
