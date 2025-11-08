# movement_utils.py
# Simple helper functions for movement (no OOP)

import random
import heapq
from itertools import count
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


# -----------------------------
# A* PATHFINDING (grid, 4-neigh)
# -----------------------------

def a_star_path(start, goal, nfz_mask):
    """
    Compute a path from start -> goal avoiding NFZs using A* with Manhattan heuristic.
    Returns a list of cells [start, ..., goal] if reachable; otherwise None.
    """
    sr, sc = start
    gr, gc = goal

    # If start/goal invalid or blocked, bail quickly
    if not in_bounds(sr, sc) or not in_bounds(gr, gc):
        return None
    if nfz_mask[sr, sc] or nfz_mask[gr, gc]:
        return None
    if start == goal:
        return [start]

    # Open set as heap of (f, g, tie, (r,c))
    open_heap = []
    tie = count()  # ensures deterministic ordering for ties
    g_score = {start: 0}
    f_start = manhattan(start, goal)
    heapq.heappush(open_heap, (f_start, 0, next(tie), start))

    came_from = {}
    closed = set()

    while open_heap:
        f, g, _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        cr, cc = current
        for nbr in valid_neighbors(cr, cc, nfz_mask):
            if nbr in closed:
                continue
            tentative_g = g + 1  # unit cost per step
            if tentative_g < g_score.get(nbr, 10**12):
                came_from[nbr] = current
                g_score[nbr] = tentative_g
                f_nbr = tentative_g + manhattan(nbr, goal)
                heapq.heappush(open_heap, (f_nbr, tentative_g, next(tie), nbr))

    # Unreachable
    return None


def a_star_next_step(current, target, nfz_mask):
    """
    Return the next cell to step to along the A* path from current -> target.
    Returns None if no path exists or we're already at the target.
    """
    if current == target:
        return None
    path = a_star_path(current, target, nfz_mask)
    if not path or len(path) < 2:
        return None
    # path[0] == current, so next step is:
    return path[1]


# --------------------------------------
# Backward-compat wrappers (used by main)
# --------------------------------------

def choose_step_toward(current, target, nfz_mask):
    """
    Legacy greedy function kept for compatibility.
    Here we simply call A* and return the first step on the shortest path.
    """
    return a_star_next_step(current, target, nfz_mask)


def choose_step_toward_smart(current, prev, target, nfz_mask):
    """
    Smart chooser used by navigator: now purely A* (prev is ignored).
    Returns the first step along the A* path; None if unreachable or already there.
    """
    return a_star_next_step(current, target, nfz_mask)