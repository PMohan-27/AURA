import serial
import time
import numpy as np
import soundfile as sf
import requests
from gtts import gTTS
import speech_recognition as sr
import tempfile

# --------------------------
# CONFIG
# --------------------------
ESP32_PORT = "COM5"       # change as needed
BAUD = 115200
SAMPLE_RATE = 16000
RECORD_SECONDS = 10

HF_TOKEN = "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"
HUGGINGFACE_MODEL = "google/flan-t5-small"

ser = serial.Serial(ESP32_PORT, BAUD, timeout=1)
time.sleep(2)
print("Connected to ESP32")

recognizer = sr.Recognizer()

# --------------------------
# STEP 1: Record audio from ESP32
# --------------------------
def record_audio():
    print("Recording from ESP32...")
    raw_bytes = bytearray()
    start = time.time()

    while time.time() - start < RECORD_SECONDS:
        if ser.in_waiting:
            raw_bytes.extend(ser.read(ser.in_waiting))

    # Buffer alignment fix for int32 samples
    extra = len(raw_bytes) % 4
    if extra != 0:
        raw_bytes = raw_bytes[:-extra]

    data32 = np.frombuffer(raw_bytes, dtype=np.int32)
    data16 = (data32 >> 14).astype(np.int16)

    wav_path = "input.wav"
    sf.write(wav_path, data16, SAMPLE_RATE)
    print("Saved:", wav_path)
    return wav_path

# --------------------------
# STEP 2: Speech recognition
# --------------------------
def speech_to_text(wav_path):
    print("Running STT...")
    with sr.AudioFile(wav_path) as src:
        audio = recognizer.record(src)
    try:
        text = recognizer.recognize_google(audio)
        print("User:", text)
        return text
    except:
        return ""

# --------------------------
# STEP 3: Hugging Face therapy response
# --------------------------
def get_therapy_reply(text):
    if not text:
        return "I couldn't understand you. Please repeat."

    print("Hugging Face generating response...")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"You are a calm, friendly therapy assistant. User: {text}\nAssistant:"
    }

    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
        json=payload,
        headers=headers
    )

    reply = resp.json()[0]["generated_text"]
    print("Bot:", reply)
    return reply

# --------------------------
# STEP 4: Text-to-speech
# --------------------------
def tts_to_pcm(text):
    print("Converting response to speech...")
    tts = gTTS(text)
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tts.save(tmp.name)

    audio, sr = sf.read(tmp.name, dtype='int16')
    if audio.ndim > 1:
        audio = audio[:, 0]

    return audio.tobytes()

# --------------------------
# STEP 5: Send audio back to ESP32
# --------------------------
def send_audio_to_esp32(pcm_data):
    print("Sending audio to ESP32...")
    chunk = 256
    for i in range(0, len(pcm_data), chunk):
        ser.write(pcm_data[i:i+chunk])
        time.sleep(0.002)
    print("Playback complete\n")

# --------------------------
# MAIN LOOP
# --------------------------
print("AI Therapy Bot Bridge Ready")

while True:
    try:
        wav = record_audio()
        text = speech_to_text(wav)
        reply = get_therapy_reply(text)
        pcm = tts_to_pcm(reply)
        send_audio_to_esp32(pcm)

    except KeyboardInterrupt:
        print("Exiting.")
        break
