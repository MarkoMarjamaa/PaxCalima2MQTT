#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time
from pycalima.Calima import Calima
import threading

broker_address="homeautomation"
discovery_topic="homeassistant"
my_topic="PaxCalima2MQTT"
mac="XX:XX:XX:XX:XX:XX"
pin="XXXXXXXX"
device_name="Projector Room Fan"
device_id="projector_room_fan"

bluetooth_lock = threading.Lock()

def refresh_all(fan, client):
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



############
def on_message(client, userdata, message):
	value = str(message.payload.decode("utf-8"))
	fan = None
	with bluetooth_lock: 
		try:
			if message.topic in ( base_topic+"/heatdistributorsettings_temperaturelimit/set", base_topic+"/heatdistributorsettings_fanspeedbelow/set", base_topic+"/heatdistributorsettings_fanspeedabove/set"):
				fan = Calima(mac, pin)

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

			elif message.topic in (base_topic+"/mode/set"):
				fan = Calima(mac, pin)

				#print('Reading data')
				if value == "MultiMode" : fan.setMode(int(0))
				if value == "DraftShutterMode" : fan.setMode(int(1))
				if value == "WallSwitchExtendedRuntimeMode" : fan.setMode(int(2))
				if value == "WallSwitchNoExtendedRuntimeMode" : fan.setMode(int(3))
				if value == "HeatDistributionMode" : fan.setMode(int(4))

			elif message.topic in (base_topic+"/fanspeed_humidity/set",base_topic+"/fanspeed_light/set",base_topic+"/fanspeed_trickle/set"):
				fan = Calima(mac, pin)

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

			elif message.topic in (base_topic+"/sensitivity_humidity/set",base_topic+"/sensitivity_light/set"):
				fan = Calima(mac, pin)

				#print('Reading data')
				Sensitivity = fan.getSensorsSensitivity()
				Sensitivity_Humidity = Sensitivity.Humidity
				Sensitivity_Light = Sensitivity.Light
				if message.topic == base_topic+"/sensitivity_humidity/set" : 
					Sensitivity_Humidity = value
				if message.topic == base_topic+"/sensitivity_light/set" : 
					Sensitivity_Light = value
				fan.setSensorsSensitivity(int(Sensitivity_Humidity),int(Sensitivity_Light))

			elif message.topic in (base_topic+"/lightsensorsettings_delayedstart/set",base_topic+"/lightsensorsettings_runningtime/set"):
				fan = Calima(mac, pin)

				#print('Reading data')
				LightSensorSettings = fan.getLightSensorSettings()
				LightSensorSettings_DelayedStart = LightSensorSettings.DelayedStart
				LightSensorSettings_RunningTime = LightSensorSettings.RunningTime
				
				if message.topic == base_topic+"/lightsensorsettings_delayedstart/set" : 
					LightSensorSettings_DelayedStart = value
				if message.topic == base_topic+"/lightsensorsettings_runningtime/set" : 
					LightSensorSettings_RunningTime = value
				fan.setLightSensorSettings(int(LightSensorSettings_DelayedStart), int(LightSensorSettings_RunningTime))

			elif message.topic in (base_topic+"/boostmode/set",base_topic+"/boostmodespeed/set",base_topic+"/boostmodesec/set"):
				fan = Calima(mac, pin)

				#print('Reading data')
				BoostMode = fan.getBoostMode()
				BoostMode_OnOff = BoostMode.OnOff
				BoostMode_Speed = BoostMode.Speed
				BoostMode_Seconds = BoostMode.Seconds
				
				if message.topic == base_topic+"/boostmode/set" : 
					BoostMode_OnOff = value
				if message.topic == base_topic+"/boostmodespeed/set" : 
					BoostMode_Speed = value
				if message.topic == base_topic+"/boostmodesec/set" : 
					BoostMode_Seconds = value
				
				fan.setBoostMode(int(BoostMode_OnOff),int(BoostMode_Speed),int(BoostMode_Seconds))

			elif message.topic in (base_topic+"/silenthours_on/set",base_topic+"/silenthours_startinghour/set",base_topic+"/silenthours_startingminute/set",base_topic+"/silenthours_endinghour/set",base_topic+"/silenthours_endingminute/set"):
				fan = Calima(mac, pin)

				#print('Reading data')
				SilentHours = fan.getSilentHours()
				SilentHours_On = SilentHours.On
				SilentHours_StartingHour = SilentHours.StartingHour
				SilentHours_StartingMinute = SilentHours.StartingMinute
				SilentHours_EndingHour = SilentHours.EndingHour
				SilentHours_EndingMinute = SilentHours.EndingMinute
				
				if message.topic == base_topic+"/silenthours_on/set" : 
					SilentHours_On = value
				if message.topic == base_topic+"/silenthours_startinghour/set" : 
					SilentHours_StartingHour = value
				if message.topic == base_topic+"/silenthours_startingminute/set" : 
					SilentHours_StartingMinute = value
				if message.topic == base_topic+"/silenthours_endinghour/set" : 
					SilentHours_EndingHour = value
				if message.topic == base_topic+"/silenthours_endingminute/set" : 
					SilentHours_EndingMinute = value
				fan.setSilentHours(int(SilentHours_On),int(SilentHours_StartingHour),int(SilentHours_StartingMinute),int(SilentHours_EndingHour), int(SilentHours_EndingMinute))

			elif message.topic in (base_topic+"/trickledays_weekdays/set",base_topic+"/trickledays_weekends/set"):
				fan = Calima(mac, pin)

				#print('Reading data')
				TrickleDays = fan.getTrickleDays()
				TrickleDays_Weekdays = TrickleDays.Weekdays
				TrickleDays_Weekends = TrickleDays.Weekends
				
				if message.topic == base_topic+"/trickledays_weekdays/set" : 
					TrickleDays_Weekdays = value
				if message.topic == base_topic+"/trickledays_weekends/set" : 
					TrickleDays_Weekends = value
				fan.setTrickleDays(int(TrickleDays_Weekdays),int(TrickleDays_Weekends))

			elif message.topic in (base_topic+"/automatic_cycles/set"):
				fan = Calima(mac, pin)

				#print('Reading data')
				fan.setAutomaticCycles(int(value))

			else:
				print("WTF")
			
			# Refresh data after a delay
			time.sleep(5)
			refresh_all(fan, client)

			fan.disconnect()

		except :
			exit()

########################################
print('Starting PaxCalima2MQTT.py')

# Device base MQTT topic
base_topic = "PaxCalima2MQTT/" + device_id

#print("creating new instance")
client = mqtt.Client(my_topic+"_"+ device_id)
client.on_message=on_message #attach function to callback

#print("connecting to broker")
client.connect(broker_address)

client.subscribe(base_topic+"/+/set")

sensors = [
    ['sensor',			None,    'humidity', 									'Humidity', 								'%', 	'humidity',		None, 	None, 	None],
    ['sensor',			None,    'temperature', 								'Temperature', 								'°C', 	'temperature',	None, 	None, 	None],
    ['sensor',			None,    'light', 										'Light', 									'lx', 	'illuminance',	None, 	None, 	None],
    ['sensor',			None,    'rpm', 										'RPM', 										'rpm', 	None, 			None, 	None, 	None],
    ['sensor',			None,    'state', 										'State', 									None, 	None, 			None, 	None, 	None],
    ['select',			'config','mode', 										'Mode', 									None, 	None, 			None, 	None, 	["MultiMode","DraftShutterMode","WallSwitchExtendedRuntimeMode","WallSwitchNoExtendedRuntimeMode","HeatDistributionMode"]],
    ['number',			'config','fanspeed_humidity', 							'Fanspeed Humidity', 						'rpm', 	None, 			0, 		2500, 	None],
    ['number',			'config','fanspeed_light', 								'Fanspeed Light', 							'rpm', 	None, 			0, 	 	2500, 	None],
    ['number',			'config','fanspeed_trickle', 							'Fanspeed Trickle', 						'rpm', 	None, 			0, 	 	2500, 	None],
    ['sensor',			'diagnostic','sensitivity_humidityon', 						'Sensitivity Humidity On', 					None, 	None, 			None, 	None, 	None],
    ['number',			'config','sensitivity_humidity', 						'Sensitivity Humidity', 					'%', 	'humidity', 	0, 	 	3,	 	None],
    ['sensor',			'diagnostic','sensitivity_lighton', 						'Sensitivity Light On', 					None, 	None, 			None, 	None, 	None],
    ['number',			'config','sensitivity_light', 							'Sensitivity Light', 						'lx', 	'illuminance',	0, 	 	3,	 	None],
    ['number',			'config','lightsensorsettings_delayedstart', 			'LightSensorSettings DelayedStart', 		's', 	None, 			0, 	 	10, 	None],
    ['number',			'config','lightsensorsettings_runningtime', 			'LightSensorSettings Runningtime', 			's', 	None, 			5, 	 	60, 	None],
    ['number',			'config','heatdistributorsettings_temperaturelimit', 	'HeatDistributorSettings TemperatureLimit', '°C', 	'temperature', 	0, 	 	100, 	None],
    ['number',			'config','heatdistributorsettings_fanspeedbelow', 		'HeatDistributorSettings FanSpeedBelow', 	'rpm', 	None, 			0, 	 	2500, 	None],
    ['number',			'config','heatdistributorsettings_fanspeedabove', 		'HeatDistributorSettings FanSpeedAbove', 	'rpm', 	None, 			0, 	 	2500, 	None],
    ['number',			'config','boostmode', 									'BoostMode', 								None, 	None, 			0, 	 	1,	 	None],
    ['number',			'config','boostmodespeed', 								'BoostMode Speed', 							'rpm', 	None, 			0, 	 	2500, 	None],
    ['number',			'config','boostmodesec', 								'BoostMode Time', 							's', 	None, 			0, 	 	900, 	None],
    ['number',			'config','silenthours_on', 								'SilentHours On', 							None, 	None, 			0, 	 	1,	 	None],
    ['number',			'config','silenthours_startinghour', 					'SilentHours StartingHour', 				'H', 	None, 			0, 	 	23, 	None],
    ['number',			'config','silenthours_startingminute', 					'SilentHours StartingMinute', 				'Min', 	None, 			0, 	 	59, 	None],
    ['number',			'config','silenthours_endinghour', 						'SilentHours EndingHour', 					'H', 	None, 			0, 	 	23, 	None],
    ['number',			'config','silenthours_endingminute', 					'SilentHours EndingMinute', 				'Min', 	None, 			0, 	 	59, 	None],
    ['number',			'config','trickledays_weekdays', 						'TrickleDays Weekdays', 					None, 	None, 			0, 	 	7,	 	None],
    ['number',			'config','trickledays_weekends', 						'TrickleDays Weekends', 					None, 	None, 			0, 	 	3,	 	None],
    ['number',			'config','automatic_cycles', 							'Automatic Cycles', 						None, 	None, 			0, 	 	3,	 	None]
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
    device_category, entity_category, sensor_id, sensor_name, unit_of_measurement, device_class, min, max, options = sensor
    
    # Construct the payload for each sensor
    sensor_payload = {
        "name": sensor_name,
        "state_topic": f"{base_topic}/{sensor_id}/state",
        "unique_id": f"{device_id}_{sensor_id}",
        "device": device_data  # Use the same device for all sensors
    }

    if entity_category is not None:
        sensor_payload["entity_category"] = entity_category
        if device_category in ("number","select"): 
            sensor_payload["command_topic"] = f"{base_topic}/{sensor_id}/set"

    if options is not None:
        sensor_payload["options"] = options
    if min is not None:
        sensor_payload["min"] = min
    if max is not None:
        sensor_payload["max"] = max
    if unit_of_measurement is not None:
        sensor_payload["unit_of_measurement"] = unit_of_measurement
    if device_class is not None:
        sensor_payload["device_class"] = device_class
    
    # Convert the dictionary to a JSON string
    discovery_message = json.dumps(sensor_payload, indent=4)
    
    # Print the discovery message
    client.publish(discovery_topic+"/"+device_category+"/"+sensor_id+"/config",discovery_message, retain=True)

fan = None
with bluetooth_lock: 
	try:
		# Publish data
		fan = Calima(mac, pin)

		refresh_all(fan, client)

		fan.disconnect()
	except :
		exit()

# Start on_message loop
client.loop_start()

# Loop to send fan speed every 5 minutes
try:
	while True:
        
		# Update every minute
		time.sleep(60)

		with bluetooth_lock: 
			try:
				# Publish data
				fan = Calima(mac, pin)

				FanState = fan.getState()

				if (FanState is None):
					print('Could not read data')
				else: 
					client.publish(base_topic+"/humidity/state",FanState.Humidity, retain=True)
					client.publish(base_topic+"/temperature/state",FanState.Temp, retain=True)
					client.publish(base_topic+"/light/state",FanState.Light, retain=True)
					client.publish(base_topic+"/rpm/state",FanState.RPM, retain=True)
					client.publish(base_topic+"/state/state",FanState.Mode, retain=True)

				#print('Disconnecting')
				fan.disconnect()
			except :
				exit()
			
		
except KeyboardInterrupt:
	print("Program interrupted by user.")
finally:
	# Stop the MQTT loop and disconnect
	client.loop_stop()
	client.disconnect()
print("Exiting")
