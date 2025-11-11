# AURA - Adaptive Understanding & Responsive Assistant
Developed by Parasinder Mohan, Krrish Lala, Luca Seaman

Tools used - 
     💻 SOFTWARE SETUP
🧩 ESP32 Firmware

Written in Arduino (C++) using:

WiFi.h

WiFiClientSecure.h

HTTPClient.h

driver/i2s.h

Functions:

Captures audio from the Fermion I²S mic

Sends raw PCM over Serial USB to the laptop

Receives AI-generated PCM audio from laptop

Streams audio to Adafruit I²S amplifier

Sample rate:

16000 Hz mono (for Whisper + Hugging Face compatibility)                                   |
| ------------------------ | ------------------------------------------------- | --------------------------------------------- |
| **Speech-to-Text**       | `SpeechRecognition` (Google STT) or `Whisper API` | Converts mic audio → text                     |
| **Therapy Logic / Chat** | Hugging Face API (`flan-t5-small`)                | Generates empathetic, conversational response |
| **Text-to-Speech**       | `gTTS` (Google TTS)                               | Converts reply text → audio (WAV/PCM)         |
| **Serial Communication** | `pyserial`                                        | Sends/receives audio with ESP32               |
| **Audio I/O**            | `soundfile`, `numpy`                              | Handles WAV encoding and PCM conversion       |

