login_info = {"broker_url": "test.mosquitto.org", 
                "username": "user",
                "password": "pass!"}

site_id = "5219_Oneida"

poll_frequency = 300

topics = (
    f"sensor/telemetry/hvac/{site_id}/zone/temp",
    f"sensor/telemetry/hvac/{site_id}/zone/temp/setpoint",
    f"sensor/telemetry/hvac/{site_id}/vav/reheat/valve",
    f"sensor/telemetry/hvac/{site_id}/vav/reheat/temp",
    f"sensor/telemetry/hvac/{site_id}/vav/damper",
    f"sensor/telemetry/eletrical/{site_id}"
    )
  
  
topic_filters = (
    f"sensor/telemetry/hvac/{site_id}/zone/temp",
    f"sensor/telemetry/hvac/{site_id}/zone/temp/setpoint",
    f"sensor/telemetry/hvac/{site_id}/vav/reheat/valve",
    f"sensor/telemetry/hvac/{site_id}/vav/reheat/temp",
    f"sensor/telemetry/hvac/{site_id}/vav/damper",
    f"sensor/telemetry/eletrical/{site_id}",
    f"bacnet/write/{site_id}"
)    
    
    
subscribe_topic = (f"bacnet/write/{site_id}")
		
zone_temps = {'devices': {
   'VAV1': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV2': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV3': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV4': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV5': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'}}}
   
   
zone_setpoints = {'devices': {
   'VAV1': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV2': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV3': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV4': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV5': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'}}}
   
   
zone_reheat_valves = {'devices': {
   'VAV1': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV2': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV3': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV4': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV5': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'}}}
   
zone_reheat_temps = {'devices': {
   'VAV1': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV2': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV3': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV4': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV5': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'}}}
   
zone_reheat_dampers = {'devices': {
   'VAV1': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV2': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV3': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'VAV4': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'VAV5': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'}}}
