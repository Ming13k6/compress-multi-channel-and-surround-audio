import numpy as np
import matplotlib.pyplot as plt

from audio_io import load_audio
from transform import mid_side_encode, mid_side_decode, energy_analysis, pca_decorrelation
from compression import compress_data
from coupling import compute_fft, frequency_coupling, plot_spectrum, inverse_fft
from metrics import compute_compression_ratio, compute_snr
from analysis import split_channels, compute_correlation_matrix, plot_correlation_heatmap
from reconstruction import reconstruct_from_ms
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
plot_correlation_heatmap(corr_ms)
#decode check
L_rec, R_rec = mid_side_decode(mid, side)

error = np.mean((L - L_rec)**2 + (R - R_rec)**2)
print("Reconstruction error:", error)

#PCA decorrelation
transformed, eigvecs, mean = pca_decorrelation(data)

corr_pca = compute_correlation_matrix(transformed)

print("Correlation AFTER PCA:")
print(corr_pca)
plot_correlation_heatmap(corr_pca)
#metric so sanh correlation
def off_diag_mean(corr):
    return np.mean(np.abs(corr - np.eye(corr.shape[0])))

print("Off-diagonal correlation:")
print("Before:", off_diag_mean(corr_before))
print("Mid/Side:", off_diag_mean(corr_ms))
print("PCA:", off_diag_mean(corr_pca))


#chuẩn hóa
def normalize(x):
    m = np.max(np.abs(x))
    return x / m if m > 0 else x

mid = normalize(mid)
side = normalize(side)

#FFT
freqs, M_spec, _ = compute_fft(mid, sr)
_, S_spec, _ = compute_fft(side, sr)

#high-freq coupling
M_coupled, S_coupled = frequency_coupling(M_spec, S_spec, freqs)
# Energy check (optional nhưng nên giữ)

high_energy_before = np.sum(np.abs(M_spec[freqs > 4000])**2)
high_energy_after = np.sum(np.abs(M_coupled[freqs > 4000])**2)

print("High-frequency energy BEFORE:", high_energy_before)
print("High-frequency energy AFTER:", high_energy_after)

# Inverse FFT

M_time = inverse_fft(M_coupled)
S_time = inverse_fft(S_coupled)

combined_coupled = np.stack([M_time, S_time], axis=1)

# reconstruct từ Mid/Side sau coupling
reconstructed = reconstruct_from_ms(M_time, S_time)

snr = compute_snr(data, reconstructed)

print("SNR:", snr)
plot_spectrum(freqs, np.abs(M_spec), np.abs(M_coupled),
            "Mid Channel Spectrum Before vs After Coupling")
#nén
compressed = compress_data(combined_coupled)

#metrics
original_size = data.nbytes
compressed_size = len(compressed)

cr = compute_compression_ratio(original_size, compressed_size)

print("Original size:", original_size)
print("Compressed size:", compressed_size)
print("Compression ratio:", cr)

#so sánh với pipeline chỉ Mid/Side
compressed_ms = compress_data(combined_ms)

cr_ms = compute_compression_ratio(original_size, len(compressed_ms))
cr_coupled = compute_compression_ratio(original_size, compressed_size)

print("CR Mid/Side:", cr_ms)
print("CR Coupling:", cr_coupled)

#visualization
plt.plot(data[:1000, 0])
plt.title("Channel 0 waveform")
plt.show()
