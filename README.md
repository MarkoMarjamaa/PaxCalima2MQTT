# PaxCalima2MQTT
MQTT gateway for Pax Calima fans for Python <=3.11

## Who is this for?  
- If you want a custom component working closer with HA, use https://github.com/eriknn/ha-pax_ble  
- If you want a component that is more detached from HA versioning and does not need constant updating, use this.  
  This sends HA MQTT discovery message to be registered to HA and then data is sent back and forth via MQTT. The most recent changes are with that discovery message but otherwise it's pretty stable interface. 
  I just updated my HA version from 2022.6 -> 2025.12 and there wasn't much updates this one needed, mainly changes in discovery. 

## Installing

Install my version of Pycalima ( works with 3.9 and has one new function )

```
#Get the latest to your work directory 
wget https://github.com/MarkoMarjamaa/pycalima/archive/master.zip
unzip master.zip
cd pycalima-master
```

Install it as python package
```
pip3 install . 
```

Bluez-5.47 compile might needs this:  
apt-get install libgtk-3-dev

Install right MQTT Paho version  
pip install paho-mqtt==1.6.1

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

Installing as service
```
sudo cp paxcalima2mqtt.service /etc/systemd/system
systemctl enable paxcalima2mqtt
systemctl restart paxcalima2mqtt
systemctl status paxcalima2mqtt
```

Bash script exits python script in case of error, restarts bluetooth adapter and starts script again. This seems to work with Rpi3&4 bluetooth. With Strix Halo I have removed the bluetooth restart, because there's also other devices attached. 


## Using component

Updating values works directly with MQTT and are also updatable in HA
```
      - service: mqtt.publish
        data:
          topic: PaxCalima2MQTT/projector_room_fan/heatdistributorsettings_temperaturelimit/set
          payload: '25'
          retain: false
```

This is how I currently use this. Set polling time first to 1min, change value, and wait until value changed. Then set polling time back to normal 60min. 
I have also an alert if the rpm value is older than 60min and if the polling value is 1min for a longer time, which means setting value was not successful. 

I have had this component now in Rpi4, Rpi5 and now in Strix Halo. In all of them, there was problems with bluetooth connection getting stuck and the problem seems to be in Pax Calima. 
I have this fan in projector room and the projector is not allowed to start until the fan is in high mode. I have input_boolean for low/high fan mode and this is action for high mode. 
Earlier I had polling time 1min, because that's what you need when you change the mode and have to check the results but that 1min was always on, so I added this parameter for polling. 
Now it seems it's not getting stuck anymore (=so much) because polling is 1/60. I also have smart plug with fan, so I can guickly restart it. 

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

