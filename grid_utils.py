# grid_utils.py
import numpy as np
from config import GRID_ROWS, GRID_COLS

def in_bounds(r, c):
    return 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS

def build_nfz_mask(nfzs):
    """Return a boolean mask (rows x cols) where True means blocked."""
    mask = np.zeros((GRID_ROWS, GRID_COLS), dtype=bool)
    for r1, c1, r2, c2 in nfzs:
        rt = min(r1, r2)
        rb = max(r1, r2)
        cl = min(c1, c2)
        cr = max(c1, c2)
        rt = max(0, min(rt, GRID_ROWS - 1))
        rb = max(0, min(rb, GRID_ROWS - 1))
        cl = max(0, min(cl, GRID_COLS - 1))
        cr = max(0, min(cr, GRID_COLS - 1))
        mask[rt:rb+1, cl:cr+1] = True
    return mask

def check_start_and_targets(start, targets, nfz_mask):
    """Print simple warnings; return (fixed_start, filtered_targets)."""
    sr, sc = start
    fixed_start = start

    if not in_bounds(sr, sc):
        print(f"⚠️  Start {start} is out of bounds. Using (0,0).")
        fixed_start = (0, 0)

    elif nfz_mask[sr, sc]:
        print(f"⚠️  Start {start} is inside an NFZ. Using nearest free cell (0,0) fallback.")
        fixed_start = (0, 0)

    filtered = []
    for i, (r, c) in enumerate(targets, start=1):
        if not in_bounds(r, c):
            print(f"⚠️  Target #{i} {(r,c)} out of bounds. Skipping.")
            continue
        if nfz_mask[r, c]:
            print(f"⚠️  Target #{i} {(r,c)} is inside an NFZ. Keeping it for now (the mover will try to navigate around).")
        filtered.append((r, c))

    if not filtered:
        print("⚠️  No valid targets found. You can add lines like '9,9' to data/targets.csv.")
    return fixed_start, filtered