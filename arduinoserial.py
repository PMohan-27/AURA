import serial
import numpy as np
from scipy.io.wavfile import write
import time

# --------------------------
# Configuration
# --------------------------
PORT = "COM3"        # Change to your Arduino port
BAUD = 115200        # Must match Arduino Serial.begin()
RATE = 8000          # Audio sample rate (Hz)
SECONDS = 5          # How long to record

# --------------------------
# Open serial port
# --------------------------
ser = serial.Serial(PORT, BAUD, timeout=0.1)
samples = []

start_time = time.time()
print("Recording...")

while time.time() - start_time < SECONDS:
    # wait until we have 2 bytes for one sample
    if ser.in_waiting >= 2:
        data = ser.read(2)
        # convert little-endian bytes to integer
        val = int.from_bytes(data, 'little')
        samples.append(val)

ser.close()
print("Finished recording.")

# --------------------------
# Convert to signed PCM
# --------------------------
samples = np.array(samples, dtype=np.float32)
# center around 0 (-1 to 1)
samples = (samples - 2048) / 2048.0
# scale to 16-bit PCM
samples = np.int16(samples * 32767)

# --------------------------
# Save WAV file
# --------------------------
write("recording.wav", RATE, samples)
print(f"Saved recording.wav ({len(samples)} samples)")
