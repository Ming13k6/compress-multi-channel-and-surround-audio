import numpy as np
import matplotlib.pyplot as plt

from audio_io import load_audio
from transform import mid_side_encode
from compression import compress_data
from metrics import compute_compression_ratio
from analysis import split_channels, compute_correlation_matrix, plot_correlation_heatmap
#load audio
data, sr = load_audio("data/test.wav")

print("Sample rate:", sr)
print("Shape:", data.shape)

#phan tich kenh
from analysis import split_channels, compute_correlation_matrix, plot_correlation_heatmap

channels = split_channels(data)
print("Number of channels:", len(channels))

corr_matrix = compute_correlation_matrix(data)

print("Correlation matrix:")
print(corr_matrix)

plot_correlation_heatmap(corr_matrix)

plt.xticks(range(corr_matrix.shape[0]))
plt.yticks(range(corr_matrix.shape[0]))
#xu li kenh
if data.shape[1] == 1:
    print("Mono audio detected")
    L = data[:, 0]
    R = data[:, 0]
else:
    L = data[:, 0]
    R = data[:, 1]

#transform mid/side
mid, side = mid_side_encode(L, R)

combined = np.stack([mid, side], axis=1)

#correlation sau Mid/Side
combined = np.stack([mid, side], axis=1)
corr_after = compute_correlation_matrix(combined)

print("Correlation after Mid/Side:")
print(corr_after)

#nén
compressed = compress_data(combined)

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