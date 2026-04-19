import numpy as np
#tính CR
def compute_compression_ratio(original, compressed):
    return original / compressed if compressed > 0 else float("inf")

#tính SNR
def compute_snr(original, reconstructed):
    original = original.flatten()
    reconstructed = reconstructed.flatten()

    noise = original - reconstructed
    num = np.sum(original**2)
    den = np.sum(noise**2)

    return 10 * np.log10(num / den) if den > 0 else float("inf")