// Include Arduino IoT Cloud properties
#include "thingProperties.h"  
// initiallise the pins we will be using
#define TRIG_PIN 9
#define ECHO_PIN 10
#define THRESHOLD_DISTANCE 10  // reads Threshold in cm

void setup() {
  // Set baud rate for serial communication
    Serial.begin(9600);
    // Set trigger pin as output and Set echo pin as input
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    // Initialize Arduino Cloud connection
    initProperties();
    ArduinoCloud.begin(ArduinoIoTPreferredConnection);
    
    // Wait until connected using while loop
    while (ArduinoCloud.connected() == 0) {
        Serial.println("Connecting to Arduino Cloud...");
        delay(1000);
    }

    Serial.println("Connected to Arduino Cloud!");
}

void loop() {
   // Sync with IoT Cloud
    ArduinoCloud.update(); 
    // Get distance from sensor
    distance = measureDistance();  
    // prints the distance on the serial monitor
    Serial.print("Distance: ");
    Serial.println(distance);
     // Trigger alarm in the cloud if threshold distance is reached
    if (distance < THRESHOLD_DISTANCE) {
        alarm = true;  
        // Reset alarm if distance is in safe distance
    } else {
        alarm = false;  
    }

    delay(1000);  // Wait before taking the next reading
}

//  measure distance using HC-SR04 every 2 microsecond.
float measureDistance() {
  // Ensure trigger pin is low , waits for 2 m.sec to again read the pin
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    // Ensure trigger pin is high, waits for 2 m.sec to again read the pin
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    // Ensure trigger pin is low, waits for 2 m.sec to again read the pin
    digitalWrite(TRIG_PIN, LOW);

    // formula to Measure the time taken for echo
    long duration = pulseIn(ECHO_PIN, HIGH);
    return duration * 0.034 / 2;  // Convert time to cm
}