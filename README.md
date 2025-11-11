# AURA - Adaptive Understanding & Responsive Assistant
Developed by Parasinder Mohan, Krrish Lala, Luca Seaman

Tools used - 
     (1) Hardwarre - 
                    ESP 32
                    Adafruit 1314 4Ω 3W
                    DFRobot Fermion: I2S MEMS Microphone (Breakout) module.
     (2) Software - 
                    | Function                 | API / Library                                     | Description                                   |
| ------------------------ | ------------------------------------------------- | --------------------------------------------- |
| **Speech-to-Text**       | `SpeechRecognition` (Google STT) or `Whisper API` | Converts mic audio → text                     |
| **Therapy Logic / Chat** | Hugging Face API (`flan-t5-small`)                | Generates empathetic, conversational response |
| **Text-to-Speech**       | `gTTS` (Google TTS)                               | Converts reply text → audio (WAV/PCM)         |
| **Serial Communication** | `pyserial`                                        | Sends/receives audio with ESP32               |
| **Audio I/O**            | `soundfile`, `numpy`                              | Handles WAV encoding and PCM conversion       |

