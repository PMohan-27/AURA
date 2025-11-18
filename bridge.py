import serial
import time
import numpy as np
from scipy.io.wavfile import write
import requests
import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
import tempfile

# --------------------------
# CONFIG
# --------------------------
PORT = "COM3"           # change if needed
BAUD = 115200
RATE = 8000             # 4000 Hz sample rate
SECONDS = 4             # recording duration

HF_TOKEN = "hf_your_token_here"
HUGGINGFACE_MODEL = "google/flan-t5-small"

ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(2)
print("Connected to ESP32")

recognizer = sr.Recognizer()

# --------------------------
# STEP 1: Record analog mic samples
# --------------------------
def record_audio():
    return "D:\\AURA\\AURA\\resampled_resampy.wav"
    print("Recording from ESP32 analog mic...")
    samples = []
    start_time = time.time()

    while time.time() - start_time < SECONDS:
        if ser.in_waiting >= 2:
            data = ser.read(2)
            val = int.from_bytes(data, "little")
            samples.append(val)

    if not samples:
        print("No samples received.")
        return None

    samples = np.array(samples, dtype=np.uint16)   # unsigned 16-bit

    # convert unsigned 16-bit (0–65535) → signed 16-bit (-32768 to +32767)
    samples = samples.astype(np.int32)
    samples = samples - 32768
    samples = samples.astype(np.int16)

    wav_path = "recording.wav"
    write(wav_path, RATE, samples)
    print(f"Saved {wav_path} ({len(samples)} samples)")
    return wav_path

# --------------------------
# STEP 2: Speech-to-Text
# --------------------------
def speech_to_text(wav_path):
    print("Running speech recognition...")
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("User:", text)
        return text
    except:
        return "FAIL"

# --------------------------
# STEP 3: Hugging Face Therapy Model
# --------------------------
def get_therapy_reply(text):
    if not text:
        return "I could not understand you. Please try again."

    print("Querying Hugging Face model...")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"You are a calm, friendly therapy assistant. User said: {text}\nAssistant:"
    }

    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
        json=payload,
        headers=headers,
        timeout=60
    )

    reply = resp.json()[0]["generated_text"]
    print("Bot:", reply)
    return reply

# --------------------------
# STEP 4: Convert TTS to PCM16
# --------------------------
def tts_to_pcm(text):
    print("Converting reply to speech...")
    tts = gTTS(text)
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tts.save(tmp.name)

    audio, sr_ = sf.read(tmp.name, dtype='int16')
    if audio.ndim > 1:
        audio = audio[:, 0]  # mono

    return audio.tobytes()

# --------------------------
# STEP 5: Send PCM16 audio back to ESP32
# --------------------------
def send_audio_to_esp32(pcm_data):
    print("Sending audio to ESP32...")
    chunk = 256
    for i in range(0, len(pcm_data), chunk):
        ser.write(pcm_data[i:i+chunk])
        time.sleep(0.002)
    print("Playback complete.\n")

# --------------------------
# MAIN LOOP
# --------------------------
print("AI Therapy Bot Bridge Ready.")

try:
    while True:
        wav = record_audio()
        if wav is None:
            continue

        text = speech_to_text(wav)
        print(text)
        reply = get_therapy_reply(text)
        pcm = tts_to_pcm(reply)
        send_audio_to_esp32(pcm)

except KeyboardInterrupt:
    print("Exiting.")
    ser.close()
