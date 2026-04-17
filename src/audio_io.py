import soundfile as sf
import numpy as np

def load_audio(path):
    data, sr = sf.read(path)

    if len(data.shape) == 1:
        data = data.reshape(-1, 1)
data.shape = (n_samples, n_channels)
def save_audio(path, data, sr):
    sf.write(path, data, sr)
    return data, sr
#test456