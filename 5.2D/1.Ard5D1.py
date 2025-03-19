import paho.mqtt.client as mqtt
import pymongo
import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import certifi

MQTT_BROKER = "7b1c32b9170b4ff79d2e5bdfe263f742.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "Nyanashi"
MQTT_USERNAME = "dctDtask"
MQTT_PASSWORD = "Dct13Dtask"

import pymongo
import certifi

MONGO_URI = "mongodb+srv://nyanashi:mongoDB@cluster0.i0gub.mongodb.net/taskD?retryWrites=true&w=majority&tls=true"

mongo_client = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = mongo_client["taskD"]
collection = db["N"]

print("MongoDB Connection Successful!")


data_list = []

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        print(f"Received: {data}")

        # Store in MongoDB
        collection.insert_one(data)
        data_list.append(data)

    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set()  
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to MQTT...")
client.connect(MQTT_BROKER, MQTT_PORT)

print("Listening for messages (Run for at least 5 minutes)...")
client.loop_start()

import time
time.sleep(1800)  # Collecting data for 30 minutes

client.loop_stop()
client.disconnect()
