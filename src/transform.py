import numpy as np

def pca_decorrelation(data):
    # center
    mean = np.mean(data, axis=0)
    centered = data - mean

    # covariance
    cov = np.cov(centered, rowvar=False)

    # eigen decomposition
    eigvals, eigvecs = np.linalg.eigh(cov)

    # sort descending
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    # numerical stability (optional)
    eigvals = np.maximum(eigvals, 0)

    # transform
    transformed = centered @ eigvecs

    return transformed, eigvecs, mean


def pca_inverse(transformed, eigvecs, mean):
    return transformed @ eigvecs.T + mean