import random
import time
from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883 


# generate client ID with pub prefix randomly
client_id = "test_1"
topic_to_publish = f"laptop/publish"
topic_to_listen = f"mobile/publish"
topic_to_wildcard = f"testing/*"

username = ""
password = ""


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(topic_to_listen)
            print(f"Connected to MQTT Broker on topic: {topic_to_wildcard}")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(20)
        msg = f"hello from {client_id}: {msg_count}"
        result = client.publish(topic_to_publish, msg)
        
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send {msg} to topic {topic_to_publish}")
        else:
            print(f"Failed to send message to topic {topic_to_publish}")
        msg_count += 1



def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))



def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
