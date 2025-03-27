# Import necessary libraries, MQTT protocol for subscribing to sensor data, MongoDB client for storing data, json fo  JSON data format,
# matplotlib  For data visualization,  certifi for SSL certificate verification with MongoDB
import paho.mqtt.client as mqtt  
import pymongo  
import json 
import pandas as pd
import matplotlib.pyplot as plt  
import os 
import certifi 

# MQTT Configuration , MQTT broker address, Secure MQTT port, Topic to subscribe to, MQTT username, MQTT password
MQTT_BROKER = "7b1c32b9170b4ff79d2e5bdfe263f742.s1.eu.hivemq.cloud"  
MQTT_PORT = 8883 
MQTT_TOPIC = "Nyanashi"  
MQTT_USERNAME = "dctDtask"  
MQTT_PASSWORD = "Dct13Dtask" 

# MongoDB Configuration
MONGO_URI = "mongodb+srv://nyanashi:mongoDB@cluster0.i0gub.mongodb.net/taskD?retryWrites=true&w=majority&tls=true"

# Establish connection to MongoDB,  Select database,  Select collection
mongo_client = pymongo.MongoClient(MONGO_URI)  
db = mongo_client["taskD"] 
collection = db["N"] 

print("MongoDB Connection Successful!")  # Print success message if connected to mongodb

# List to temporarily store received data
data_list = []

# Callback function for successful MQTT connection
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        # if connected print message that it have connected successfully.
        print("Connected to MQTT!")  
         # Subscribe to the specified topic
        client.subscribe(MQTT_TOPIC) 
    else:
        # Print error code if not connected
        print(f"Connection failed with code {rc}")  

# Callback function for processing received messages
def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))  # Decode JSON message
        print(f"Received: {data}")  # Print received data

        # Store received data into MongoDB
        collection.insert_one(data)
        data_list.append(data)
        # exception if data not proccesed correctly. print error message
    except Exception as e:
        print(f"Error: {e}")  

# Initialize MQTT client by giving username and password.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  
 # Enable TLS for secure connection
client.tls_set() 

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message
# prints if succesfully connected to MQTT
print("Connecting to MQTT...")
 # Connect to the MQTT broker and port
client.connect(MQTT_BROKER, MQTT_PORT) 
 # print message 
print("Listening for messages (Run for at least 5 minutes)...")
client.loop_start()  # Start listening in the background

import time
# Wait for 30 minutes to collect data
time.sleep(1800)  

# Stop MQTT loop and disconnect when data collected
client.loop_stop()
client.disconnect()
print("MQTT Disconnected. Data collection completed.")  
