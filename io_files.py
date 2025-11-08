# io_files.py
import csv
from config import TARGETS_FILE, NFZS_FILE, DRONES_FILE

def load_multi_starts():
    starts = []
    with open(DRONES_FILE, "r") as f:
        for row in csv.reader(f):
            starts.append((int(row[0]), int(row[1])))
    return starts


def load_targets():
    targets = []
    with open(TARGETS_FILE, "r") as f:
        for row in csv.reader(f):
            targets.append((int(row[0]), int(row[1])))
    return targets


def load_nfzs():
    nfzs = []
    with open(NFZS_FILE, "r") as f:
        for row in csv.reader(f):
            nfzs.append((int(row[0]), int(row[1]), int(row[2]), int(row[3])))
    return nfzs

