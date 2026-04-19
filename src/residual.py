import numpy as np
import matplotlib.pyplot as plt

def temporal_predict(signal):
    predicted = np.zeros_like(signal)
    predicted[1:, :] = signal[:-1, :]
    return predicted


def compute_residual(signal):
    predicted = temporal_predict(signal)
    return signal - predicted


def reconstruct_from_residual(residual):
    signal = np.zeros_like(residual)
    signal[0, :] = residual[0, :]

    for n in range(1, residual.shape[0]):
        signal[n, :] = residual[n, :] + signal[n - 1, :]

    return signal


def residual_analysis(original, residual):
    var_original = np.var(original)
    var_residual = np.var(residual)

    print("Variance original:", var_original)
    print("Variance residual:", var_residual)
    print("Reduction:", var_original - var_residual)

    return var_original, var_residual


def plot_histograms(original, residual):
    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    plt.hist(original.flatten(), bins=100, density=True)
    plt.title("Original Signal Histogram")

    plt.subplot(1,2,2)
    plt.hist(residual.flatten(), bins=100, density=True)
    plt.title("Residual Histogram")

    plt.tight_layout()
    plt.show()