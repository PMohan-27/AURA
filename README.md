# 🌟 **AURA — Arduino + AI Voice Therapy Bot**

*A compact, voice-activated AI companion built using the Arduino UNO R4, custom analog audio front-end, and a single Python backend (`bridge.py`).*

AURA listens through an analog microphone, streams audio into a Python backend for **STT → AI → TTS**, and plays natural speech through a Class-D amplifier.

This repository includes **hardware**, **firmware**, **Python backend**, and **3D-printable shell CAD** for a complete end-to-end build.

---

# 📦 **Repository Structure**

```
AURA/
│
├── AURA_ARDUINO/             # PlatformIO firmware project
│   ├── src/main.cpp
│   ├── include/
│   ├── lib/
│   ├── test/
│   ├── .vscode/
│   └── platformio.ini
│
├── bridge.py                 # Single backend Python file (STT → LLM → TTS)
│
├── docs/
│   ├── schematic.pdf         # Full electronics schematic
│   ├── architecture.png      # System architecture diagram
│   └── CAD/
│       ├── AURA Shell UPPER.stl
│       └── AURA Shell LOWER.stl
│
├── resampled_resampy.wav     # Debug sample output
├── README.md
└── .gitignore
```

---

# 🧩 **Hardware Overview**

AURA uses:

* **Arduino UNO R4 Minima**
* **SEN0487 Analog Electret Microphone**
* **PAM8302A Class-D Audio Amplifier**
* **Single-ended mic input (AC-coupled)**
* **High-frequency PWM speaker output**
* **Custom 3D-printed enclosure**

---

## 🔌 **Hardware Block Diagram**

```
 Mic → Arduino ADC → Serial → bridge.py →
 Google STT → Azure GPT-4o Mini → TTS →
 Arduino PWM → PAM8302 → Speaker
```

---

# 🔧 **Electronics Wiring (Matches Your Schematic)**

## 🎤 Microphone → Arduino

| SEN0487 Pin | Arduino Pin | Notes                                 |
| ----------- | ----------- | ------------------------------------- |
| OUT         | A0 (MIC_IN) | Through 10 µF capacitor (AC coupling) |
| VCC         | 3.3V        | Mic power                             |
| GND         | GND         | Common ground                         |

---

## 🔊 Arduino → PAM8302 Amplifier → Speaker

| Arduino Pin  | PAM8302 Pin | Purpose          |
| ------------ | ----------- | ---------------- |
| D9 (SPK_OUT) | A+          | PWM audio signal |
| GND          | A-          | Ground           |
| 5V           | VIN         | Amplifier power  |
| GND          | GND         | Power ground     |

Additional components used:

* **C1 = 10 µF** (audio smoothing)
* **R1 = 10k** (pull-down resistor for stable PWM idle)

---

# 📘 **Schematic & CAD Files**

### 🔧 Electronics Schematic

`docs/schematic.pdf`

### 🧱 3D Printable Shell

Located in `docs/CAD/`:

* `AURA Shell UPPER.stl`
* `AURA Shell LOWER.stl`

---

# 💻 **Firmware (Arduino / PlatformIO)**

The Arduino code lives inside **`AURA_ARDUINO/`** and is built using **PlatformIO** (not Arduino IDE).

---

### 📁 **Firmware Structure**

```
AURA_ARDUINO/
│
├── src/main.cpp            # Main firmware logic
├── include/
├── lib/
├── test/
├── .vscode/
└── platformio.ini
```

---

### 🧠 **Firmware Responsibilities**

`main.cpp` handles:

* ADC sampling of microphone at ~6.5 kHz
* Serial streaming of raw audio frames to Python
* Receiving PCM audio from Python
* Reconstructing audio via **high-frequency PWM** on D9
* Synchronizing with Python's `bridge.py`

---

### ▶️ **Building the Firmware**

From inside `AURA_ARDUINO/`:

```bash
pio run
pio run --target upload
```

Or use VSCode PlatformIO:

* ✔ Build
* ✔ Upload
* ✔ Serial Monitor

---

### ⚙ PlatformIO Config (Expected)

```ini
[env:uno_r4_minima]
platform = renesas-ra
board = uno_r4_minima
framework = arduino
monitor_speed = 921600
```

---

# 🧠 **Python Backend (bridge.py)**

The entire AI pipeline runs through one Python script.

### Pipeline:

```
Audio → STT → GPT-4o Mini → TTS → Audio Playback
```

### Features inside `bridge.py`:

* Serial connection to Arduino
* Audio buffer and noise preprocessing
* **Google STT**
* **Azure GPT-4o Mini** 
* **gTTS**
* WAV → PCM conversion
* Sending PCM packets to Arduino

---

# ⚙ **Setup Instructions**

### 1. Clone repo

```bash
git clone https://github.com/l-krrish/AURA
cd AURA
```

### 2. Create Python environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys (inside `bridge.py`)

```python
AZURE_ENDPOINT = "https://therapy-bot.openai.azure.com/"
AZURE_API_KEY = "<your key>"
AZURE_DEPLOYMENT = "gpt-4o-mini"
GOOGLE_CREDENTIALS = "credentials.json"
```

### 5. Upload firmware

Inside `AURA_ARDUINO/`:

```bash
pio run --target upload
```

---

# ▶️ **Running AURA**

```bash
python bridge.py
```

You should see:

```
Connected to Arduino on COM7
AI Therapy Bot Ready.
Recording...
```

Speak → AURA replies → audio plays.

---

# 🚀 **Features**

* Real-time conversational feedback
* GPT-4o Mini reasoning
* Hardware-accurate PWM audio
* Full schematic + CAD for reproducibility
* Single-file backend for simplicity
* Custom enclosure design

---

# 🧪 **Future Improvements**

* Wake-word activation
* Noise reduction filters
* ESP32-S3 upgrade
* Local quantized LLM support
* LED expressions + servo motion

---

# 👤 **Authors & Contributors**

### **Krrish Lala**

*Waterloo Computer Engineering*
[![](https://img.shields.io/badge/GitHub-l--krrish-black?logo=github)](https://github.com/l-krrish)
[![](https://img.shields.io/badge/LinkedIn-Krrish%20Lala-blue?logo=linkedin)](https://linkedin.com/in/krrish-lala)

---

### **Parasinder Mohan**

*Waterloo Computer Engineering*
[![](https://img.shields.io/badge/GitHub-PMohan--27-black?logo=github)](https://github.com/PMohan-27)
[![](https://img.shields.io/badge/LinkedIn-Parasinder%20Mohan-blue?logo=linkedin)](https://www.linkedin.com/in/parasinder-mohan/)

---

### **Luca Seaman**

*Waterloo Computer Engineering*
[![](https://img.shields.io/badge/GitHub-LucaSeaman-black?logo=github)](https://github.com/LucaSeaman)
[![](https://img.shields.io/badge/LinkedIn-Luca%20Seaman-blue?logo=linkedin)](https://www.linkedin.com/in/luca-seaman/)

---
Just tell me!
