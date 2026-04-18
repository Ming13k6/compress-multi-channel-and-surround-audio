import soundfile as sf
import numpy as np

def load_audio(path):
    data, sr = sf.read(path)

    if len(data.shape) == 1:
        data = data.reshape(-1, 1)

    return data.astype(np.float32), sr


def save_audio(path, data, sr):
    sf.write(path, data, sr)