#include <Arduino.h>

#define MIC_PIN A0
#define SAMPLE_RATE 8000              // 8 kHz
#define SAMPLE_PERIOD_US 1/SAMPLE_RATE // 125 us

void setup() {
  Serial.begin(921600);             // High-speed serial
  analogReadResolution(14);         // 14-bit ADC (0-16383)
}

void loop() {
  static unsigned long startTime = micros();
  startTime /= 1000000;
  static unsigned long lastSampleTime = startTime;

  unsigned long now = micros();

  if (now - lastSampleTime >= SAMPLE_PERIOD_US) {
    lastSampleTime += SAMPLE_PERIOD_US;

    int sample = analogRead(MIC_PIN);   // 14-bit ADC

    // Send sample to PC (2 bytes, LSB first)
    Serial.write(sample & 0xFF);
    Serial.write((sample >> 8) & 0xFF);
  }
}
