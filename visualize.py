import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from config import GRID_ROWS, GRID_COLS

def enable_interactive():
    plt.ion()

def _battery_layout_positions(n):
    if n <= 0:
        return []
    y = 0.035
    if n == 1:
        return [(0.5, y)]
    xs = [0.2 + i * (0.6 / (n - 1)) for i in range(n)]
    return [(x, y) for x in xs]

def begin_live_map_multi(drone_starts, targets, nfzs):
    plt.style.use('seaborn-v0_8-white')
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#fafafb')
    ax.set_facecolor('#f9f9fb')

    ax.set_xlim(-0.5, GRID_COLS - 0.5)
    ax.set_ylim(-0.5, GRID_ROWS - 0.5)
    ax.set_xticks(range(GRID_COLS))
    ax.set_yticks(range(GRID_ROWS))
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.tick_params(axis='both', which='major', labelsize=12, length=3)
    ax.grid(True, linestyle='-', linewidth=0.15, alpha=0.25)

    ax.set_title("Multi-Drone Map", fontsize=17, fontweight='normal', pad=14)
    ax.set_xlabel("Columns", fontsize=12, labelpad=7)
    ax.set_ylabel("Rows", fontsize=12, labelpad=7)

    for (r1, c1, r2, c2) in nfzs:
        top, left = min(r1, r2), min(c1, c2)
        bot, right = max(r1, r2), max(c1, c2)
        rect = plt.Rectangle(
            (left - 0.5, top - 0.5),
            right - left + 1, bot - top + 1,
            facecolor="#ef9a9a", alpha=0.13,
            edgecolor="#b71c1c", linewidth=1.25
        )
        ax.add_patch(rect)

    remaining_targets = set()
    if targets:
        t_rows = [r for r, _ in targets]
        t_cols = [c for _, c in targets]
        ax.scatter(t_cols, t_rows, s=180, c="#1976d2", marker="*",
                   zorder=5, edgecolors="#0d47a1", linewidths=1.2)
        remaining_targets = set(targets)

    palette = [
        ("#E57373", "#B71C1C"),
        ("#81C784", "#388E3C"),
        ("#FFD54F", "#FBC02D"),
        ("#BA68C8", "#4A148C"),
        ("#64B5F6", "#1976D2"),
        ("#FFA726", "#F57C00"),
    ]
    drones = []
    legend_handles = [
        Patch(facecolor="#ef9a9a", edgecolor="#b71c1c", alpha=0.13, label="No-Fly Zone"),
        Line2D([0], [0], marker="*", linestyle="None",
               markerfacecolor="#1976d2", markeredgecolor="#0d47a1",
               markersize=11, label="Target", linewidth=1)
    ]
    for i, (sr, sc) in enumerate(drone_starts):
        lc, ec = palette[i % len(palette)]
        line, = ax.plot([], [], "-", lw=2, color=lc, alpha=0.75)
        dot,  = ax.plot([], [], "o", ms=10, color=lc, markeredgecolor=ec, markeredgewidth=1.2)
        line.set_data([sc], [sr])
        dot.set_data([sc], [sr])
        drones.append({"xs": [sc], "ys": [sr], "line": line, "dot": dot})
        legend_handles.append(Line2D([0], [0], color=lc, lw=2, label=f"Drone {i+1}"))

    ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.01, 1),
              fontsize=11, frameon=False, labelspacing=0.7)

    plt.tight_layout(pad=1.8)
    plt.draw()
    plt.pause(0.15)

    battery_texts = []
    for i, (x, y) in enumerate(_battery_layout_positions(len(drone_starts))):
        t = fig.text(x, y, f"Drone {i+1} Battery: —",
                     ha="center", va="bottom", fontsize=11,
                     bbox=dict(facecolor='#e3f2fd', edgecolor="#bbdefb", boxstyle="round,pad=0.25", linewidth=0.8))
        battery_texts.append(t)

    return {
        "fig": fig, "ax": ax,
        "drones": drones,
        "remaining_targets": remaining_targets,
        "battery_texts": battery_texts,
    }

def live_draw_step_multi(state, drone_index, pos, battery=None, pause_sec=0.018):
    r, c = pos
    d = state["drones"][drone_index]
    d["xs"].append(c)
    d["ys"].append(r)
    d["line"].set_data(d["xs"], d["ys"])
    d["dot"].set_data([c], [r])
    if (r, c) in state["remaining_targets"]:
        state["ax"].plot(c, r, marker="*", markersize=14, color="#BA68C8",
                         markeredgecolor="white", markeredgewidth=1.5, zorder=6)
        state["remaining_targets"].remove((r, c))
    if battery is not None and 0 <= drone_index < len(state["battery_texts"]):
        state["battery_texts"][drone_index].set_text(
            f"Drone {drone_index+1} Battery: {battery}%"
        )
    plt.pause(pause_sec)

def keep_plot_open():
    plt.ioff()
    print("\nAnimation complete! Close the window to exit.")
    plt.show()

