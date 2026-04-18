
import zlib
import numpy as np


def compress_signal(signal):
   # Convert numpy array to bytes and compress with zlib

    byte_data = signal.tobytes()
    compressed = zlib.compress(byte_data)
    return compressed


def decompress_signal(compressed_data, dtype, shape):

    #Decompress and reshape back to numpy array

    decompressed = zlib.decompress(compressed_data)
    signal = np.frombuffer(decompressed, dtype=dtype)
    return signal.reshape(shape)