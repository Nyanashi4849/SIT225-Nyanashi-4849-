#include <Arduino_LSM6DS3.h>   
#include <WiFiNINA.h>
#include <PubSubClient.h>

// WiFi Credentials
const char* ssid = "TM";
const char* password = "TM200513";

// MQTT Broker Details
const char* mqttServer = "7b1c32b9170b4ff79d2e5bdfe263f742.s1.eu.hivemq.cloud";
const int mqttPort = 8883;
const char* mqttUser = "dctDtask";
const char* mqttPassword = "Dct13Dtask";

// MQTT Topic
const char* mqttTopic = "Nyanashi";

WiFiSSLClient wifiClient; 
PubSubClient client(wifiClient);

void setup() {
    Serial.begin(115200);
    delay(1000);

    // Connect to WiFi
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Connect to MQTT
    client.setServer(mqttServer, mqttPort);
    Serial.println("Connecting to MQTT...");

    while (!client.connected()) {
        if (client.connect("304eb72112904f44bcfe2947ba22c412", mqttUser, mqttPassword)) {
            Serial.println("Connected to MQTT Broker!");
        } else {
            Serial.print("Failed! State: ");
            Serial.println(client.state());
            delay(5000);
        }
    }

    // Initialize IMU Sensor
    if (!IMU.begin()) {
        Serial.println("IMU Sensor not detected!");
        while (1);
    }
}

void loop() {
    float x, y, z;
    
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);
        
        // Get Timestamp
        unsigned long timestamp = millis();

        // Create JSON Payload
        String payload = "{ \"x\": " + String(x) + ", \"y\": " + String(y) + ", \"z\": " + String(z) + ", \"timestamp\": " + String(timestamp) + " }";

        // Publish Data
        if (client.publish(mqttTopic, payload.c_str())) {
            Serial.println("Sending data to MQTT: " + payload);
        } else {
            Serial.println("Failed to send data!");
        }
    }
    
    client.loop();
    delay(1000);
}