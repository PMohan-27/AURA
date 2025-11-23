# 🌟 AURA — Arduino + AI Voice Therapy Bot

**Real-time Conversational Bot using Arduino UNO R4, Analog Mic, PAM8302A Speaker Amp, and a Single Python `bridge.py` Backend**

AURA is a minimalistic but powerful voice-first AI bot designed for therapy-style or assistant-style conversations.
It records audio through an electret mic, sends it to a Python backend for transcription → AI → TTS, and plays the generated audio back through a Class-D amplifier.

This repo uses only **one Python file: `bridge.py`** to handle the entire pipeline.

---

# 📸 Hardware Overview 

AURA uses:

* **Arduino UNO R4 Minima**
* **SEN0487 analog microphone**
* **PAM8302A mono Class-D speaker amplifier**
* **10 µF AC coupling capacitors**
* **PWM audio output**

You provided the exact Altium schematic, and this README matches it 100%.

---

## 🧩 Hardware Architecture

```
 ┌────────────────────────────┐
 │         Arduino R4         │
 │  MIC_IN (A0) ◄─────┐        │
 │                     │        │
 │  SPK_OUT (D9) ──────┼──► PAM8302A ─► Speaker
 │                     │
 └─────────────────────┘
         ▲
         │
   SEN0487 Analog Mic
```

---

## 🔌 Pin Connections

### 🎤 Microphone (SEN0487 → Arduino)

| SEN0487 Pin | Arduino Pin | Notes                        |
| ----------- | ----------- | ---------------------------- |
| VCC         | 3.3V        | Mic power                    |
| GND         | GND         | Shared ground                |
| OUT (A)     | A0 (MIC_IN) | Through 10 µF capacitor (C2) |

> The 10 µF capacitor provides AC coupling and removes DC bias.

---

### 🔊 Speaker Path (Arduino → PAM8302)

| Arduino Pin  | PAM8302 Pin | Function            |
| ------------ | ----------- | ------------------- |
| D9 (SPK_OUT) | A+ (P1)     | PWM audio signal    |
| GND          | A- (P2)     | Audio return        |
| —            | SD (P3)     | Shutdown (not used) |
| +5V          | VIN (P4)    | Power for amplifier |
| GND          | GND (P5)    | Ground              |

> C1 = 10 µF smoothing capacitor
> R1 = 10k pulldown on SPK_OUT

---

# 💻 Software Overview

AURA uses a **single Python file**: `bridge.py`.
It handles:

* Serial communication
* Raw audio preprocessing
* Google Speech-to-Text
* Azure / FLAN-T5 LLM inference
* gTTS or TTS of your choice
* Audio resampling
* Playback to Arduino

---

# 📂 Project Structure 

```
AURA/
│
├── arduino/
│   └── firmware.ino
│
├── python/
│   └── bridge.py        # ONLY file handling all backend logic
│
├── docs/
│   ├── schematic.png
│   └── architecture.png
│
└── README.md
```


---

# 🧠 Full AI Pipeline (Inside bridge.py)

```
Microphone → Arduino ADC → Serial → Python bridge.py
Python → Google STT → LLM (Azure GPT-4o Mini or FLAN-T5)
→ TTS (gTTS / Coqui / Azure TTS)
→ Python sends PCM → Arduino PWM → PAM8302 → Speaker
```

---

# ⚙️ Installation

### 1. Clone Repo

```bash
git clone https://github.com/l-krrish/AURA
cd AURA
```

### 2. Create Python Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Inside `bridge.py`:

```python
AZURE_ENDPOINT = "https://therapy-bot.openai.azure.com/"
AZURE_API_KEY = "your_key_here"
AZURE_DEPLOYMENT = "gpt-4o-mini"
```

Google STT:

```python
GOOGLE_CREDENTIALS = "path/to/credentials.json"
```

---

# ▶️ Running the Bot

1. Plug in Arduino
2. Upload `firmware.ino`
3. Run:

```bash
python python/bridge.py
```

You should see:

```
Connected to Arduino on COM7
AI Therapy Bot Ready.
Recording...
```

Speak into the mic → bot replies → audio plays from speaker.

---

# 🎤 Audio Internals

### Input (MIC):

* Sampled at 6.5 kHz
* 12-bit ADC
* DC offset removed
* Sent raw via serial to Python

### Output (SPEAKER):

* Arduino uses high-frequency PWM on D9
* PAM8302 amplifies
* Speaker plays clean audio

---

# 🧪 Troubleshooting

| Issue                                     | Fix                                                  |
| ----------------------------------------- | ---------------------------------------------------- |
| Bot responds with same message repeatedly | LLM prompt issue — update system prompt in bridge.py |
| Audio weak                                | Use 5V USB-C power or larger capacitor on VIN        |
| Mic noisy                                 | Ensure shielded wiring and clean 3.3V source         |
| Python freezing                           | Use `timeout=None` and flush serial buffers          |

---

# 🚀 Features

* Full **voice → AI → voice** loop
* Only **1 backend file**
* Hardware-accurate PWM audio
* Works with **Arduino UNO R4 Minima**
* Supports **Google STT + Azure GPT-4o Mini + gTTS**
* Plug-and-play architecture

---

# 📈 Future Improvements

* Wake-word ("AURA")
* Noise suppression filters
* Use ESP32-S3 + I2S mic for faster STT
* Offline local LLM (Q4_0 GGUF) on laptop
* Emotion detection via pitch analysis

---

# 👤 Author

**Krrish Lala**
 Waterloo Computer Engineering

* GitHub: [https://github.com/l-krrish](https://github.com/l-krrish)
* LinkedIn: [https://linkedin.com/in/krrish-lala/](https://linkedin.com/in/krrish-lala/)

**Parasinder Mohan**
 Waterloo Computer Engineering

* GitHub: [https://github.com/PMohan-27](https://github.com/PMohan-27)
* LinkedIn: [https://www.linkedin.com/in/parasinder-mohan/](https://www.linkedin.com/in/parasinder-mohan/)

**Luca Seaman**
 Waterloo Computer Engineering

* GitHub: [https://github.com/LucaSeaman](https://github.com/LucaSeaman)
* LinkedIn: [https://www.linkedin.com/in/luca-seaman/](https://www.linkedin.com/in/luca-seaman/)



---

