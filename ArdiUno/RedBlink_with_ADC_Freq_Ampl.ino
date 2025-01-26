#include <SoftwareSerial.h>
#include <TinyGPS++.h>

const int piezoPinA0 = A0;  // Piezoelectric sensor pin
const int ledPin = 13;       // White LED pin (Pin 13 for flickering)
const int ledPin2 = 12;      // Constant LED pin (Pin 12 for example)
const float freqThresholdLow = 20.0;  // Low frequency threshold (Hz)
const float freqThresholdHigh = 60.0; // High frequency threshold (Hz)

const int sampleWindow = 1000; // 1 second sample window for averaging

// GPS setup
SoftwareSerial gpsSerial(8, 9);
TinyGPSPlus gps;
float latitude, longitude;

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  gpsSerial.begin(9600);  // Initialize GPS serial communication
  pinMode(piezoPinA0, INPUT);  // Set piezo pin as input
  pinMode(ledPin, OUTPUT);      // Set LED pin for flickering as output
  pinMode(ledPin2, OUTPUT);     // Set LED pin for constant light as output
}

void loop() {
  // Update GPS data
  updateGPS();
  
  unsigned long startMillis = millis();  // Start time
  int cycles = 0;                        // Count cycles
  int adcValue;                          // Store ADC value

  float maxAmplitude = 0.0;  // Max vibration amplitude

  // Measure vibrations over 1 second
  while (millis() - startMillis < sampleWindow) {
    adcValue = analogRead(piezoPinA0);

    // Update max amplitude
    maxAmplitude = max(maxAmplitude, adcValue * (5.0 / 1023.0));

    // Count cycles for frequency
    if (adcValue > 512) {  
      while (analogRead(piezoPinA0) > 512);  
      while (analogRead(piezoPinA0) < 512);  
      cycles++;
    }
  }

  // Calculate frequency (in Hz) based on cycles
  float frequency = (float)cycles / (sampleWindow / 1000.0); // Hz

  // Display all sensor data including GPS
  Serial.print("ADC Value: ");
  Serial.print(adcValue);
  Serial.print("  |  Amplitude: ");
  Serial.print(maxAmplitude, 2);
  Serial.print(" V  |  ");

  // Print GPS coordinates regardless of status
  if (gps.location.isValid()) {
    Serial.print("Latitude: ");
    Serial.print(latitude, 6);
    Serial.print("  |  Longitude: ");
    Serial.print(longitude, 6);
    Serial.print("  |  ");
  } else {
    Serial.print("GPS: No Fix  |  ");
  }

  // Anomaly detection based on frequency
  if (cycles == 0) {
    Serial.println("No frequency detected.");
  } else {
    Serial.print("Frequency: ");
    Serial.print(frequency, 2);
    Serial.print(" Hz  |  ");

    if (frequency < freqThresholdLow || frequency > freqThresholdHigh) {
      Serial.println("Anomaly Detected!");
      digitalWrite(ledPin2, LOW);    
      flickerLED();  
    } else {
      Serial.println("Normal Operation.");
      digitalWrite(ledPin, LOW);  
      digitalWrite(ledPin2, HIGH); 
    }
  }
}

void updateGPS() {
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      if (gps.location.isValid()) {
        latitude = gps.location.lat();
        longitude = gps.location.lng();
      }
    }
  }
}

void flickerLED() {
  // Flicker LED for a short duration when anomaly is detected
  for (int i = 0; i < 5; i++) {   // Flicker 5 times
    digitalWrite(ledPin, HIGH);   // Turn LED on
    delay(100);                   // Wait for 100ms
    digitalWrite(ledPin, LOW);    // Turn LED off
    delay(100);                   // Wait for 100ms
  }
}