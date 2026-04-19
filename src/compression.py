import zlib
import numpy as np

def compress_data(data):
    if not isinstance(data, np.ndarray):
        raise ValueError("Input must be numpy array")

    data_bytes = data.tobytes()
    compressed = zlib.compress(data_bytes)

    return compressed
def decompress_data(compressed, shape):
    import zlib
    raw = zlib.decompress(compressed)
    return np.frombuffer(raw, dtype=np.float32).reshape(shape)