import random
import json
import time
import mysql.connector
from mysql.connector import Error
from paho.mqtt import client as mqtt_client

# --------------------------------------------------

broker = 'test.mosquitto.org'
port = 1883
topic = "/1951a"
client_id = f'python-mqtt-{random.randint(0, 100)}'
callback_api_version = mqtt_client.MQTTv5

# --------------------------------------------------

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {reason_code}\n")

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# --------------------------------------------------

def store_in_db(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='projetr203', # change this to your database name
            user='ProjetUser',
            password='***RECACTED***'
        )
        print("Connected to database")

        if connection.is_connected():
            cursor = connection.cursor()

            sql_insert_query = """
            INSERT INTO data (lon, lat, temp, feels_like, temp_min, temp_max, pressure, humidity, date_of_creation, name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
            """

            cursor.execute(sql_insert_query, data)
            connection.commit()
            print("Successfully written data to database")

    except Error as err:
        print(f"Error while connecting to MySQL: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# --------------------------------------------------

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        s = str(msg.payload.decode("utf-8"))
        print(f"Received `{s}` from `{msg.topic}` topic")

        try:
            json_data = json.loads(s)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return

        try:
            lon = json_data['coord']['lon']
            lat = json_data['coord']['lat']
            temp = json_data['main']['temp']
            feels_like = json_data['main']['feels_like']
            temp_min = json_data['main']['temp_min']
            temp_max = json_data['main']['temp_max']
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            name = json_data['name']

            data_tuple = (lon, lat, temp, feels_like, temp_min, temp_max, pressure, humidity, name)
            print("Identified data from message")
            store_in_db(data_tuple)
        except KeyError as e:
            print(f"Key error: {e}")

    client.subscribe(topic)
    client.on_message = on_message

# --------------------------------------------------

def run():
    client = None
    while True:
        try:
            client = connect_mqtt()
            subscribe(client)
            client.loop_forever()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # wait for a while before attempting to reconnect

# --------------------------------------------------

if __name__ == '__main__':
    run()

# --------------------------------------------------
