import numpy as np
import matplotlib.pyplot as plt


#Tách band
def split_bands(M, sr, cutoff=4000):
    freqs = np.linspace(0, sr/2, M)
    low_idx = freqs <= cutoff
    high_idx = freqs > cutoff
    return low_idx, high_idx, freqs


#MDCT coupling
def mdct_coupling(channels_mdct, sr, cutoff=4000):
    X = np.stack(channels_mdct, axis=2)  
    # shape: (num_blocks, M, C)

    num_blocks, M, C = X.shape

    low_idx, high_idx, freqs = split_bands(M, sr, cutoff)

    X_coupled = X.copy()

    #xử lý từng block (quan trọng)
    for b in range(num_blocks):

        #lấy block (M, C)
        block = X[b]

        #high freq energy trung bình
        high_energy = np.median(block[high_idx], axis=1, keepdims=True)

        #apply coupling
        block_coupled = block.copy()
        block_coupled[high_idx] = np.sign(block[high_idx]) * high_energy

        X_coupled[b] = block_coupled

    return X_coupled, freqs


#Energy scaling
def energy_scaling(X):
    scale = np.max(np.abs(X), axis=(0,1), keepdims=True)
    scale[scale == 0] = 1
    return X / scale, scale


def inverse_scaling(X_scaled, scale):
    return X_scaled * scale


#Plot
def plot_mdct_spectrum(freqs, before, after, title):
    plt.figure(figsize=(8,4))
    plt.plot(freqs, np.abs(before), label="Before")
    plt.plot(freqs, np.abs(after), label="After", alpha=0.7)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.legend()
    plt.xlim(0, 8000)
    plt.show()