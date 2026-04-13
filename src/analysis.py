import numpy as np
import matplotlib.pyplot as plt

#tach kenh
def split_channels(data):
    return [data[:, i] for i in range(data.shape[1])]

#tinh correlation matrix 
def compute_correlation_matrix(data):
    # data shape: (samples, channels)
    return np.corrcoef(data.T)

#visualize heatmap
def plot_correlation_heatmap(corr_matrix):
    plt.imshow(corr_matrix)
    plt.colorbar()
    plt.title("Channel Correlation Heatmap")
    plt.xlabel("Channel")
    plt.ylabel("Channel")
    plt.show()
