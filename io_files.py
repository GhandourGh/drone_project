# io_files.py — minimal, multi-drone only

import csv
from config import TARGETS_FILE, NFZS_FILE, DRONES_FILE


def _iter_clean_rows(path):
    """Yield non-empty, non-comment CSV rows as lists of strings."""
    try:
        with open(path, "r") as f:
            for row in csv.reader(f):
                joined = "".join(row).strip()
                if joined and not joined.startswith("#"):
                    yield [x.strip() for x in row if x.strip()]
    except Exception:
        return  # stay silent per minimal-output rule


def load_multi_starts(expected=None):
    """
    Read drones.csv -> [(r, c), ...]
    Pads with the first start (or (0,0)) if fewer than `expected`.
    """
    starts = []
    for parts in _iter_clean_rows(DRONES_FILE):
        if len(parts) == 2:
            try:
                starts.append((int(parts[0]), int(parts[1])))
            except ValueError:
                pass

    if expected is not None and len(starts) < expected:
        filler = starts[0] if starts else (0, 0)
        while len(starts) < expected:
            starts.append(filler)
    return starts


def load_targets():
    """Read targets.csv -> [(r, c), ...]"""
    targets = []
    for parts in _iter_clean_rows(TARGETS_FILE):
        if len(parts) == 2:
            try:
                targets.append((int(parts[0]), int(parts[1])))
            except ValueError:
                pass
    return targets


def load_nfzs():
    """Read nfzs.csv -> [(r1, c1, r2, c2), ...]"""
    nfzs = []
    for parts in _iter_clean_rows(NFZS_FILE):
        if len(parts) == 4:
            try:
                r1, c1, r2, c2 = map(int, parts[:4])
                nfzs.append((r1, c1, r2, c2))
            except ValueError:
                pass
    return nfzs

