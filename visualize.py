# visualize.py — multi-drone only (clean & simple)

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from config import GRID_ROWS, GRID_COLS


def enable_interactive():
    plt.ion()


def _battery_layout_positions(n):
    """Normalized (x, y) positions for n battery labels under the plot."""
    if n <= 0:
        return []
    y = 0.02
    if n == 1:
        return [(0.5, y)]
    xs = [0.1 + i * (0.8 / (n - 1)) for i in range(n)]
    return [(x, y) for x in xs]


def begin_live_map_multi(drone_starts, targets, nfzs):
    """Set up multi-drone plot and return a state dict."""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Grid
    ax.set_xlim(-0.5, GRID_COLS - 0.5)
    ax.set_ylim(-0.5, GRID_ROWS - 0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xticks(range(GRID_COLS))
    ax.set_yticks(range(GRID_ROWS))
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.5)
    ax.set_title("Multi-Drone Animation")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Rows")

    # NFZ rectangles
    for (r1, c1, r2, c2) in nfzs:
        top, left = min(r1, r2), min(c1, c2)
        bot, right = max(r1, r2), max(c1, c2)
        rect = plt.Rectangle(
            (left - 0.5, top - 0.5),
            right - left + 1, bot - top + 1,
            facecolor="#e53935", alpha=0.25,
            edgecolor="#b71c1c", linewidth=2
        )
        ax.add_patch(rect)

    # Targets
    remaining_targets = set()
    if targets:
        t_rows = [r for r, _ in targets]
        t_cols = [c for _, c in targets]
        ax.scatter(t_cols, t_rows, s=300, c="#1976d2", marker="*",
                   zorder=5, edgecolors="#0d47a1", linewidths=2)
        remaining_targets = set(targets)

    # Drone lines/dots (cycle colors if needed)
    palette = [
        ("#e53935", "#b71c1c"),
        ("#43a047", "#1b5e20"),
        ("#fbc02d", "#795548"),
        ("#8e24aa", "#4a148c"),
        ("#1976d2", "#0d47a1"),
        ("#ffb300", "#f57c00"),
    ]
    drones = []
    legend_handles = [
        Patch(facecolor="#e53935", edgecolor="#b71c1c", alpha=0.25, label="NFZ"),
        Line2D([0], [0], marker="*", linestyle="None",
               markerfacecolor="#1976d2", markeredgecolor="#0d47a1",
               markersize=12, label="Targets")
    ]

    for i, (sr, sc) in enumerate(drone_starts):
        lc, ec = palette[i % len(palette)]
        line, = ax.plot([], [], "-", lw=3, color=lc, alpha=0.9, label=f"Drone {i+1}")
        dot,  = ax.plot([], [], "o", ms=14, color=lc, markeredgecolor=ec, markeredgewidth=2)
        line.set_data([sc], [sr])
        dot.set_data([sc], [sr])
        drones.append({"xs": [sc], "ys": [sr], "line": line, "dot": dot})
        legend_handles.append(Line2D([0], [0], color=lc, lw=3, label=f"Drone {i+1}"))

    ax.legend(handles=legend_handles, loc="upper left", bbox_to_anchor=(1.04, 1),
              fontsize=10, frameon=True)

    plt.draw()
    plt.pause(0.2)

    # Per-drone battery labels (under the plot)
    battery_texts = []
    for i, (x, y) in enumerate(_battery_layout_positions(len(drone_starts))):
        battery_texts.append(fig.text(x, y, f"Drone {i+1} Battery: —",
                                      ha="center", va="bottom", fontsize=10))

    return {
        "fig": fig, "ax": ax,
        "drones": drones,
        "remaining_targets": remaining_targets,
        "battery_texts": battery_texts,
    }


def live_draw_step_multi(state, drone_index, pos, battery=None, pause_sec=0.02):
    """Update one drone’s trail/dot and battery label; mark reached targets."""
    r, c = pos
    d = state["drones"][drone_index]

    d["xs"].append(c)
    d["ys"].append(r)
    d["line"].set_data(d["xs"], d["ys"])
    d["dot"].set_data([c], [r])

    if (r, c) in state["remaining_targets"]:
        state["ax"].plot(c, r, marker="*", markersize=16, color="#8e24aa",
                         markeredgecolor="white", markeredgewidth=2, zorder=6)
        state["remaining_targets"].remove((r, c))

    if battery is not None and 0 <= drone_index < len(state["battery_texts"]):
        state["battery_texts"][drone_index].set_text(f"Drone {drone_index+1} Battery: {battery}")

    plt.pause(pause_sec)


def keep_plot_open():
    plt.ioff()
    print("\n✅ Animation complete! Close the window to exit.")
    plt.show()