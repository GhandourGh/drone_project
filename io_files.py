# io_files.py
import csv
from config import TARGETS_FILE, NFZS_FILE, DRONES_FILE


def _clean_int_row(row, expected_len):
    # Join to check for blank / comment
    joined = "".join(row).strip()
    if not joined or joined.startswith("#"):
        return None

    # Keep non-empty cells
    parts = [x.strip() for x in row if x.strip()]
    if len(parts) < expected_len:
        return None

    try:
        values = [int(x) for x in parts[:expected_len]]
    except ValueError:
        return None

    return tuple(values)


def load_multi_starts():
    starts = []
    with open(DRONES_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            cleaned = _clean_int_row(row, expected_len=2)
            if cleaned is not None:
                r, c = cleaned
                starts.append((r, c))
        return starts


def load_targets():

    targets = []
    with open(TARGETS_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            cleaned = _clean_int_row(row, expected_len=2)
            if cleaned is not None:
                r, c = cleaned
                targets.append((r, c))
    return targets


def load_nfzs():
    """Read NFZ rectangles -> [(r1, c1, r2, c2), ...] with basic cleaning."""
    nfzs = []
    with open(NFZS_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            cleaned = _clean_int_row(row, expected_len=4)
            if cleaned is not None:
                r1, c1, r2, c2 = cleaned
                nfzs.append((r1, c1, r2, c2))
    return nfzs

