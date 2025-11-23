
# 🌟 AURA — Arduino + ESP32 AI Therapy Bot

**Voice-Activated Conversational Bot using Arduino UNO R4, Analog Mic, PAM8302A Speaker Amp, Python STT/TTS, and Azure/Google AI**

AURA is a compact, voice-first conversational bot designed for therapy-style interactions.
It captures audio from an electret microphone, streams it to a Python AI backend for STT → LLM → TTS, and returns synthesized speech through a Class-D amplifier.

---

# 📸 Hardware Overview (Your Circuit)

AURA uses a custom audio front-end built around the Arduino UNO R4 Minima, SEN0487 analog microphone, and PAM8302A mono amplifier.

**Full schematic (from your Altium design):**
`/mnt/data/9cf53d3f-11ad-4ca5-a3c5-4a2431d1e6c2.png`

---

## 🧩 Hardware Architecture

```
 ┌───────────────────────────┐
 │        Arduino R4         │
 │  MIC_IN (A0)  ◄─────┐     │
 │                      │     │
 │  SPK_OUT (D9) ───────┼──► PAM8302A Amplifier ─► Speaker
 │                      │
 └──────────────────────┘
         ▲
         │
   SEN0487 Analog Mic
```

---

## 🔌 Pin Connections

### 🎤 Microphone (SEN0487 → Arduino)

| SEN0487 Pin | Arduino Pin | Description                     |
| ----------- | ----------- | ------------------------------- |
| VCC         | 3.3V        | Microphone power                |
| GND         | GND         | Common ground                   |
| OUT (A)     | MIC_IN (A0) | Via 10 µF AC-coupling capacitor |

**C2 = 10 µF coupling capacitor**
Removes DC bias and ensures clean analog audio.

---

### 🔊 Speaker Amplifier (Arduino → PAM8302)

| Arduino Pin  | PAM8302 Pin | Description      |
| ------------ | ----------- | ---------------- |
| D9 (SPK_OUT) | A+ (P1)     | PWM audio output |
| GND          | A- (P2)     | Audio reference  |
| +5V          | VIN (P4)    | Amplifier power  |
| GND          | GND (P5)    | Ground           |

**C1 = 10 µF smoothing capacitor**
Reduces noise on amplifier input.

**R1 = 10k pull-down**
Stabilizes SPK_OUT at idle.

---

# 🔧 Software Architecture

AURA uses a hybrid microcontroller + Python backend model:

```
(Microphone) → Arduino ADC → Serial → Python
Python → STT → LLM → TTS → Arduino → Audio PWM → Speaker
```

---

## 🧠 AI Pipeline

1. **Record audio** from analog mic on Arduino
2. **Stream raw samples** to Python via serial
3. Python runs **Google STT**
4. Send transcription to **Azure GPT-4o Mini (or FLAN-T5)**
5. Generate natural language reply
6. Convert reply to speech using **gTTS / Azure TTS / Coqui**
7. Python sends PCM audio back to Arduino
8. Arduino plays through **PWM → PAM8302A → Speaker**

---

# 📂 Project Structure

```
project/
│
├── arduino/
│   ├── firmware.ino      # ADC sampling & PWM audio output
│   └── audio_pwm.cpp
│
├── python/
│   ├── bridge.py         # Serial bridge between Arduino & Python
│   ├── stt_google.py     # Google Speech-to-Text
│   ├── llm_azure.py      # Azure GPT-4o Mini inference
│   ├── tts_gtts.py       # gTTS-based TTS
│   └── utils/
│
├── docs/
│   ├── schematic.png     # Your Altium schematic
│   └── architecture.png  # System architecture diagram
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/l-krrish/AURA
cd AURA
```

---

## 2. Python Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.\.venv\Scripts\activate    # Windows
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Keys

Create a file: `python/config.py`

```python
AZURE_ENDPOINT = "https://therapy-bot.openai.azure.com/"
AZURE_API_KEY = "<your key>"
AZURE_DEPLOYMENT = "gpt-4o-mini"
AZURE_API_VERSION = "2024-08-01-preview"

GOOGLE_CREDENTIALS_JSON = "path/to/google/creds.json"
```

---

## 5. Upload Arduino Firmware

* Open `firmware.ino` in Arduino IDE / Arduino CLI
* Select **Arduino UNO R4 Minima**
* Upload to board

---

# ▶️ Usage

1. Connect Arduino (COM7 or your port)
2. Start Python bridge:

```bash
python python/bridge.py
```

3. When the bot prints:

```
AI Therapy Bot Ready.
Recording...
```

Speak into the microphone.

The bot will:

* Capture audio
* Transcribe
* Generate AI response
* Play waveform through speaker

---

# 🎤 Audio Pipeline Details

### Record from microphone:

* Arduino samples at **6.5 kHz**
* Resolution: **12-bit ADC**
* Serial burst transfer to Python

### Play audio:

* Arduino reconstructs audio using **high-frequency PWM**
* D9 → PAM8302A → 4Ω/8Ω speaker

---

# 🔒 Power Notes

* **Microphone must run on 3.3V** for noise performance
* **Amplifier must run on 5V** for maximum volume
* Add a 100–220 µF bulk capacitor on the 5V rail if using USB power + loud audio

---

# 🚀 Features

* Real-time STT → AI → TTS pipeline
* Python + Arduino hybrid architecture
* Non-blocking serial data streaming
* Hardware-accurate audio path
* Noise-free analog microphone input
* Natural voice output (WaveNet, gTTS, Coqui, etc.)
* Designed for therapy, comfort responses, conversational UX

---

# 📈 Future Improvements

* Wake-word detection (“AURA”)
* Noise suppression + AGC
* ESP32-S3 standalone version with onboard I2S mic
* Local quantized LLM (Q4_0 / Q8_0)
* Multi-modal camera input
* Emotion detection via voice tone

---

# 👤 Author

**Krrish Lala**
Waterloo Computer Engineering

* GitHub: [https://github.com/l-krrish](https://github.com/l-krrish)
* LinkedIn: [https://www.linkedin.com/in/krrish-lala/](https://www.linkedin.com/in/krrish-lala/)

---
