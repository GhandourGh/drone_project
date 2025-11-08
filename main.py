# main.py

# main.py

from io_files import load_start_pos, load_targets, load_nfzs
from grid_utils import build_nfz_mask, check_start_and_targets
from movement_utils import valid_neighbors, choose_step_toward
from config import GRID_ROWS, GRID_COLS, BATTERY_CAPACITY_STEPS
from visualize import begin_live_map, live_draw_step, enable_interactive, keep_plot_open
from navigator import visit_targets_in_order


def main():
    # Load input files
    start = load_start_pos()
    targets = load_targets()
    nfzs = load_nfzs()

    # Build NFZ mask & validate start/targets
    nfz_mask = build_nfz_mask(nfzs)
    current, filtered_targets = check_start_and_targets(start, targets, nfz_mask)

    print("\n✅ Grid check OK")
    print(f"Grid:    {GRID_ROWS} x {GRID_COLS}")
    print(f"Start:   {current}")
    print(f"Targets: {filtered_targets}")
    print(f"NFZs:    {nfzs}")
    print(f"Blocked cells: {int(nfz_mask.sum())}")

    # Show valid neighbors from start
    r, c = current
    nbrs = valid_neighbors(r, c, nfz_mask)
    print(f"\nValid neighbors from {current}: {nbrs}")

    if not filtered_targets:
        print("\nNo targets to move toward.")
        return

    # First target quick textual suggestion (now based on A*)
    first_target = filtered_targets[0]
    suggested = choose_step_toward(current, first_target, nfz_mask)
    print(f"First target: {first_target}")
    print(f"Suggested next step toward target: {suggested}")

    # Enable live plotting mode
    print("\n🎬 Starting animation...")
    enable_interactive()
    live = begin_live_map(current, filtered_targets, nfzs)

    # Battery setup
    initial_battery = BATTERY_CAPACITY_STEPS
    print(f"🔋 Battery capacity: {initial_battery} steps")

    # Walk all targets in order with animation
    max_steps_per_target = GRID_ROWS * GRID_COLS * 2  # prevent infinite loops

    final_pos, full_path, report, battery_left = visit_targets_in_order(
        current,
        filtered_targets,
        nfz_mask,
        max_steps_per_target,
        on_step=lambda pos, b: live_draw_step(live, pos, battery=b, pause_sec=0.01),
        battery=initial_battery,
    )

    # Mission summary
    print("\n✅ Mission summary")
    for idx, (tgt, reached, used) in enumerate(report, start=1):
        print(f"  Target #{idx} {tgt} | Reached: {reached} | Steps: {used}")

    print(f"Final position: {final_pos}")
    print(f"Total path length (including start): {len(full_path)}")
    print(f"🔋 Battery remaining: {battery_left} moves left")

    # Keep the plot window open after animation finishes
    keep_plot_open()

if __name__ == "__main__":
    main()