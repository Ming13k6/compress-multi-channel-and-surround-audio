import numpy as np
import matplotlib.pyplot as plt
import zlib
import os

from audio_io import load_audio, save_audio
from transform import pca_decorrelation
from compressor import compress_data, decompress_data
from coupling import mdct_coupling, plot_mdct_spectrum
from metrics import compute_compression_ratio, compute_snr
from analysis import split_channels, compute_correlation_matrix, plot_correlation_heatmap
from residual import compute_residual, reconstruct_from_residual, residual_analysis
from mdct import mdct, imdct
#load audio
data, sr = load_audio("../data/test.wav")

print("Sample rate:", sr)
print("Shape:", data.shape)

#phan tich kenh
channels = split_channels(data)
print("Number of channels:", len(channels))

corr_before = compute_correlation_matrix(data)

print("Correlation BEFORE:")
print(corr_before)

plot_correlation_heatmap(corr_before)

###########################
#      ENCODE             #
###########################

#PCA
transformed, eigvecs, mean = pca_decorrelation(data)
corr_pca = compute_correlation_matrix(transformed)

print("Correlation AFTER PCA:")
print(corr_pca)

plot_correlation_heatmap(corr_pca)
#chứng minh PCA orthogonal
energy_before = np.sum(data**2)
energy_after = np.sum(transformed**2)

print("Energy difference (PCA):", abs(energy_before - energy_after))

def run_pipeline(data, sr, use_pca=True):
    print("\n==============================")
    print("PIPELINE:", "WITH PCA" if use_pca else "WITHOUT PCA")
    print("==============================")

    if use_pca:
        transformed, eigvecs, mean = pca_decorrelation(data)
    else:
        transformed = data.copy()
        eigvecs = np.eye(data.shape[1])
        mean = np.zeros_like(data[0])
        print("SNR:", snr)
    print("Compression ratio:", cr)

    return snr, cr  

#MDCT per channel
channels_mdct = []
scales = []

for i in range(transformed.shape[1]):
    ch = transformed[:, i]

    m = np.max(np.abs(ch))
    scales.append(m if m > 0 else 1)

    ch_norm = ch / m if m > 0 else ch

    coeffs = mdct(ch_norm)
    channels_mdct.append(coeffs)

scales = np.array(scales)

# coupling
X_coupled, freqs = mdct_coupling(channels_mdct, sr)
print("X_coupled shape:", X_coupled.shape)

#avg spectrum
before_avg = np.mean(np.abs(channels_mdct[0]), axis=0)
after_avg = np.mean(np.abs(X_coupled[:,:,0]), axis=0)

plot_mdct_spectrum(
    freqs,
    before_avg,
    after_avg,
    "MDCT Spectrum (Average)"
)

#stack các channel để xử lý đa kênh
combined_mdct = np.transpose(X_coupled, (0, 2, 1)).astype(np.float32)

#residual
residual = compute_residual(combined_mdct)
residual_flat = residual.flatten()
residual_analysis(combined_mdct, residual)
print("Residual shape:", residual.shape)

#histogram dùng sample
plt.figure()
plt.hist(residual_flat, bins=100, density=True)
plt.title("Residual Distribution (Zoomed)")
plt.xlim(-0.1, 0.1)
plt.show()

residual_flat = residual.flatten()
residual_flat = residual_flat[:50000]

#nén
compressed, meta = compress_data(residual, qbits=15, deadzone=1e-5)
print("Compressed size:", len(compressed))

###########################
#    DECODE               #
###########################

#reconstruct
residual_decoded = decompress_data(compressed, meta)
reconstructed_res = reconstruct_from_residual(residual_decoded)
reconstructed_mdct = np.transpose(reconstructed_res, (0, 2, 1))
print("reconstructed_mdct shape:", reconstructed_mdct.shape)

#inverse MDCT
channels_time = []

num_channels = X_coupled.shape[2]

for i in range(num_channels):
    coeffs = reconstructed_mdct[:, :, i]

    recon = imdct(coeffs)

    #restore scale
    recon = recon * scales[i]

    channels_time.append(recon)

#ghép thành tín hiệu đa kênh time-domain
combined_time = np.stack(channels_time, axis=1)
print("combined_time shape:", combined_time.shape)

#inverse PCA
reconstructed = combined_time @ eigvecs.T + mean

#align length
min_len = min(len(data), len(reconstructed))
reconstructed_eval = reconstructed[:min_len]
data_eval = data[:min_len]

#tính SNR trên tín hiệu chưa clip
snr = compute_snr(data_eval, reconstructed_eval)
print("SNR (FULL PIPELINE):", snr)

reconstructed = np.clip(reconstructed, -1, 1)

print("SNR (FULL PIPELINE):", snr)

#lưu file
save_audio("../output/reconstructed.wav", reconstructed, sr)


#metrics

#tính CR 
original_size = data.nbytes
compressed_size = len(compressed)
cr = compute_compression_ratio(original_size, compressed_size)

bitrate = (compressed_size * 8 * sr) / len(data)
bitrate_per_channel = bitrate / data.shape[1]

print("Bitrate (bps):", bitrate)
print("Bitrate per channel:", bitrate_per_channel)
print("Original size:", original_size)
print("Compressed size:", compressed_size)
print("Compression ratio:", cr)

#tính CR raw (zlib nén trực tiếp file gốc)
compressed_raw = zlib.compress(data.astype(np.float32).tobytes(), level=9)
cr_raw = compute_compression_ratio(original_size, len(compressed_raw))
print("CR Raw:", cr_raw)
print("CR PCA+MDCT+Residual:", cr)


#độ hiệu quả nén
improvement = cr / cr_raw
print("Compression improvement:", improvement)

#visualization
plt.figure()
plt.plot(data[:1000, 0])
plt.title("Channel 0 waveform")
plt.show()
snr_pca, cr_pca = run_pipeline(data, sr, use_pca=True)
snr_no_pca, cr_no_pca = run_pipeline(data, sr, use_pca=False)

print("\n========= COMPARISON =========")
print("WITH PCA  -> SNR:", snr_pca, "| CR:", cr_pca)
print("NO PCA    -> SNR:", snr_no_pca, "| CR:", cr_no_pca)
