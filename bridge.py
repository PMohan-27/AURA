import serial
import time
import numpy as np
from scipy.io.wavfile import write
import requests
import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
import tempfile
import resampy
# --------------------------
# CONFIG
# --------------------------
PORT = "COM3"           # change if needed
BAUD = 921600   
RATE = 6500             
SECONDS = 5             # recording duration
TARGET_RATE = 15000
NUM_SAMPLES = 26000
AZURE_ENDPOINT = "https://therapy-bot.openai.azure.com/"   # <-- CHANGE THIS
AZURE_API_KEY = "ExLr27WBO13n6Hkzki6sPk6pa9z3htoUHUIWI5vwBfqehlI2ZxozJQQJ99BKACHYHv6XJ3w3AAABACOG1TzC"                            # <-- CHANGE THIS
AZURE_DEPLOYMENT = "gpt-4o-mini"                           # <-- CHECK THIS
AZURE_API_VERSION = "2024-08-01-preview"


ser = serial.Serial(PORT, BAUD, timeout=0.1)
ser.reset_input_buffer()
ser.reset_output_buffer()

# time.sleep(2)
print("Connected to Arduino")

recognizer = sr.Recognizer()

# --------------------------
# STEP 1: Record analog mic samples
# --------------------------
def record_audio():
    samples = []

    print("Recording...")
    ser.reset_input_buffer()
    ser.write(b'R')  # send handshake

    while len(samples) < NUM_SAMPLES:
        if ser.in_waiting >= 2:
            data = ser.read(2)
            val = int.from_bytes(data, 'little')
            samples.append(val)

    print("Finished recording.")

    # Convert to float PCM centered around 0
    samples = np.array(samples, dtype=np.float32)
    samples -= np.mean(samples)
    samples /= np.max(np.abs(samples))

    # Resample to target rate
    resampled = resampy.resample(samples, sr_orig=6500, sr_new=TARGET_RATE)

    # Convert to int16 PCM
    resampled_int16 = np.int16(resampled * 32767)

    write("resampled_resampy.wav", TARGET_RATE, resampled_int16)
    print(f"Saved resampled_resampy.wav at {TARGET_RATE} Hz")

    return "resampled_resampy.wav"


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
# STEP 3: Azure gpt-o4-mini Therapy module
# --------------------------
def get_therapy_reply(text):
    if not text:
        return "I could not understand you. Please try again."

    print("Querying Azure GPT-4o-mini...")

    url = (
        f"{AZURE_ENDPOINT}"
        f"openai/deployments/{AZURE_DEPLOYMENT}/chat/completions"
        f"?api-version={AZURE_API_VERSION}"
    )

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY,
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a calm, supportive, friendly therapy assistant."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "max_tokens": 80,
        "temperature": 0.7,
    }

    resp = requests.post(url, json=payload, headers=headers)

    if resp.status_code != 200:
        print("Azure Error:", resp.text)
        return "I'm having trouble right now, please try again."

    data = resp.json()
    reply = data["choices"][0]["message"]["content"]
    print("Bot:", reply)
    return reply




# --------------------------
# STEP 4: Convert TTS to PCM16
# --------------------------
def tts_to_pcm(text):
    print("Converting reply to speech...")
    tts = gTTS(text,lang="en", tld="com.au")
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tts.save(tmp.name)

    audio, sr_ = sf.read(tmp.name, dtype='float32')
    if audio.ndim > 1:
        audio = audio[:, 0]  # mono
        
    resampled = resampy.resample(audio, sr_orig=sr_,sr_new=TARGET_RATE)

    # Clip to avoid overshoot
    resampled = np.clip(resampled, -1.0, 1.0)

    # Convert to int16 PCM
    pcm_int16 = (resampled * 32767).astype(np.int16)
    print(sr_)
    return pcm_int16.tobytes()

# --------------------------
# STEP 5: Send PCM16 audio back to ESP32
# --------------------------
def send_audio_to_arduino(pcm_data):
    print("Sending audio to Arduino...")

    # Step 1: Send handshake byte 'P'
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write(b'P')

    # Step 2: Send 4-byte little-endian length (number of int16 samples)
    num_samples = len(pcm_data) // 2
    ser.write(num_samples.to_bytes(4, byteorder='little'))

    # Step 3: Send PCM16 data in chunks to avoid overflowing the serial buffer
    chunk_size = 256
    for i in range(0, len(pcm_data), chunk_size):
        ser.write(pcm_data[i:i+chunk_size])
        time.sleep(0.002)  # small delay for stability

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
        send_audio_to_arduino(pcm)

except KeyboardInterrupt:
    exit()
    print("Exiting.")
    ser.close()
