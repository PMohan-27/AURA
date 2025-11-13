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
PORT = "COM6"           # change if needed
BAUD = 115200
RATE = 4000             # sample rate must match ESP32 SAMPLE_RATE
SECONDS = 5             # recording duration per turn

HF_TOKEN = "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"
HUGGINGFACE_MODEL = "google/flan-t5-small"

ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(2)
print("Connected to ESP32")

recognizer = sr.Recognizer()

# --------------------------
# STEP 1: Record from analog mic via ESP32
# --------------------------
def record_audio():
  print("Recording from ESP32 analog mic...")

  samples = []
  start_time = time.time()

  while time.time() - start_time < SECONDS:
      if ser.in_waiting >= 2:
          data = ser.read(2)
          val = int.from_bytes(data, 'little')
          samples.append(val)

  if not samples:
      print("No samples received.")
      return None

  samples_arr = np.array(samples, dtype=np.float32)

  # center around 0 and scale to int16
  samples_arr = (samples_arr - 2048.0) / 2048.0
  samples_arr = np.int16(samples_arr * 32767)

  wav_path = "recording.wav"
  write(wav_path, RATE, samples_arr)
  print(f"Saved {wav_path} ({len(samples_arr)} samples)")
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
  except Exception as e:
      print("STT error:", e)
      return ""

# --------------------------
# STEP 3: Hugging Face response
# --------------------------
def get_therapy_reply(text):
  if not text:
      return "I couldn't understand you. Please try again."

  print("Querying Hugging Face...")
  headers = {"Authorization": f"Bearer {HF_TOKEN}"}
  payload = {
      "inputs": f"You are a calm, friendly therapy assistant. User: {text}\nAssistant:"
  }
  resp = requests.post(
      f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
      json=payload,
      headers=headers,
      timeout=60
  )
  data = resp.json()
  reply = data[0]["generated_text"]
  print("Bot:", reply)
  return reply

# --------------------------
# STEP 4: Text-to-Speech (gTTS → PCM)
# --------------------------
def tts_to_pcm(text):
  print("Converting reply to speech...")
  tts = gTTS(text)
  tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
  tts.save(tmp.name)

  audio, sr_ = sf.read(tmp.name, dtype='int16')
  if audio.ndim > 1:
      audio = audio[:, 0]

  return audio.tobytes()

# --------------------------
# STEP 5: Send PCM audio back to ESP32
# --------------------------
def send_audio_to_esp32(pcm_data):
  print("Sending audio to ESP32...")
  chunk = 256
  for i in range(0, len(pcm_data), chunk):
      ser.write(pcm_data[i:i+chunk])
      time.sleep(0.002)
  print("Done playback.\n")

# --------------------------
# MAIN LOOP
# --------------------------
print("AI therapy bridge (analog mic version) ready.")

try:
  while True:
      wav = record_audio()
      if wav is None:
          continue
      text = speech_to_text(wav)
      reply = get_therapy_reply(text)
      pcm = tts_to_pcm(reply)
      send_audio_to_esp32(pcm)

except KeyboardInterrupt:
  print("Exiting.")
  ser.close()
