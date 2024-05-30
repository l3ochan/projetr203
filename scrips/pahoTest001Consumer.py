# python3.6

import random, requests
import json
from paho.mqtt import client as mqtt_client

# --------------------------------------------------

broker = 'test.mosquitto.org'
port = 1883
topic = "/cRarhCaXsRsDYMN454Spd5rdmY4DyHGfY7QkE3ma"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
callback_api_version = mqtt_client.MQTTv5


# --------------------------------------------------

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# --------------------------------------------------

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        s = str(msg.payload.decode("utf-8"))
        print(f"Received `{s}` from `{msg.topic}` topic")
        s = json.loads(s)
    client.subscribe(topic)
    client.on_message = on_message

# --------------------------------------------------

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

# --------------------------------------------------

if __name__ == '__main__':
    run()

# --------------------------------------------------