# grid_utils.py
import numpy as np
from config import GRID_ROWS, GRID_COLS

def in_bounds(r, c):
    """True if (r,c) lies inside the grid."""
    return 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS

def build_nfz_mask(nfzs):
    """Boolean mask (rows x cols) where True means blocked."""
    mask = np.zeros((GRID_ROWS, GRID_COLS), dtype=bool)
    for r1, c1, r2, c2 in nfzs:
        rt, rb = sorted((max(0, r1), max(0, r2)))
        cl, cr = sorted((max(0, c1), max(0, c2)))
        rt = min(rt, GRID_ROWS - 1)
        rb = min(rb, GRID_ROWS - 1)
        cl = min(cl, GRID_COLS - 1)
        cr = min(cr, GRID_COLS - 1)
        mask[rt:rb+1, cl:cr+1] = True
    return mask

def check_start_and_targets(start, targets, nfz_mask):
    """
    Return (fixed_start, filtered_targets) with no printing.
    - Start is set to (0,0) if out-of-bounds or inside an NFZ.
    - Targets are kept only if in-bounds (NFZ handling is done later).
    """
    sr, sc = start
    if not in_bounds(sr, sc) or nfz_mask[sr, sc]:
        fixed_start = (0, 0)
    else:
        fixed_start = start

    filtered = [(r, c) for (r, c) in targets if in_bounds(r, c)]
    return fixed_start, filtered