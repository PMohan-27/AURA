import serial
import time
import numpy as np
import soundfile as sf
import requests
from gtts import gTTS
import speech_recognition as sr
import tempfile
import io
  
ESP32_PORT = "COM5"       
BAUD_RATE = 115200

HF_TOKEN = "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"
HUGGINGFACE_MODEL = "google/flan-t5-small"

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
RECORD_SECONDS = 4  


ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("✅ Connected to ESP32")

recognizer = sr.Recognizer()



def read_audio_from_esp32(duration=RECORD_SECONDS):
    
    print(f" Recording {duration}s from ESP32 mic...")
    raw_data = bytearray()
    start_time = time.time()
    while time.time() - start_time < duration:
        if ser.in_waiting:
            chunk = ser.read(ser.in_waiting)
            raw_data.extend(chunk)

    audio = np.frombuffer(raw_data, dtype=np.int32) >> 14
    audio = np.clip(audio, -32768, 32767).astype(np.int16)

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio, SAMPLE_RATE)
    print(f"Saved temp audio: {tmp.name}")
    return tmp.name

def speech_to_text(wav_path):

    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🧍 You: {text}")
            return text
        except sr.UnknownValueError:
            print("⚠️ Could not understand.")
            return ""
        except Exception as e:
            print("⚠️ STT Error:", e)
            return ""

def therapy_reply(user_text):
   
    if not user_text:
        return "Sorry, I didn’t catch that. Could you repeat?"
    print(" Thinking...")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": f"You are a kind therapy assistant. User: {user_text}\nAssistant:"}
    try:
        resp = requests.post(
            f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
            headers=headers, json=payload, timeout=60)
        reply = resp.json()[0]["generated_text"]
        print(f"🧠 Bot: {reply}")
        return reply
    except Exception as e:
        print("⚠️ Hugging Face Error:", e)
        return "I'm having trouble thinking right now."

def text_to_speech(reply_text):

    print("🎙️ Converting to speech...")
    tts = gTTS(reply_text, lang="en")
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tts.save(tmp.name)
    data, fs = sf.read(tmp.name, dtype='int16')
    if fs != 22050:
        data = sf.resample(data, SAMPLE_RATE, fs)
    if data.ndim > 1:
        data = data[:, 0]
    pcm_data = data.tobytes()
    return pcm_data

def send_audio_to_esp32(pcm_data):
    
    print("Sending audio to ESP32...")
    chunk_size = 512
    for i in range(0, len(pcm_data), chunk_size):
        ser.write(pcm_data[i:i+chunk_size])
        time.sleep(0.005)
    print("Done streaming.\n")


print("Therapy Bot Bridge ready! Press Ctrl+C to stop.\n")

while True:
    try:
        wav = read_audio_from_esp32()
        user_text = speech_to_text(wav)
        if user_text:
            reply = therapy_reply(user_text)
            pcm = text_to_speech(reply)
            send_audio_to_esp32(pcm)
    except KeyboardInterrupt:
        print("\nExiting gracefully.")
        break
    except Exception as e:
        print("Error:", e)
