import numpy as np


def temporal_predict(signal):
    """
    First-order predictor:
    x̂[n] = x[n-1]
    """
    predicted = np.zeros_like(signal)
    predicted[1:] = signal[:-1]
    return predicted


def compute_residual(signal):
    """
    e[n] = x[n] - x̂[n]
    """
    predicted = temporal_predict(signal)
    residual = signal - predicted
    return residual


def reconstruct_from_residual(residual):
    """
    Inverse of first-order prediction
    x[n] = e[n] + x[n-1]
    """
    signal = np.zeros_like(residual)
    signal[0] = residual[0]

    for n in range(1, len(residual)):
        signal[n] = residual[n] + signal[n - 1]

    return signal