import numpy as np


def sine_window(N):
    n = np.arange(N)
    return np.sin(np.pi / N * (n + 0.5))


def mdct(signal, M=512):
   
    N = 2 * M
    hop = M

    #padding để signal chia hết các block
    pad = (N - len(signal) % hop) % hop
    signal = np.concatenate([signal, np.zeros(pad)])

    window = sine_window(N)

    blocks = []
    for i in range(0, len(signal) - N + 1, hop):
        block = signal[i:i+N] * window

        n = np.arange(N)
        k = np.arange(M)

        cos_term = np.cos(
            np.pi / M * (n[:, None] + 0.5 + M/2) * (k + 0.5)
        )

        coeffs = block @ cos_term
        blocks.append(coeffs)

    return np.array(blocks)


def imdct(mdct_coeffs, M=512):
    num_blocks = mdct_coeffs.shape[0]
    N = 2 * M
    hop = M

    window = sine_window(N)

    output_len = (num_blocks - 1) * hop + N
    signal = np.zeros(output_len)

    n = np.arange(N)
    k = np.arange(M)

    cos_term = np.cos(
        np.pi / M * (n[:, None] + 0.5 + M/2) * (k + 0.5)
    )

    for i in range(num_blocks):
        block = cos_term @ mdct_coeffs[i]
        block = block * (2 / M)  # scale
        block = block * window

        start = i * hop
        signal[start:start+N] += block

    return signal