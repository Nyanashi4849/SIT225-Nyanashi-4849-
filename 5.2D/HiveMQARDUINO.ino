#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h> 

// WiFi credentials
const char* ssid = "MSI 7239";
const char* password = "e646E{13";
const char* mqttServer = "http://7b1c32b9170b4ff79d2e5bdfe263f742.s1.eu.hivemq.cloud";
const int mqttPort = 8883;
const char* mqttUser = "dctDtas";
const char* mqttPassword = "Dct13Dtask";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  client.setServer(mqtt_server, 1883);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    while (1);
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  float x, y, z;
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);

    String payload = "{";
    payload += "\"x\": " + String(x) + ", ";
    payload += "\"y\": " + String(y) + ", ";
    payload += "\"z\": " + String(z) + "}";

    client.publish("sit225/gyroscope", payload.c_str());
    delay(1000);
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ArduinoNano33")) {
      client.subscribe("sit225/gyroscope");
    } else {
      delay(5000);
    }
  }
}