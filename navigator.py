# navigator.py — multi-drone (tick-based, minimal, numbered targets)

from movement_utils import choose_step_toward_smart, manhattan


def assign_and_run_multi_drones(
    drone_starts, targets, nfz_mask,
    max_steps_per_target, on_step, battery_each
):
    """
    Tick loop:
      - Idle drones take the nearest unassigned target.
      - Each tick, assigned drones take ONE step toward their target.
      - On reaching a target, record and free the drone.

    Returns (final_positions, full_paths, reports, batteries_left)
      - reports[i] = [(target, reached_bool, steps_used), ...]
    """
    n = len(drone_starts)
    positions = list(drone_starts)
    batteries = [battery_each] * n

    # Map each target to a stable number based on input order: Target 1, 2, 3, ...
    target_num = {t: idx + 1 for idx, t in enumerate(targets)}

    # Keep only non-NFZ targets
    remaining = {t for t in targets if not nfz_mask[t[0], t[1]]}

    assigned = [None] * n
    steps_on_current = [0] * n
    full_paths = [[] for _ in range(n)]
    reports = [[] for _ in range(n)]

    # One critical notice per drone when battery <= 20%
    cap = max(1, battery_each)
    critical_threshold = max(1, cap // 5)   # <= 20%
    critical_warned = [False] * n

    # Simple cap to avoid endless loops
    max_ticks = max_steps_per_target * max(1, len(remaining) + 1)
    tick = 0

    while tick < max_ticks and (remaining or any(assigned)) and any(b > 0 for b in batteries):
        # Assign idle drones to nearest *unassigned* targets
        taken = {t for t in assigned if t is not None}
        available = list(remaining - taken)

        for i in range(n):
            if batteries[i] <= 0 or assigned[i] is not None:
                continue
            if not available:
                break
            nearest = min(available, key=lambda t: manhattan(positions[i], t))
            assigned[i] = nearest
            steps_on_current[i] = 0
            available.remove(nearest)

        # One step per assigned drone
        any_progress = False
        for i in range(n):
            t = assigned[i]
            if t is None or batteries[i] <= 0:
                continue

            tgt_id = target_num.get(t, "?")

            # Already on target (0-step reach)
            if positions[i] == t:
                k = steps_on_current[i]
                print(f"Drone {i+1}: reached Target {tgt_id} in {k} step" + ("s" if k != 1 else ""))
                reports[i].append((t, True, k))
                remaining.discard(t)
                assigned[i] = None
                continue

            nxt = choose_step_toward_smart(positions[i], None, t, nfz_mask)
            if nxt is None:
                # No path — record and free the drone (concise)
                k = steps_on_current[i]
                print(f"Drone {i+1}: cannot reach Target {tgt_id}")
                reports[i].append((t, False, k))
                assigned[i] = None
                continue

            # Move one step
            positions[i] = nxt
            full_paths[i].append(nxt)
            steps_on_current[i] += 1
            batteries[i] -= 1
            any_progress = True

            # Single critical notice at ≤20%
            if not critical_warned[i] and batteries[i] <= critical_threshold:
                print(f"Drone {i+1}: critical battery ≤ 20%")
                critical_warned[i] = True

            if on_step:
                on_step(i, positions[i], batteries[i])

            # Reached after moving?
            if positions[i] == t:
                k = steps_on_current[i]
                print(f"Drone {i+1}: reached Target {tgt_id} in {k} step" + ("s" if k != 1 else ""))
                reports[i].append((t, True, k))
                remaining.discard(t)
                assigned[i] = None

        if not any_progress and not remaining:
            break

        tick += 1

    return positions, full_paths, reports, batteries