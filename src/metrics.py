import numpy as np
#ti le nen
def compute_compression_ratio(original, compressed):
    return original / compressed
#SNR
def compute_snr(original, reconstructed):
    noise = original - reconstructed
    num = np.sum(original**2)
    den = np.sum(noise**2)
    return 10 * np.log10(num / den) if den > 0 else float("inf")
