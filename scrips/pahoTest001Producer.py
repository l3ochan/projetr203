import random
import time
import requests
import json
import logging
from paho.mqtt import client as mqtt_client

# --------------------------------------------------

broker = 'test.mosquitto.org'
port = 1883
topic = "/1951a"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
callback_api_version = mqtt_client.MQTTv5
api_key = "***RECACTED***"
lat = 43.88658787401135
lon = -0.5083205120259326
api_link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

# --------------------------------------------------

def get_data():
    response = requests.get(api_link)
    if response.status_code == 200:
        return json.dumps(response.json())  # Convert dictionary to JSON string
    else:
        return json.dumps({"error": f"There's a {response.status_code} error with your request"})

# --------------------------------------------------

def connect_mqtt():
    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {reason_code}\n")

    client = mqtt_client.Client(client_id=client_id, protocol=callback_api_version)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# --------------------------------------------------

def publish(client):
    msg = get_data()
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

# --------------------------------------------------

def run():
    client = connect_mqtt()
    client.loop_start()
    try:
        while True:
            publish(client)
            time.sleep(1200)  # Wait 1 minute before sending the next message
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        client.loop_stop()
        client.disconnect()

# --------------------------------------------------

if __name__ == '__main__':
    run()

# --------------------------------------------------
