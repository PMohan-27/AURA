#include <Arduino.h>

#define MIC_PIN A1
#define SAMPLE_RATE 8000                 // realistic stable rate
#define SAMPLE_PERIOD_US 1000000 / SAMPLE_RATE
#define NUM_SAMPLES 26000                // 4 sec * 6500 Hz
#define SPEAKER_PIN DAC          // DAC output on R4 Minima
#define PLAYBACK_RATE 15000
#define PLAYBACK_PERIOD_US (1000000UL / PLAYBACK_RATE)

int16_t sample = 0;

void setup() {
  Serial.begin(921600);
  analogReadResolution(14);
  
}

void loop() {
  // Wait for handshake
  if (Serial.available()) {
      char cmd = Serial.read();
      if(cmd == 'R'){
        unsigned long lastSampleTime = micros();

        for (int i = 0; i < NUM_SAMPLES; i++) {
          // wait until next sample
          while (micros() - lastSampleTime < SAMPLE_PERIOD_US) { }
          lastSampleTime += SAMPLE_PERIOD_US;

          int sample = analogRead(MIC_PIN);
          Serial.write(sample & 0xFF);
          Serial.write(sample >> 8);
        }
      }
  
      if (cmd == 'P') {
          // Read length first (4 bytes little-endian)
          while (Serial.available() < 4) {}
          int len = 0;
          for (int i = 0; i < 4; i++) {
            len |= Serial.read() << (i * 8);
          }

          // Read and play samples
          for (int i = 0; i < len; i++) {
            while (Serial.available() < 2) {}  // wait for one sample
            uint8_t low = Serial.read();
            uint8_t high = Serial.read();
            sample = (high << 8) | low;

            uint8_t pwmVal = map(sample, -32768, 32767, 0, 255);
            analogWrite(SPEAKER_PIN, pwmVal);

            delayMicroseconds(PLAYBACK_PERIOD_US);
          }
        }
  }
}

