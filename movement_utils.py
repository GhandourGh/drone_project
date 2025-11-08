# movement_utils.py — minimal helpers for grid movement

import heapq
from grid_utils import in_bounds


def neighbors4(r, c):
    """Return U/D/L/R neighbors around (r, c)."""
    return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]


def valid_neighbors(r, c, nfz_mask):
    """Neighbors inside the grid and not blocked."""
    out = []
    for nr, nc in neighbors4(r, c):
        if in_bounds(nr, nc) and not nfz_mask[nr, nc]:
            out.append((nr, nc))
    return out


def manhattan(a, b):
    """Manhattan distance between cells a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# -----------------------------
# A* PATHFINDING (grid, 4-neigh)
# -----------------------------
def a_star_path(start, goal, nfz_mask):
    """
    Shortest path from start -> goal avoiding NFZs using A* (Manhattan).
    Returns [start, ..., goal] or None.
    """
    sr, sc = start
    gr, gc = goal

    if start == goal:
        return [start]
    if not (in_bounds(sr, sc) and in_bounds(gr, gc)):
        return None
    if nfz_mask[sr, sc] or nfz_mask[gr, gc]:
        return None

    # heap items: (f, g, (r, c))
    open_heap = []
    heapq.heappush(open_heap, (manhattan(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    closed = set()

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            # reconstruct
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))

        cr, cc = current
        for nbr in valid_neighbors(cr, cc, nfz_mask):
            if nbr in closed:
                continue
            tentative_g = g + 1
            if tentative_g < g_score.get(nbr, 10**12):
                came_from[nbr] = current
                g_score[nbr] = tentative_g
                fn = tentative_g + manhattan(nbr, goal)
                heapq.heappush(open_heap, (fn, tentative_g, nbr))

    return None  # unreachable


def a_star_next_step(current, target, nfz_mask):
    """Return next cell along A* path current -> target, or None."""
    if current == target:
        return None
    path = a_star_path(current, target, nfz_mask)
    if not path or len(path) < 2:
        return None
    return path[1]


# --------------------------------------
# Simple wrappers used by other modules
# --------------------------------------
def choose_step_toward(current, target, nfz_mask):
    """First step on shortest path (kept for compatibility)."""
    return a_star_next_step(current, target, nfz_mask)


def choose_step_toward_smart(current, prev, target, nfz_mask):
    """Same as choose_step_toward; prev is ignored."""
    return a_star_next_step(current, target, nfz_mask)