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


def publish(client,msg):

    result = client.publish(topic_to_publish, msg)
    
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send {msg} to topic {topic_to_publish}")
    else:
        print(f"Failed to send message to topic {topic_to_publish}")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):  
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    
    if str(msg.payload) == "zone temps":
        publish(client,"avg=72.1;min=66.4;max=78.8")
        

def run():
    client = connect_mqtt()
    client.loop_start()


if __name__ == '__main__':
    run()
