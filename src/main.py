import numpy as np
import matplotlib.pyplot as plt

from audio_io import load_audio
from transform import mid_side_encode, mid_side_decode, energy_analysis, pca_decorrelation
from compression import compress_data
from coupling import compute_fft, frequency_coupling, plot_spectrum, inverse_fft
from metrics import compute_compression_ratio
from analysis import split_channels, compute_correlation_matrix, plot_correlation_heatmap
#load audio
data, sr = load_audio("data/test.wav")

print("Sample rate:", sr)
print("Shape:", data.shape)

#phan tich kenh

channels = split_channels(data)
print("Number of channels:", len(channels))

corr_before = compute_correlation_matrix(data)

print("Correlation BEFORE:")
print(corr_before)

plot_correlation_heatmap(corr_before)

#xu li kenh
if data.shape[1] == 1:
    print("Mono audio detected")
    L = data[:, 0]
    R = data[:, 0]
else:
    L = data[:, 0]
    R = data[:, 1]

#mid/side encode
mid, side = mid_side_encode(L, R)

combined_ms = np.stack([mid, side], axis=1)

#phan tich nang luong
energy_lr, energy_ms, reduction, ratio = energy_analysis(L, R, mid, side)

print("Energy (L+R):", energy_lr)
print("Energy (M+S):", energy_ms)
print("Energy reduction:", reduction)
print("Energy ratio:", ratio)

#correlation sau Mid/Side 
corr_ms = compute_correlation_matrix(combined_ms)

print("Correlation AFTER Mid/Side:")
print(corr_ms)
#mid/side decode
L_rec, R_rec = mid_side_decode(mid, side)

error = np.mean((L - L_rec)**2 + (R - R_rec)**2)
print("Reconstruction error:", error)

#PCA decorrelation
transformed_pca, eigvecs, mean = pca_decorrelation(data)

corr_pca = compute_correlation_matrix(transformed_pca)

print("Correlation AFTER PCA:")
print(corr_pca)
#metric so sanh correlation
def off_diag_mean(corr):
    return np.mean(np.abs(corr - np.eye(corr.shape[0])))

print("Off-diagonal correlation:")
print("Before:", off_diag_mean(corr_before))
print("Mid/Side:", off_diag_mean(corr_ms))
print("PCA:", off_diag_mean(corr_pca))

#FFT
freqs, M_spec, _ = compute_fft(mid, sr)
_, S_spec, _ = compute_fft(side, sr)

#high-freq coupling
M_coupled, S_coupled = frequency_coupling(M_spec, S_spec, freqs)
# Energy check (optional nhưng nên giữ)

high_energy_before = np.sum(np.abs(L_spec[freqs > 4000])**2)
high_energy_after = np.sum(np.abs(L_coupled[freqs > 4000])**2)

print("High-frequency energy BEFORE:", high_energy_before)
print("High-frequency energy AFTER:", high_energy_after)

# Inverse FFT

M_time = inverse_fft(M_coupled)
S_time = inverse_fft(S_coupled)

combined_coupled = np.stack([M_time, S_time], axis=1)
#nén
compressed = compress_data(combined_coupled)

#metrics
original_size = data.nbytes
compressed_size = len(compressed)

cr = compute_compression_ratio(original_size, compressed_size)

print("Original size:", original_size)
print("Compressed size:", compressed_size)
print("Compression ratio:", cr)

#visualization
plt.plot(data[:1000, 0])
plt.title("Channel 0 waveform")
plt.show()
