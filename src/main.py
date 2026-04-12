import numpy as np
import zlib
from audio_io import load_audio

data, sr = load_audio("data/test.wav")

if data.shape[1] == 1:
    L = data[:,0]
    R = data[:,0]
else:
    L = data[:,0]
    R = data[:,1]

mid = (L + R) / 2
side = (L - R) / 2

combined = np.stack([mid, side], axis=1)

compressed = zlib.compress(combined.tobytes())

print("Sample rate:", sr)
print("Original size:", data.nbytes)
print("Compressed size:", len(compressed))
