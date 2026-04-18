def mid_side_encode(L, R):
    M = (L + R) / 2
    S = (L - R) / 2
    return M, S
    
def mid_side_decode(M, S):
    L = M + S
    R = M - S
    return L, R