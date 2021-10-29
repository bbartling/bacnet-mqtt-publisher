import asyncio, json, BAC0
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

from bacnet_actions import BacNetWorker
import configs



broker_url = configs.login_info["broker_url"]
username = configs.login_info["username"]
password = configs.login_info["password"]
site_id = configs.site_id
poll_frequency = configs.poll_frequency
zone_temps = configs.zone_temps
zone_setpoints = configs.zone_setpoints


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
            f"sensor/telemetry/hvac/{site_id}/zone/temp",
            f"sensor/telemetry/hvac/{site_id}/zone/temp/setpoint",
            f"sensor/telemetry/hvac/{site_id}/vav/reheat/valve",
            f"sensor/telemetry/hvac/{site_id}/vav/reheat/temp",
            f"sensor/telemetry/hvac/{site_id}/vav/damper",
            f"sensor/telemetry/eletrical/{site_id}",
            f"bacnet/write/{site_id}"
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
        await client.subscribe(f"bacnet/write/{site_id}")

        # Publish a random value to each of these topics
        topics = (
            f"sensor/telemetry/hvac/{site_id}/zone/temp",
            f"sensor/telemetry/hvac/{site_id}/zone/temp/setpoint",
            f"sensor/telemetry/hvac/{site_id}/vav/reheat/valve",
            f"sensor/telemetry/hvac/{site_id}/vav/reheat/temp",
            f"sensor/telemetry/hvac/{site_id}/vav/damper",
            f"sensor/telemetry/eletrical/{site_id}",
        )
        task = asyncio.create_task(post_to_topics(client, topics))
        tasks.add(task)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)

async def post_to_topics(client, topics):
    while True:
        for topic in topics:
        
            # PUBLISH ZONE TEMPS TO BUS
            if topic == f"sensor/telemetry/hvac/{site_id}/zone/temp":
                for info,devices in zone_temps.items():
                    for device,attributes in devices.items():
                    
                        read_result = await BacNetWorker.do_things(
                        "read",
                        attributes['address'],
                        attributes['object_type'],
                        attributes['object_instance']
                        )
                        
                        topic_to_pub = topic + "/" + str(read_result)
                        print(topic_to_pub)
                        await client.publish(topic, json.dumps(topic_to_pub), qos=1)
            else:
                print(f'PASSING TOPIC on {topic} to PUBLISH/post')
            await asyncio.sleep(poll_frequency) # [seconds]

            # PUBLISH ZONE SETPOINTS TO BUS
            if topic == f"sensor/telemetry/hvac/{site_id}/zone/setpoint":
                for info,devices in zone_setpoints.items():
                    for device,attributes in devices.items():
                    
                        read_result = await BacNetWorker.do_things(
                        "read",
                        attributes['address'],
                        attributes['object_type'],
                        attributes['object_instance']
                        )
                        
                        topic_to_pub = topic + "/" + str(read_result)
                        print(topic_to_pub)
                        await client.publish(topic, json.dumps(topic_to_pub), qos=1)
            else:
                print(f'PASSING TOPIC on {topic} to PUBLISH/post')
            await asyncio.sleep(poll_frequency) # [seconds]

async def log_messages(messages, template):
    async for message in messages:
        payload_ = template.format(message.payload.decode())
        print("log_messages def hit ",payload_)
        if message.payload.decode() == "Testing123":
            print("YES payload_ == Testing123, DO SOMETHING")
        else:
            print("payload_ not == Testing123")


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
    reconnect_interval = 30  # [seconds]
    while True:
        try:
            await advanced_example()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)



asyncio.run(main())
