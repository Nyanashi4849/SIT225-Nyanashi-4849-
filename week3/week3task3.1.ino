
// Include the Arduino LSM6DS3 library for sensor
#include <Arduino_LSM6DS3.h>

// Define variables to store acceleration values in X, Y, and Z (coordinates)
float x, y, z;

void setup() {
  Serial.begin(9600); // Set baud rate for serial communication
  while (!Serial);  // Wait for the serial port to initialize using while loop 
  Serial.println("Started");

  // Initialize the IMU sensor and check if it is detected
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1); //  if the IMU initialization fails execution does not occur.
  }

  // Print the accelerometer values to the serial monitor
  Serial.println(
    "Accelerometer sample rate = " 
    + String(IMU.accelerationSampleRate()) + " Hz");
}

void loop() {
  // Check if new accelerometer data is available
  if (IMU.accelerationAvailable()) {
    // Read the acceleration values and store them in x, y, and z variables defined above
    IMU.readAcceleration(x, y, z);
  }
  
  // Print the acceleration values to the serial monitor in formate x,y,z
  Serial.println(
    String(x) + ", " + String(y) + ", " + String(z));
  
  // Wait for 10 seconds before reading the next values
  delay(10000);
}
