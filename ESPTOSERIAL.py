import serial
import numpy as np
from scipy.io.wavfile import write
import time

PORT = "COM6"
BAUD = 115200
RATE = 4000
SECONDS = 5

ser = serial.Serial(PORT, BAUD, timeout=0.1)
samples = []

start_time = time.time()
while time.time() - start_time < SECONDS:
    if ser.in_waiting >= 2:
        data = ser.read(2)
        val = int.from_bytes(data, 'little')
        samples.append(val)

ser.close()

# convert to signed PCM
samples = np.array(samples, dtype=np.float32)
samples = (samples - 2048) / 2048.0
samples = np.int16(samples * 32767)

write("recording.wav", RATE, samples)
print(f"Saved recording.wav ({len(samples)} samples)")
