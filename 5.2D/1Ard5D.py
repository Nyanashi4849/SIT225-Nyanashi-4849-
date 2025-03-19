import paho.mqtt.client as mqtt
# from cloudant.client import CouchDB
# import CouchDB
import couchdb
import json
import pandas as pd
import os
import time

MQTT_BROKER = "7b1c32b9170b4ff79d2e5bdfe263f742.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "Nyanashi"
MQTT_USERNAME = "dctDtask"
MQTT_PASSWORD = "Dct13Dtask"

COUCHDB_URL = "http://127.0.0.1:5984/"
COUCHDB_USER = "Nyanashi"
COUCHDB_PASS = "1977"

# Connect to CouchDB
client_couch = couchdb.Server(COUCHDB_URL)
client_couch.resource.credentials = (COUCHDB_USER, COUCHDB_PASS)

# Database name
db_name = "taskd"

# Connect to the existing database
if db_name in client_couch:
    db = client_couch[db_name]  # Connect to existing database
    print(f"Connected to existing database: {db_name}")
else:
    db = client_couch.create(db_name)  # Create new database
    print(f"Database '{db_name}' created.")

# Now, you can insert documents into 'db'
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
        print(f" Receiving data : {data}")

        db.create_document(data)

        data_list.append(data)

    except Exception as e:
        print(f"Error: {e}")

client_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_mqtt.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client_mqtt.tls_set()  
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

print("MQTT connecting...")
client_mqtt.connect(MQTT_BROKER, MQTT_PORT)

client_mqtt.loop_start()

time.sleep(900)

client_mqtt.loop_stop()
client_mqtt.disconnect()
