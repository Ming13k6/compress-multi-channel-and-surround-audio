import zlib

def compress_data(data):
    return zlib.compress(data.tobytes())
