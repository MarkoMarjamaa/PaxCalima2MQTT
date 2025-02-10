#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time
from Calima import Calima

broker_address="homeautomation"
discovery_topic="homeassistant"
my_topic="PaxCalima2MQTT"
#port="/dev/grandview"
mac="XX:XX:XX:XX:XX:XX"
pin="XXXXXXXX"
device_name="Projector Room Fan"
device_id="projector_room_fan"

############
def on_message(client, userdata, message):
	value = str(message.payload.decode("utf-8"))
	#print(message.topic)
	#print(value)
	fan = None
	try:
		if message.topic in ( base_topic+"/heatdistributorsettings_temperaturelimit/set", base_topic+"/heatdistributorsettings_fanspeedbelow/set", base_topic+"/heatdistributorsettings_fanspeedabove/set"):
			fan = Calima(mac, pin)
			if (fan is None):
				print('Not connected')
			else:
				#print('Reading data')
				HeatDistributorSettings = fan.getHeatDistributor()
				HeatDistributorSettings_TemperatureLimit = HeatDistributorSettings.TemperatureLimit
				HeatDistributorSettings_FanSpeedBelow = HeatDistributorSettings.FanSpeedBelow
				HeatDistributorSettings_FanSpeedAbove = HeatDistributorSettings.FanSpeedAbove
				if message.topic == base_topic+"/heatdistributorsettings_temperaturelimit/set" :
					HeatDistributorSettings_TemperatureLimit = value
				if message.topic == base_topic+"/heatdistributorsettings_fanspeedbelow/set" :
					HeatDistributorSettings_FanSpeedBelow = value
				if message.topic == base_topic+"/heatdistributorsettings_fanspeedabove/set" :
					HeatDistributorSettings_FanSpeedAbove = value
				# Change value
				fan.setHeatDistributor(int(HeatDistributorSettings_TemperatureLimit), int(HeatDistributorSettings_FanSpeedBelow), int(HeatDistributorSettings_FanSpeedAbove))
				time.sleep(2)
				HeatDistributorSettings = fan.getHeatDistributor()
				client.publish(base_topic+"/heatdistributorsettings_temperaturelimit/state",HeatDistributorSettings.TemperatureLimit, retain=True)
				client.publish(base_topic+"/heatdistributorsettings_fanspeedbelow/state",HeatDistributorSettings.FanSpeedBelow, retain=True)
				client.publish(base_topic+"/heatdistributorsettings_fanspeedabove/state",HeatDistributorSettings.FanSpeedAbove, retain=True)
		elif message.topic in (base_topic+"/fanspeed_humidity/set",base_topic+"/fanspeed_light/set",base_topic+"/fanspeed_trickle/set"):
			fan = Calima(mac, pin)
			if (fan is None):
				print('Not connected')
			else:
				#print('Reading data')
				FanSpeeds = fan.getFanSpeedSettings()
				FanSpeeds_Humidity = FanSpeeds.Humidity
				FanSpeeds_Light = FanSpeeds.Light
				FanSpeeds_Trickle = FanSpeeds.Trickle
				if message.topic == base_topic+"/fanspeed_humidity/set" : 
					FanSpeeds_Humidity = value
				if message.topic == base_topic+"/fanspeed_light/set" : 
					FanSpeeds_Light = value
				if message.topic == base_topic+"/fanspeed_trickle/set" : 
					FanSpeeds_Trickle = value
				fan.setFanSpeedSettings(int(FanSpeeds_Humidity), int(FanSpeeds_Light), int(FanSpeeds_Trickle))
				time.sleep(2)
				FanSpeeds = fan.getFanSpeedSettings()
				client.publish(base_topic+"/fanspeed_humidity/state",FanSpeeds.Humidity, retain=True)
				client.publish(base_topic+"/fanspeed_light/state",FanSpeeds.Light, retain=True)
				client.publish(base_topic+"/fanspeed_trickle/state",FanSpeeds.Trickle, retain=True)

		elif message.topic == "STOP":
			print("WTF")
		else:
			print("WTF")

	except :
		print('Not connected, error')

	finally:
		if fan is not None:
			FanState = fan.getState()
			client.publish(base_topic+"/humidity/state",FanState.Humidity, retain=True)
			client.publish(base_topic+"/temperature/state",FanState.Temp, retain=True)
			client.publish(base_topic+"/light/state",FanState.Light, retain=True)
			client.publish(base_topic+"/rpm/state",FanState.RPM, retain=True)
			client.publish(base_topic+"/state/state",FanState.Mode, retain=True)

			client.publish(base_topic+"/mode/state",fan.getMode(), retain=True)

			fan.disconnect()

########################################

# Device base MQTT topic
base_topic = "PaxCalima2MQTT/" + device_id

#print("creating new instance")
client = mqtt.Client(my_topic+"_"+ device_id)
client.on_message=on_message #attach function to callback

#print("connecting to broker")
client.connect(broker_address)

client.subscribe(base_topic+"/+/set")

sensors = [
    ['humidity', 'Humidity', '%', None, 'humidity'],
    ['temperature', 'Temperature', '°C', None, 'temperature'],
    ['light', 'Light', 'lx', None, 'illuminance'],
    ['rpm', 'RPM', 'rpm', None, None],
    ['state', 'State', None, None, None],
    ['mode', 'Mode', None, None, None],
    ['fanspeed_humidity', 'Fanspeed Humidity', 'rpm', None, None],
    ['fanspeed_light', 'Fanspeed Light', 'rpm', None, None],
    ['fanspeed_trickle', 'Fanspeed Trickle', 'rpm', None, None],
    ['sensitivity_humidityon', 'Sensitivity Humidity On', None, None, None],
    ['sensitivity_humidity', 'Sensitivity Humidity', '%', None, 'humidity'],
    ['sensitivity_lighton', 'Sensitivity Light On', None, None, None],
    ['sensitivity_light', 'Sensitivity Light', 'lx', None, 'illuminance'],
    ['lightsensorsettings_delayedstart', 'LightSensorSettings DelayedStart', 's', None, None],
    ['lightsensorsettings_runningtime', 'LightSensorSettings Runningtime', 's', None, None],
    ['heatdistributorsettings_temperaturelimit', 'HeatDistributorSettings TemperatureLimit', '°C', None, 'temperature'],
    ['heatdistributorsettings_fanspeedbelow', 'HeatDistributorSettings FanSpeedBelow', 'rpm', None, None],
    ['heatdistributorsettings_fanspeedabove', 'HeatDistributorSettings FanSpeedAbove', 'rpm', None, None],
    ['boostmode', 'BoostMode', None, None, None],
    ['boostmodespeed', 'BoostMode Speed', 'rpm', None, None],
    ['boostmodesec', 'BoostMode Time', 's', None, None],
    ['silenthours_on', 'SilentHours On', None, None, None],
    ['silenthours_startinghour', 'SilentHours StartingHour', 'H', None, None],
    ['silenthours_startingminute', 'SilentHours StartingMinute', 'Min', None, None],
    ['silenthours_endinghour', 'SilentHours EndingHour', 'H', None, None],
    ['silenthours_endingminute', 'SilentHours EndingMinute', 'Min', None, None],
    ['trickledays_weekdays', 'TrickleDays Weekdays', None, None, None],
    ['trickledays_weekends', 'TrickleDays Weekends', None, None, None],
    ['automatic_cycles', 'Automatic Cycles', None, None, None]
]

# Define the device data (same for all sensors)
device_data = {
    "identifiers": ["PaxCalima2MQTT_"+mac],
    "name": device_name,
    "model": "Pax Calima",
    "manufacturer": "Pax"
}

# Generate MQTT discovery messages for each sensor
for sensor in sensors:
    sensor_id, sensor_name, unit_of_measurement, _, device_class = sensor
    
    # Construct the payload for each sensor
    sensor_payload = {
        "name": device_name + " " + sensor_name,
        "state_topic": f"{base_topic}/{sensor_id}/state",
        "unique_id": f"{device_id}_{sensor_id}",
        "device": device_data  # Use the same device for all sensors
    }

    if unit_of_measurement is not None:
        sensor_payload["unit_of_measurement"] = unit_of_measurement
    if device_class is not None:
        sensor_payload["device_class"] = device_class
    
    # Convert the dictionary to a JSON string
    discovery_message = json.dumps(sensor_payload, indent=4)
    
    # Print the discovery message
    #print(f"homeassistant/sensor/{sensor_id}/config")
    #print(discovery_message)
    client.publish(discovery_topic+"/sensor/"+sensor_id+"/config",discovery_message, retain=True)
    #print()
	
#    print (json.dumps(config_data))

try:
	# Publish data
	fan = Calima(mac, pin)

	if (fan is None):
		print('Not connected')
	else:
		#print('Reading data')
		FanState = fan.getState()

		if (FanState is None):
			print('Could not read data')
		else: 
			FanSpeeds = fan.getFanSpeedSettings()
			Sensitivity = fan.getSensorsSensitivity()
			LightSensorSettings = fan.getLightSensorSettings()
			HeatDistributorSettings = fan.getHeatDistributor()
			BoostMode = fan.getBoostMode()
			SilentHours = fan.getSilentHours()
			TrickleDays = fan.getTrickleDays()
			
			client.publish(base_topic+"/humidity/state",FanState.Humidity, retain=True)
			client.publish(base_topic+"/temperature/state",FanState.Temp, retain=True)
			client.publish(base_topic+"/light/state",FanState.Light, retain=True)
			client.publish(base_topic+"/rpm/state",FanState.RPM, retain=True)
			client.publish(base_topic+"/state/state",FanState.Mode, retain=True)

			client.publish(base_topic+"/mode/state",fan.getMode(), retain=True)

			client.publish(base_topic+"/fanspeed_humidity/state",FanSpeeds.Humidity, retain=True)
			client.publish(base_topic+"/fanspeed_light/state",FanSpeeds.Light, retain=True)
			client.publish(base_topic+"/fanspeed_trickle/state",FanSpeeds.Trickle, retain=True)

			client.publish(base_topic+"/sensitivity_humidityon/state",Sensitivity.HumidityOn, retain=True)
			client.publish(base_topic+"/sensitivity_humidity/state",Sensitivity.Humidity, retain=True)
			client.publish(base_topic+"/sensitivity_lighton/state",Sensitivity.LightOn, retain=True)
			client.publish(base_topic+"/sensitivity_light/state",Sensitivity.Light, retain=True)

			client.publish(base_topic+"/lightsensorsettings_delayedstart/state",LightSensorSettings.DelayedStart, retain=True)
			client.publish(base_topic+"/lightsensorsettings_runningtime/state",LightSensorSettings.RunningTime, retain=True)

			client.publish(base_topic+"/heatdistributorsettings_temperaturelimit/state",HeatDistributorSettings.TemperatureLimit, retain=True)
			client.publish(base_topic+"/heatdistributorsettings_fanspeedbelow/state",HeatDistributorSettings.FanSpeedBelow, retain=True)
			client.publish(base_topic+"/heatdistributorsettings_fanspeedabove/state",HeatDistributorSettings.FanSpeedAbove, retain=True)

			client.publish(base_topic+"/boostmode/state",BoostMode.OnOff, retain=True)
			client.publish(base_topic+"/boostmodespeed/state",BoostMode.Speed, retain=True)
			client.publish(base_topic+"/boostmodesec/state",BoostMode.Seconds, retain=True)

			client.publish(base_topic+"/silenthours_on/state",SilentHours.On, retain=True)
			client.publish(base_topic+"/silenthours_startinghour/state",SilentHours.StartingHour, retain=True)
			client.publish(base_topic+"/silenthours_startingminute/state",SilentHours.StartingMinute, retain=True)
			client.publish(base_topic+"/silenthours_endinghour/state",SilentHours.EndingHour, retain=True)
			client.publish(base_topic+"/silenthours_endingminute/state",SilentHours.EndingMinute, retain=True)

			client.publish(base_topic+"/trickledays_weekdays/state",TrickleDays.Weekdays, retain=True)
			client.publish(base_topic+"/trickledays_weekends/state",TrickleDays.Weekends, retain=True)

			client.publish(base_topic+"/automatic_cycles/state",fan.getAutomaticCycles(), retain=True)

except :
	print('Not connected, error')

finally:
	if fan is not None:
		#print('Disconnecting')
		fan.disconnect()

# Start on_message loop
client.loop_start()

# Loop to send fan speed every 5 minutes
try:
	while True:
        
		# Wait for 5 minutes (300 seconds)
		time.sleep(60)

		try:
			# Publish data
			fan = Calima(mac, pin)

			if (fan is None):
				print('Not connected')
			else:
				#print('Reading data')
				FanState = fan.getState()

				if (FanState is None):
					print('Could not read data')
				else: 
					#print(FanState.RPM)
					client.publish(base_topic+"/humidity/state",FanState.Humidity, retain=True)
					client.publish(base_topic+"/temperature/state",FanState.Temp, retain=True)
					client.publish(base_topic+"/light/state",FanState.Light, retain=True)
					client.publish(base_topic+"/rpm/state",FanState.RPM, retain=True)
					client.publish(base_topic+"/state/state",FanState.Mode, retain=True)

					client.publish(base_topic+"/mode/state",fan.getMode(), retain=True)

		except :
			print('Not connected, error')

		finally:
			if fan is not None:
				#print('Disconnecting')
				fan.disconnect()
			
		
except KeyboardInterrupt:
	print("Program interrupted by user.")
finally:
	# Stop the MQTT loop and disconnect
	client.loop_stop()
	client.disconnect()
