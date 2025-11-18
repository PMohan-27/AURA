import serial
import numpy as np
import resampy
from scipy.io.wavfile import write
import time
# --------------------------
# Configuration
# --------------------------
PORT = "COM3"
BAUD = 921600
SECONDS = 5
TARGET_RATE = 10000  # Target sample rate for STT

# --------------------------
# Read from Arduino
# --------------------------
ser = serial.Serial(PORT, BAUD, timeout=0.1)
samples = []

print("Recording...")
start_time = time.time()
while time.time() - start_time < SECONDS:
    if ser.in_waiting >= 2:
        data = ser.read(2)
        val = int.from_bytes(data, 'little')
        samples.append(val)
ser.close()
print("Finished recording.")

# --------------------------
# Convert to signed PCM
# --------------------------
samples = np.array(samples, dtype=np.float32)
samples = (samples - 2048) / 2048.0        # center around 0
samples = samples.astype(np.float32)

# --------------------------
# Estimate actual sample rate
# --------------------------
actual_rate = len(samples) / SECONDS
print("Actual Arduino sample rate:", actual_rate)

# --------------------------
# Resample to target rate using Resampy
# --------------------------
resampled = resampy.resample(samples, sr_orig=actual_rate, sr_new=TARGET_RATE)

# Scale to 16-bit PCM for saving
resampled_int16 = np.int16(resampled * 32767)

# --------------------------
# Save WAV (optional)
# --------------------------
write("resampled_resampy.wav", TARGET_RATE, resampled_int16)
print(f"Saved resampled_resampy.wav at {TARGET_RATE} Hz")
