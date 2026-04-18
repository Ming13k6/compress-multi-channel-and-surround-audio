import numpy as np

#mid/side encode
def mid_side_encode(L, R):
    M = (L + R) / 2
    S = (L - R) / 2
    return M, S

#mid/side decode
def mid_side_decode(M, S):
    L = M + S
    R = M - S
    return L, R

#tinh nang luong
def compute_energy(signal):
    return np.sum(signal ** 2)

#so sanh nang luong
def energy_analysis(L, R, M, S):
    energy_lr = compute_energy(L) + compute_energy(R)
    energy_ms = compute_energy(M) + compute_energy(S)

    reduction = energy_lr - energy_ms
    ratio = energy_ms / energy_lr

    return energy_lr, energy_ms, reduction, ratio

#PCA
def pca_decorrelation(data):
    # data shape: (samples, channels)

    # center data
    mean = np.mean(data, axis=0)
    centered = data - mean

    # covariance matrix
    cov = np.cov(centered, rowvar=False)

    # eigen decomposition
    eigvals, eigvecs = np.linalg.eigh(cov)

    # sort descending
    idx = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, idx]

    # transform
    transformed = centered @ eigvecs

    return transformed, eigvecs, mean

#inverse PCA
def pca_inverse(transformed, eigvecs, mean):
    return transformed @ eigvecs.T + mean