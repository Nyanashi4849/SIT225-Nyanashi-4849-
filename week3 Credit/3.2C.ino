#include "thingProperties.h"  // Include Arduino IoT Cloud properties
#define TRIG_PIN 9
#define ECHO_PIN 10
#define THRESHOLD_DISTANCE 10  // Threshold in cm

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    // Initialize Arduino Cloud connection
    initProperties();
    ArduinoCloud.begin(ArduinoIoTPreferredConnection);
    
    // Wait until connected
    while (ArduinoCloud.connected() == 0) {
        Serial.println("Connecting to Arduino Cloud...");
        delay(1000);
    }

    Serial.println("Connected to Arduino Cloud!");
}

void loop() {
    ArduinoCloud.update();  // Sync with IoT Cloud
    distance = measureDistance();  // Get distance from sensor

    Serial.print("Distance: ");
    Serial.println(distance);

    if (distance < THRESHOLD_DISTANCE) {
        alarm = true;  // Trigger alarm in the cloud
    } else {
        alarm = false;  // Reset alarm if distance is safe
    }

    delay(1000);  // Wait before taking the next reading
}

// Function to measure distance using HC-SR04
float measureDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    return duration * 0.034 / 2;  // Convert time to cm
}
