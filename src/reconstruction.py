import numpy as np
from transform import mid_side_decode

def reconstruct_from_ms(M, S):
    L, R = mid_side_decode(M, S)
    return np.stack([L, R], axis=1)
