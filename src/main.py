import numpy as np
import matplotlib.pyplot as plt

from audio_io import load_audio, save_audio
from transform import pca_decorrelation
from compression import compress_data, decompress_data
from coupling import mdct_coupling, plot_mdct_spectrum
from metrics import compute_compression_ratio, compute_snr
from analysis import split_channels, compute_correlation_matrix, plot_correlation_heatmap
from residual import compute_residual, reconstruct_from_residual, residual_analysis
from mdct import mdct, imdct
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

###########################
#      ENCODE             #
###########################

#PCA
transformed, eigvecs, mean = pca_decorrelation(data)

#chứng minh PCA orthogonal
energy_before = np.sum(data**2)
energy_after = np.sum(transformed**2)

print("Energy difference (PCA):", abs(energy_before - energy_after))

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

#coupling
X_coupled, freqs = mdct_coupling(channels_mdct, sr)

plot_mdct_spectrum(freqs, channels_mdct[0], X_coupled[:,0],
                   "MDCT Spectrum Before vs After Coupling")

#residual
residual = compute_residual(combined_mdct)

residual_analysis(combined_mdct, residual)

#histogram dùng sample
plt.figure()
plt.hist(residual_flat, bins=100, density=True)
plt.title("Residual Distribution (Zoomed)")
plt.xlim(-0.1, 0.1)
plt.show()

residual_flat = residual.flatten()
residual_flat = residual_flat[:50000]

#nén
compressed = compress_data(residual)

###########################
#    DECODE               #
###########################

#reconstruct
residual_decoded = decompress_data(compressed, residual.shape)
reconstructed_res = reconstruct_from_residual(residual_decoded)

#inverse MDCT
channels_time = []

for i in range(X_coupled.shape[1]):
    recon = imdct(X_coupled[:, i])

    # restore scale
    recon = recon * scales[i]

    channels_time.append(recon)

combined_mdct = np.stack(channels_time, axis=1)
 




#inverse PCA
reconstructed = reconstructed_res @ eigvecs.T + mean

#align length
min_len = min(len(data), len(reconstructed))
snr = compute_snr(data[:min_len], reconstructed[:min_len])

print("SNR (FULL PIPELINE):", snr)

#lưu file
save_audio("output/reconstructed.wav", reconstructed, sr)


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
compressed_raw = compress_data(data)
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
