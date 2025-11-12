#include <Arduino.h>

#define MIC_PIN 34
#define SAMPLE_RATE 4000

unsigned long lastMicros = 0;
const unsigned long samplePeriod = 1000000 / SAMPLE_RATE;

void setup() {
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
  Serial.begin(115200);
}

void loop() {
  if (micros() - lastMicros >= samplePeriod) {
    lastMicros += samplePeriod;
    int raw = analogRead(MIC_PIN);    // 0–4095
    uint16_t sample = raw;            // 12-bit
    Serial.write((byte*)&sample, 2);  // binary stream
  }
}
