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

Updating values works directly with MQTT
```
      - service: mqtt.publish
        data:
          topic: PaxCalima2MQTT/projector_room_fan/heatdistributorsettings_temperaturelimit/set
          payload: '25'
          retain: false
```

Installing as service
```
sudo cp paxcalima2mqtt.service /etc/systemd/system
systemctl enable paxcalima2mqtt
systemctl restart paxcalima2mqtt
systemctl status paxcalima2mqtt
```
