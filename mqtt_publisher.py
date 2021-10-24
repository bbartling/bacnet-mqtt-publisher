import asyncio, json, BAC0
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

from bacnet_actions import BacNetWorker
import configs


data_to_get = configs.devices
broker_url = configs.login_info["broker_url"]
username = configs.login_info["username"]
password = configs.login_info["password"]



async def advanced_example():
    # context managers create a stack to help manage them
    
    async with AsyncExitStack() as stack:
        # Keep track of the asyncio tasks that we create, so that
        # we can cancel them on exit
        tasks = set()
        stack.push_async_callback(cancel_tasks, tasks)

        # Connect to the MQTT broker
        client = Client(broker_url,
                username=username,
                password=password)
        await stack.enter_async_context(client)

        # topic filters
        topic_filters = (
            "sensor/telemetry/hvac/temps",
            "sensor/telemetry/hvac/temps/setpoints",
            "sensor/telemetry/eletrical/main/power"
        )
        for topic_filter in topic_filters:
        
            # Log all messages that matches the filter
            manager = client.filtered_messages(topic_filter)
            messages = await stack.enter_async_context(manager)
            template = f'[topic_filter="{topic_filter}"] {{}}'
            task = asyncio.create_task(log_messages(messages, template))
            tasks.add(task)

        # Messages that doesn't match a filter will get logged here
        messages = await stack.enter_async_context(client.unfiltered_messages())
        print("INCOMING, NO TEMPLATE FOUND FOR THIS ONE")
        task = asyncio.create_task(log_messages(messages, "[unfiltered] {}"))
        tasks.add(task)

        # Subscribe to topic(s)
        # subscribe *after* starting the message
        await client.subscribe("write/setpoint/#")

        # Publish a random value to each of these topics
        topics = (
            "sensor/telemetry/hvac/temps",
            "sensor/telemetry/hvac/temps/setpoints",
            "sensor/telemetry/eletrical/main/power"
        )
        task = asyncio.create_task(post_to_topics(client, topics))
        tasks.add(task)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)

async def post_to_topics(client, topics):
    while True:
        for topic in topics:
        
            if topic == "sensor/telemetry/hvac/temps":
            
                device_mapping = {}
                
                for info,devices in data_to_get.items():
                    for device,attributes in devices.items():
                    
                        read_result = await BacNetWorker.bacnet_ops(
                        "read",
                        attributes['address'],
                        attributes['object_type'],
                        attributes['object_instance']
                        )
                        
                        device_mapping[device] = {'pv':read_result}
                        
                print(device_mapping)
                
                await client.publish(topic, json.dumps(device_mapping), qos=1)
            else:
                print(f'PASSING TOPIC on {topic} to PUBLISH/post')
            await asyncio.sleep(60)

async def log_messages(messages, template):    
    async for message in messages:
        # 🤔 Note that we assume that the message paylod is an
        # UTF8-encoded string (hence the `bytes.decode` call).
        print("FUNCTION HIT def log_messages!")
        print("TEMPLATES TO DECODE")
        print(template.format(message.payload.decode()))

async def cancel_tasks(tasks):
    for task in tasks:
        if task.done():
            continue
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

async def main():
    # Run the advanced_example indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 10  # [seconds]
    while True:
        try:
            await advanced_example()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)



asyncio.run(main())
