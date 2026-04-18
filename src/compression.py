import zlib
def compress_data(data):
    return zlib.compress(data.astype(np.float32).tobytes())