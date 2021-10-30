# bacnet-mqtt-publisher


Work in progress asyncio gateway device to publish BACnet data on mqtt pub sub. BACnet building automation data can get published to an MQTT topic in this fashion that shows a site ID and 5 VAV box temperature sensor readings:
`SITEID=5219_Oneida;VAV1=66.54;VAV2=69.26;VAV3=66.54;VAV4=69.26;VAV5=66.54;`

![schematic](/images/schematic.PNG)

* git ignore excludes `configs.py` which is a file that can contain passwords for the MQTT broker URL, as well as topics, and BACnet point for the BAS. The idea to modify the `configs.py` only per MQTT schema as well as BACnet building automation system (BAS) point schema. Change `configs_example.py` to `configs.py` after necessary modifications.

# Run script
` $ python3 mqtt_publisher.py`