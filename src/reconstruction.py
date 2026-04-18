from residual import reconstruct_from_residual
from compression import decompress_signal
from transform import mid_side_decode


def full_decode(compressed_M, compressed_S, dtype, shape):

    # 1. entropy decode
    M_res = decompress_signal(compressed_M, dtype, shape)
    S_res = decompress_signal(compressed_S, dtype, shape)

    # 2. residual reconstruction
    M = reconstruct_from_residual(M_res)
    S = reconstruct_from_residual(S_res)

    # 3. inverse mid/side
    L, R = mid_side_decode(M, S)

    return L, R
