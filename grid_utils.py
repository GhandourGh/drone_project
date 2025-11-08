# grid_utils.py
import numpy as np
from config import GRID_ROWS, GRID_COLS

def in_bounds(r, c):
    return 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS

def build_nfz_mask(nfzs):
    mask = np.zeros((GRID_ROWS, GRID_COLS), dtype=bool)
    for r1, c1, r2, c2 in nfzs:
        mask[r1:r2+1, c1:c2+1] = True
    return mask
