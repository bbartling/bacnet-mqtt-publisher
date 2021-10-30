# bacnet-mqtt-publisher


Work in progress asyncio gateway device to publish BACnet data on mqtt pub sub


* git ignore excludes `configs.py` which is a file that can contain passwords for the MQTT broker URL, as well as topics, and BACnet point for the BAS. The idea to modify the `configs.py` only per MQTT schema as well as BACnet building automation system (BAS) point schema.


