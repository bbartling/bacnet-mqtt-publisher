import BAC0, time, random


data_to_get = {'devices': {
   'boiler_temp': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '2'},
  'cooling_plant_temp': {'address': '12345:2',
   'object_type': 'analogInput',
   'object_instance': '3'},
  'air_handler_setpoint1': {'address': '12345:2',
   'object_type': 'analogValue',
   'object_instance': '301'},
  'air_handler_setpoint2': {'address': '12345:2',
   'object_type': 'analogValue',
   'object_instance': '302'},
  'hot_water_valve_command': {'address': '12345:2',
   'object_type': 'binaryOutput',
   'object_instance': '1'}}}

bacnet = BAC0.lite()



for info,devices in data_to_get.items():
    for device,attributes in devices.items():

        print(device)
        address=attributes['address']
        object_type=attributes['object_type']
        object_instance=attributes['object_instance']

        
        read_vals = f'{address} {object_type} {object_instance} presentValue'

        check = bacnet.read(read_vals)
        print("check ",check)
        print("check type",type(check))

'''
write_vals = f'{address} {object_type} {object_instance} presentValue {value}'
print("Excecuting write_vals statement:", write_vals)

write_result = bacnet.write(write_vals)

read_vals = f'{address} {object_type} {object_instance} presentValue'
check = bacnet.read(read_vals)
print("check ",check)
'''


bacnet.disconnect()
print('BACnet disconnected')
