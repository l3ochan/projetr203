# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client

# --------------------------------------------------

broker = 'test.mosquitto.org'
port = 1883
topic = "/test917298739287"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
callback_api_version = mqtt_client.MQTTv5

# --------------------------------------------------

def connect_mqtt():
    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, protocol=callback_api_version)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# --------------------------------------------------

def publish(client):
    time.sleep(1)
    
    msg = "A single message from my computer"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

# --------------------------------------------------

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

# --------------------------------------------------

if __name__ == '__main__':
    run()

# --------------------------------------------------