# movement_utils.py
# Simple helper functions for movement (no OOP)

import random
from grid_utils import in_bounds


def neighbors4(r, c):
    """
    Return the four U/D/L/R neighbor cells around (r, c)
    in this fixed order: Up, Down, Left, Right.
    """
    return [
        (r - 1, c),  # Up
        (r + 1, c),  # Down
        (r, c - 1),  # Left
        (r, c + 1),  # Right
    ]


def valid_neighbors(r, c, nfz_mask):
    """
    Keep only neighbors that are inside the grid and not blocked by NFZ.
    nfz_mask is a boolean numpy array where True means blocked.
    """
    nbrs = neighbors4(r, c)
    ok = []
    for nr, nc in nbrs:
        if in_bounds(nr, nc) and not nfz_mask[nr, nc]:
            ok.append((nr, nc))
    return ok


def manhattan(a, b):
    """Return Manhattan distance between cells a=(r1,c1) and b=(r2,c2)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def choose_step_toward(current, target, nfz_mask):
    """
    From current (r, c), look at valid U/D/L/R neighbors and pick the one
    with the smallest Manhattan distance to target. If multiple neighbors tie,
    pick randomly among them. Return None if no valid neighbors exist.
    """
    r, c = current
    nbrs = valid_neighbors(r, c, nfz_mask)
    if not nbrs:
        return None

    # Compute distances and choose the minimum; break ties randomly
    distances = [(nbr, manhattan(nbr, target)) for nbr in nbrs]
    min_d = min(d for _, d in distances)
    best_candidates = [nbr for nbr, d in distances if d == min_d]
    return random.choice(best_candidates)

def choose_step_toward_smart(current, prev, target, nfz_mask):
    """
    Like choose_step_toward, but avoids immediately returning to `prev`
    (the last cell) unless there is no other valid option.
    """
    r, c = current
    nbrs = valid_neighbors(r, c, nfz_mask)
    if not nbrs:
        return None

    # Prefer neighbors that are NOT the previous cell
    if prev is not None:
        nbrs_pref = [n for n in nbrs if n != prev]
        if nbrs_pref:
            nbrs = nbrs_pref  # use filtered list

    # Greedy by Manhattan distance; break ties randomly
    distances = [(nbr, manhattan(nbr, target)) for nbr in nbrs]
    min_d = min(d for _, d in distances)
    best_candidates = [nbr for nbr, d in distances if d == min_d]
    return random.choice(best_candidates)