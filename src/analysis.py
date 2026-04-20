import numpy as np
import matplotlib.pyplot as plt

#tach kenh
def split_channels(data):
    return [data[:, i] for i in range(data.shape[1])]

#tinh correlation matrix 
def compute_correlation_matrix(data):
    corr = np.corrcoef(data.T)
    corr = np.nan_to_num(corr)
    return corr

#visualize heatmap
def plot_correlation_heatmap(corr_matrix):
    plt.imshow(corr_matrix, vmin=-1, vmax=1, cmap="coolwarm")
    plt.colorbar()
    plt.title("Channel Correlation Heatmap")

    n = corr_matrix.shape[0]
    labels = [f"Ch {i}" for i in range(n)]

    plt.xticks(range(n), labels)
    plt.yticks(range(n), labels)

    plt.xlabel("Channel")
    plt.ylabel("Channel")

    plt.show()