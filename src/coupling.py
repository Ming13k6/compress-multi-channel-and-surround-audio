import numpy as np
import matplotlib.pyplot as plt

#Fast Fourier Transform 
def compute_fft(signal, sr):
    N = len(signal)
    spectrum = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(N, 1/sr)
    magnitude = np.abs(spectrum)
    return freqs, spectrum, magnitude


#Identify high-freq bands
def split_frequency_bands(freqs, cutoff=4000):
#cutoff: hz
    low_idx = freqs <= cutoff
    high_idx = freqs > cutoff

    return low_idx, high_idx


#Frequency coupling
def frequency_coupling(L_spec, R_spec, freqs, cutoff=4000):
    low_idx, high_idx = split_frequency_bands(freqs, cutoff)

    #high freq: average
    avg_high = (np.abs(L_spec) + np.abs(R_spec)) / 2

    #giữ phase riêng
    L_phase = np.exp(1j * np.angle(L_spec))
    R_phase = np.exp(1j * np.angle(R_spec))

    #áp coupling
    L_coupled = L_spec.copy()
    R_coupled = R_spec.copy()

    L_coupled[high_idx] = avg_high[high_idx] * L_phase[high_idx]
    R_coupled[high_idx] = avg_high[high_idx] * R_phase[high_idx]

    return L_coupled, R_coupled

#inverse FFT
def inverse_fft(spectrum):
    return np.fft.irfft(spectrum)

#Plot spectrum
def plot_spectrum(freqs, mag_before, mag_after, title):
    plt.figure(figsize=(8,4))
    plt.plot(freqs, mag_before, label="Before")
    plt.plot(freqs, mag_after, label="After", alpha=0.7)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.legend()
    plt.xlim(0, 8000)  # zoom cho dễ nhìn
    plt.show()