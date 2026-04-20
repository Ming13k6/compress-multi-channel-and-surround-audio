import zlib
import numpy as np


def compress_data(data, qbits=12, deadzone=1e-3):
    if not isinstance(data, np.ndarray):
        raise ValueError("Input must be numpy array")

    data = data.astype(np.float32).copy()

    #dead-zone
    data[np.abs(data) < deadzone] = 0.0

    #scale riêng từng channel để giữ chất lượng
    max_abs = np.max(np.abs(data), axis=(0, 2), keepdims=True)
    max_abs[max_abs < 1e-8] = 1.0

    qmax = (2 ** (qbits - 1)) - 1  # ví dụ 12 bits -> 2047
    scale = qmax / max_abs

    quantized = np.round(data * scale)
    quantized = np.clip(quantized, -qmax, qmax).astype(np.int16)

    compressed = zlib.compress(quantized.tobytes(), level=9)

    meta = {
        "shape": data.shape,
        "qbits": qbits,
        "scale_inv": (1.0 / scale).astype(np.float32),
        "deadzone": deadzone,
    }
    return compressed, meta


def decompress_data(compressed, meta):
    raw = zlib.decompress(compressed)

    shape = tuple(meta["shape"])
    quantized = np.frombuffer(raw, dtype=np.int16).reshape(shape)

    scale_inv = meta["scale_inv"].astype(np.float32)
    reconstructed = quantized.astype(np.float32) * scale_inv
    return reconstructed