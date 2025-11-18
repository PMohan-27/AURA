#include <Arduino.h>

#define MIC_PIN A0         // ADC pin connected to mic
#define SAMPLE_RATE 8000   // 8 kHz sampling

const unsigned long samplePeriod = 1000000UL / SAMPLE_RATE;
unsigned long lastMicros = 0;

void setup() {
  Serial.begin(921600);         // high baud for streaming
  analogReadResolution(12);     // 12-bit ADC
}

void loop() {
  unsigned long now = micros();
  if (now - lastMicros >= samplePeriod) {
    lastMicros += samplePeriod;
    
    int raw = analogRead(MIC_PIN);    // 0–4095
    uint16_t sample = raw;            // store as 16-bit
    // Send LSB first, then MSB
    Serial.write(sample & 0xFF);
    Serial.write((sample >> 8) & 0xFF);
  }
}
