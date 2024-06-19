#include <ThingSpeak.h>
#include <ESP8266WiFi.h>
#include <Wire.h>
#include <HX711.h>
#include <MPU6050.h>

// Define the pins for HX711 connection
const int LOADCELL_DOUT_PIN = D1;   // D1 pin for HX711 data output
const int LOADCELL_SCK_PIN = D2;    // D2 pin for HX711 clock input

// Define the MPU-6050 I2C address
const uint8_t MPU_addr = 0x68;  // I2C address of the MPU-6050

// Define calibration values
const float LOADCELL_CALIBRATION_FACTOR = 1.0;  // Replace with your load cell calibration factor

// Initialize the HX711 and MPU-6050 library instances
HX711 scale;
MPU6050 mpu;

// WiFi settings
const char* ssid = "AJ";
const char* password = "anushka1502";

// ThingSpeak settings
const char* server = "api.thingspeak.com";
const unsigned long channelID = 2185632; // Replace with your ThingSpeak channel ID
const char* writeAPIKey = "TBYC75VG58D1DYGK";   // Replace with your ThingSpeak write API Key

WiFiClient espClient; // Declare the WiFiClient variable

void setup() {
  Serial.begin(9600);   // Initialize serial communication

  // Set up the HX711 connections
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale();    // Initialize the scale

  Wire.begin(12, 13);  // Specify the SDA (D6) and SCL (D7) pins for MPU-6050
  mpu.initialize();    // Initialize the MPU-6050

  Serial.println("Ready to read from the load cell and gyroscope sensor!");

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize ThingSpeak
  ThingSpeak.begin(espClient);
}

void loop() {
  // Read the raw value from the load cell
  long rawValue = scale.read();

  // Apply the calibration factor to calculate the weight
  float weight = rawValue / LOADCELL_CALIBRATION_FACTOR;
  weight = weight / 1000000.0;

  // Print the load cell weight
  Serial.print("Load Cell Weight: ");
  Serial.print(weight);
  Serial.println(" kg");

  // Read gyroscope data
  int16_t gyroX, gyroY, gyroZ;
  mpu.getRotation(&gyroX, &gyroY, &gyroZ);

  // Calculate the single value of angular velocity
  float angularVelocity = (abs(gyroX) + abs(gyroY) + abs(gyroZ)) / 3.0;

  angularVelocity_ = angularVelocity / 1000;

  // Print the angular velocity
  Serial.print("Angular Velocity: ");
  Serial.println(angularVelocity_);

  // Update ThingSpeak channel with weight and angular velocity data
  ThingSpeak.setField(1, weight);
  ThingSpeak.setField(2, angularVelocity);
  int response = ThingSpeak.writeFields(channelID, writeAPIKey);

  if (response == 200) {
    Serial.println("Data sent to ThingSpeak successfully");
  } else {
    Serial.print("Error sending data to ThingSpeak. HTTP error code: ");
    Serial.println(response);
  }

  delay(1000);
}
