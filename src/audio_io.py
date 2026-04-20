import soundfile as sf
import numpy as np

def load_audio(path):
    data, sr = sf.read(path)

    # mono → (N,1)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    # convert float32
    data = data.astype(np.float32)

    # normalize về [-1, 1] nếu cần
    max_val = np.max(np.abs(data))
    if max_val > 1:
        data = data / max_val

    return data, sr

def save_audio(path, data, sr):
    # tránh clipping
    max_val = np.max(np.abs(data))
    if max_val > 1:
        data = data / max_val

    sf.write(path, data, sr)