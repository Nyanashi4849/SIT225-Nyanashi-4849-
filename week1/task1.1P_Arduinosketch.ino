// void setup() {
//   Serial.begin(9600);  // Start serial communication
//   pinMode(LED_BUILTIN, OUTPUT);  // Set the LED pin as output
// }

// void loop() {
//   if (Serial.available() > 0) {
//     int blinkCount = Serial.parseInt();  // Read the number sent from Python
//     for (int i = 0; i < blinkCount; i++) {
//       digitalWrite(LED_BUILTIN, HIGH);  // Turn LED on
//       delay(1000);  // Wait for 1 second
//       digitalWrite(LED_BUILTIN, LOW);  // Turn LED off
//       delay(1000);  // Wait for 1 second
//     }
//     int randomResponse = random(1, 10);  // Generate a random number between 1 and 10
//     Serial.println(randomResponse);  // Send it back to Python
//   }
// }
