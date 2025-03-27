// Include library for LSM6DS3 IMU sensor
#include <Arduino_LSM6DS3.h> 
void setup() {
  // Initialize serial communication with baud rate 115200
    Serial.begin(115200);
 // Wait for serial port to initialize
    while (!Serial); 
    
    // Initialize IMU sensor and check if it is available and Print error if initialization fails
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!"); 
        while (1); //  if IMU fails to initialize execution does not happen
    }
}

void loop() {
 // Variables to store gyroscope readings
    float x, y, z; 
    
    // Check if new gyroscope data is available using if loop
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z); // Read gyroscope data
        
        // Print timestamp and gyroscope readings in CSV format
        Serial.print(millis()); // Timestamp in milliseconds
        Serial.print(",");
        Serial.print(x); // X-axis 
        Serial.print(",");
        Serial.print(y); // Y-axis 
        Serial.print(",");
        Serial.println(z); // Z-axis 
    }
    
    delay(20); // Delay for 20ms 
}
