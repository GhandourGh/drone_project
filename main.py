from io_files import load_multi_starts, load_targets, load_nfzs
from grid_utils import build_nfz_mask
from config import GRID_ROWS, GRID_COLS, BATTERY_CAPACITY_STEPS
from visualize import begin_live_map_multi, live_draw_step_multi, enable_interactive, keep_plot_open
from navigator import assign_and_run_multi_drones


def run_multi_drones():
    # Load data
    starts = load_multi_starts()
    targets = load_targets()
    nfzs = load_nfzs()
    nfz_mask = build_nfz_mask(nfzs)
    print(f"\nMulti-drone: {len(starts)} drones | {len(targets)} targets | {len(nfzs)} NFZs")
    print(f"Grid: {GRID_ROWS}x{GRID_COLS}")

    # Visualization
    enable_interactive()
    live = begin_live_map_multi(starts, targets, nfzs)

    def on_step(drone_idx, position, battery):
        live_draw_step_multi(live, drone_idx, position, battery=battery, pause_sec=0.01)

    max_steps_per_target = GRID_ROWS * GRID_COLS * 2
    battery_each = BATTERY_CAPACITY_STEPS
    final_positions, batteries_left, reached_targets, unreachable_targets = assign_and_run_multi_drones(
        starts, targets, nfz_mask,
        max_steps_per_target=max_steps_per_target,
        on_step=on_step,
        battery_each=battery_each
    )

    # Summary
    for i in range(len(final_positions)):
        drone_num = i + 1
        pos = final_positions[i]
        batt = batteries_left[i]
        print(f"Drone {drone_num}: final position {pos} | battery {batt}%")

    keep_plot_open()


def main():
    run_multi_drones()


if __name__ == "__main__":
    main()
