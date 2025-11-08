# io_files.py
import csv
from config import START_FILE, TARGETS_FILE, NFZS_FILE


def load_start_pos():
    """Reads drone.csv and returns (row, col). If anything fails, return (0,0)."""
    try:
        with open(START_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                # Expect: row,col
                parts = [x.strip() for x in row if x.strip() != ""]
                if len(parts) == 2:
                    return int(parts[0]), int(parts[1])

        print("⚠️  drone.csv is empty or not formatted correctly. Using default (0,0).")
        return (0, 0)

    except:
        print("⚠️  Could not read drone.csv. Using default (0,0).")
        return (0, 0)


def load_targets():
    """Reads targets.csv and returns a list of (row, col). If problem, returns empty list."""
    targets = []
    try:
        with open(TARGETS_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                joined = "".join(row).strip()
                if joined == "" or joined.startswith("#"):
                    continue

                parts = [x.strip() for x in row if x.strip() != ""]
                if len(parts) == 2:
                    targets.append((int(parts[0]), int(parts[1])))

    except:
        print("⚠️  Could not read targets.csv. No targets loaded.")

    return targets


def load_nfzs():
    """Reads nfzs.csv and returns list of rectangles (r1,c1,r2,c2)."""
    nfzs = []
    try:
        with open(NFZS_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                joined = "".join(row).strip()
                if joined == "" or joined.startswith("#"):
                    continue

                parts = [x.strip() for x in row if x.strip() != ""]
                if len(parts) == 4:
                    nfzs.append((int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])))

    except:
        print("⚠️  Could not read nfzs.csv. No NFZs loaded.")

    return nfzs

