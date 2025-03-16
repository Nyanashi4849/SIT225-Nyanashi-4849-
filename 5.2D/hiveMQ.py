import pandas as pd
import paho.mqtt.client as mqtt
import time
import json

#  Read CSV File
csv_file = "5.2D.csv"
df = pd.read_csv(csv_file)

#  HiveMQ Cloud MQTT Configuration
MQTT_BROKER = "7b1c32b9170b4ff79d2e5bdfe263f742.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "taskD/gyroscope"
MQTT_USERNAME = "dctDtask"
MQTT_PASSWORD = "Dct13Dtask"

is_connected = False  # Track connection state

#  MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    global is_connected
    if rc == 0:
        print(" Connected to HiveMQ Cloud!")
        is_connected = True
    else:
        print(f"Connection failed with code {rc}")
        is_connected = False

def on_disconnect(client, userdata, rc):
    global is_connected
    print("Disconnected from MQTT broker. Attempting to reconnect...")
    is_connected = False
    while not is_connected:
        try:
            client.reconnect()
            print("Reconnected successfully!")
            is_connected = True
        except Exception as e:
            print(f"Reconnection failed: {e}. Retrying in 5s...")
            time.sleep(5)

def on_publish(client, userdata, mid):
    print(f"Message {mid} successfully published!")

#  MQTT Client Setup
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  # Authenticate
client.tls_set()  # Enable TLS encryption
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

#  Connect to HiveMQ Cloud
print("Connecting to HiveMQ Cloud...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

#  Publish each row as a JSON message
for index, row in df.iterrows():
    data = row.to_dict()
    json_data = json.dumps(data)

    # Wait until reconnected before publishing
    while not is_connected:
        print(" Waiting for reconnection...")
        time.sleep(1)

    # Publish message with QoS 1
    result = client.publish(MQTT_TOPIC, json_data, qos=1)
    status = result.rc

    if status == 0:
        print(f" Published: {json_data}")
    else:
        print(f" Failed to publish message, result code: {status}. Retrying...")
        time.sleep(5)  # Give some delay before retrying

    time.sleep(2)  # Adjusted delay to prevent rate limiting

#  Cleanup
client.loop_stop()
client.disconnect()
