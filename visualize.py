# visualize.py
import matplotlib.pyplot as plt
from config import GRID_ROWS, GRID_COLS


def enable_interactive():
    """Enable interactive mode so the live plot updates outside the Plots pane."""
    plt.ion()


def begin_live_map(start, targets, nfzs):
    """Set up the plot and return a small 'state' dict you can update per step."""
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.ion()  # ensure interactive mode is on

    # Axes & grid styling (cell-like grid)
    ax.set_xlim(-0.5, GRID_COLS - 0.5)
    ax.set_ylim(-0.5, GRID_ROWS - 0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xticks(range(GRID_COLS))
    ax.set_yticks(range(GRID_ROWS))
    ax.set_xticks([x - 0.5 for x in range(GRID_COLS + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(GRID_ROWS + 1)], minor=True)
    ax.grid(True, which="major", linestyle="-", linewidth=1, alpha=0.35, color="#b5b5b5")
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.18)
    ax.set_title("Drone Map (live)")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Rows")
    ax.set_facecolor("#f9faff")
    for spine in ax.spines.values():
        spine.set_color("#b8c6d2")
        spine.set_linewidth(1.2)

    # Draw NFZs (semi-transparent red blocks)
    for (r1, c1, r2, c2) in nfzs:
        top, left = min(r1, r2), min(c1, c2)
        bot, right = max(r1, r2), max(c1, c2)
        w = right - left + 1
        h = bot - top + 1
        rect = plt.Rectangle((left - 0.5, top - 0.5), w, h, fill=True, alpha=0.2, edgecolor='r')
        ax.add_patch(rect)

    # Targets (blue)
    if targets:
        t_rows = [r for r, _ in targets]
        t_cols = [c for _, c in targets]
        ax.scatter(t_cols, t_rows, s=60, label='Targets')

    # Trail line + moving dot
    line, = ax.plot([], [], linewidth=2, label='Trail')
    dot,  = ax.plot([], [], marker='o', markersize=10, label='Drone', linestyle='None')
    ax.legend(loc='upper right')

    # Seed with start
    sr, sc = start
    xs = [sc]
    ys = [sr]
    line.set_data(xs, ys)
    dot.set_data([sc], [sr])

    # Show initial state with pause
    plt.pause(0.5)

    return {"fig": fig, "ax": ax, "line": line, "dot": dot, "xs": xs, "ys": ys}


def live_draw_step(state, pos, pause_sec=0.08):
    """Append pos to the trail and refresh the plot."""
    r, c = pos
    state["xs"].append(c)
    state["ys"].append(r)
    state["line"].set_data(state["xs"], state["ys"])
    state["dot"].set_data([c], [r])

    # Use plt.pause for proper display updates
    plt.pause(pause_sec)


def keep_plot_open():
    """Keep the plot window open after animation completes."""
    plt.ioff()  # turn off interactive mode
    print("\n✅ Animation complete! Close the plot window to exit.")
    plt.show()  # block and keep window open