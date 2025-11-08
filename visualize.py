# visualize.py
import matplotlib.pyplot as plt
from config import GRID_ROWS, GRID_COLS


def enable_interactive():
    """Enable interactive mode so the live plot updates."""
    plt.ion()


def begin_live_map(start, targets, nfzs):
    """Set up the plot and return a small 'state' dict you can update per step."""
    fig, ax = plt.subplots(figsize=(8, 8))

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

    base_title = "Drone Map - Live Animation"
    ax.set_title(base_title, fontsize=14, fontweight='bold')
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
        rect = plt.Rectangle(
            (left - 0.5, top - 0.5), w, h,
            fill=True, facecolor='red', alpha=0.3,
            edgecolor='darkred', linewidth=2
        )
        ax.add_patch(rect)

    # Targets (blue stars)
    if targets:
        t_rows = [r for r, _ in targets]
        t_cols = [c for _, c in targets]
        ax.scatter(
            t_cols, t_rows, s=300, c='blue', marker='*',
            label='Targets', zorder=5, edgecolors='darkblue', linewidths=2
        )

    # Trail line + moving drone dot
    line, = ax.plot([], [], 'g-', linewidth=3, label='Trail', zorder=3, alpha=0.7)
    dot,  = ax.plot([], [], 'o', color='red', markersize=15,
                    label='Drone', zorder=4, markeredgecolor='darkred', markeredgewidth=2)
    ax.legend(loc='upper right', fontsize=10)

    # Seed with start
    sr, sc = start
    xs = [sc]
    ys = [sr]
    line.set_data(xs, ys)
    dot.set_data([sc], [sr])

    # Force draw and show the initial plot
    plt.draw()
    plt.pause(0.5)  # Show initial state briefly

    # Track which targets remain to recolor when reached
    remaining_targets = set(targets) if targets else set()

    return {
        "fig": fig, "ax": ax,
        "line": line, "dot": dot,
        "xs": xs, "ys": ys,
        "remaining_targets": remaining_targets,
        "title_base": base_title,
    }


def live_draw_step(state, pos, battery=None, pause_sec=0.2):
    """Append pos to the trail and refresh the plot with animation.
       If the drone steps on a target, recolor it purple.
       If battery is provided, show it in the title."""
    r, c = pos
    state["xs"].append(c)
    state["ys"].append(r)
    state["line"].set_data(state["xs"], state["ys"])
    state["dot"].set_data([c], [r])

    # If current cell is a remaining target, mark it as reached (purple star)
    if (r, c) in state.get("remaining_targets", set()):
        state["ax"].plot(
            c, r, marker="*", markersize=18,
            color="purple", markeredgecolor="white", markeredgewidth=2,
            zorder=6
        )
        state["remaining_targets"].remove((r, c))

    # Update title with battery if available
    if battery is not None:
        state["ax"].set_title(f"{state['title_base']}  |  Battery: {battery} moves left")

    # Render and wait a bit
    plt.pause(pause_sec)


def keep_plot_open():
    """Keep the plot window open after animation completes."""
    plt.ioff()  # turn off interactive mode
    print("\n✅ Animation complete! Close the plot window to exit.")
    plt.show()  # block and keep window open