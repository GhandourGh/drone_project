# navigator.py
# Tiny stepper helpers (no OOP, simple prints)

from movement_utils import choose_step_toward_smart, manhattan


def take_steps_toward(current, target, nfz_mask, max_steps=5):
    """
    Legacy tiny stepper (no battery). Kept for quick tests.
    Uses the smart chooser step-by-step.
    Returns (new_pos, path_extension).
    """
    pos = current
    prev = None
    path_ext = []

    for step in range(1, max_steps + 1):
        nxt = choose_step_toward_smart(pos, prev, target, nfz_mask)
        if nxt is None:
            print(f"⚠️  No valid move from {pos}. Stopping early.")
            break

        path_ext.append(nxt)
        prev = pos
        pos = nxt
        print(f"Step {step}: moved to {pos} (toward {target})")

        if pos == target:
            print("🎯 Reached target!")
            break

    return pos, path_ext


def walk_to_target(current, target, nfz_mask, max_steps, on_step=None, battery=None):
    """
    Step toward `target` up to `max_steps` or until battery empties.
    Returns (new_pos, path_ext, reached, steps_used, battery).
    """
    pos = current
    prev = None  # kept for signature compatibility
    path_ext = []
    steps_used = 0
    reached = False

    # If no battery provided, treat as effectively infinite
    if battery is None:
        battery = 10**9

    for _ in range(max_steps):
        if battery <= 0:
            print("🔋 Battery empty. Stopping.")
            break

        if pos == target:
            reached = True
            break

        nxt = choose_step_toward_smart(pos, prev, target, nfz_mask)
        if nxt is None:
            print(f"⚠️  Stuck at {pos}. No valid move.")
            break

        path_ext.append(nxt)
        prev = pos
        pos = nxt
        steps_used += 1
        battery -= 1  # 🔋 drain per step

        if on_step is not None:
            on_step(pos, battery)

        print(f"Step {steps_used}: moved to {pos} (toward {target})")

        if pos == target:
            reached = True
            break

    if reached:
        print("🎯 Reached target!")
    else:
        if battery <= 0:
            print(f"⏹ Stopped after {steps_used} steps (battery empty).")
        else:
            print(f"⏹ Stopped after {steps_used} steps (target not reached).")

    return pos, path_ext, reached, steps_used, battery


def visit_targets_in_order(start, targets, nfz_mask, max_steps_per_target, on_step=None, battery=None):
    """
    Visit targets using a greedy rule: always pick the nearest remaining target
    (by Manhattan distance) from the current position. Skip targets inside NFZ.
    Then return to the start if battery allows.

    Battery decreases by 1 per step across the whole mission.

    Returns (final_pos, full_path, report, battery_left)
      - final_pos: last position after all attempts (ideally back at 'start')
      - full_path: list of all visited cells starting with 'start'
      - report: list of tuples (target, reached_bool, steps_used)
                (the final tuple corresponds to returning to 'start' if attempted)
      - battery_left: remaining battery after mission/return
    """
    pos = start
    full_path = [start]
    report = []

    # Default battery (effectively infinite) if not provided
    if battery is None:
        battery = 10**9

    # Make a working copy of targets
    remaining = list(targets)
    step_idx = 0

    while remaining and battery > 0:
        # Filter out targets that are inside NFZ
        not_blocked = []
        blocked = []
        for t in remaining:
            tr, tc = t
            if nfz_mask[tr, tc]:
                blocked.append(t)
            else:
                not_blocked.append(t)

        # Log and drop blocked ones
        for t in blocked:
            print(f"⛔ Target {t} is inside a No-Fly Zone — skipping.")
            report.append((t, False, 0))
            remaining.remove(t)

        if not not_blocked:
            # Nothing left that isn't blocked
            break

        # Pick the nearest (by Manhattan) among the non-blocked targets
        nearest = not_blocked[0]
        best_d = manhattan(pos, nearest)
        for t in not_blocked[1:]:
            d = manhattan(pos, t)
            if d < best_d:
                best_d = d
                nearest = t

        step_idx += 1
        print(f"\n🎯 Target #{step_idx} (nearest): {nearest}")

        # Walk to the chosen target
        new_pos, path_ext, reached, used, battery = walk_to_target(
            pos, nearest, nfz_mask, max_steps=max_steps_per_target, on_step=on_step, battery=battery
        )

        full_path.extend(path_ext)
        report.append((nearest, reached, used))
        pos = new_pos

        # Remove it from remaining (regardless of reached or not, we won't try it again)
        if nearest in remaining:
            remaining.remove(nearest)

    # Return to start (if possible) and if battery remains
    if pos != start and battery > 0:
        print(f"\n🚦 Returning to start {start} ...")
        sr, sc = start
        if nfz_mask[sr, sc]:
            print("⛔ Start position is inside a No-Fly Zone — cannot return.")
            report.append((start, False, 0))
        else:
            new_pos, path_ext, reached, used, battery = walk_to_target(
                pos, start, nfz_mask, max_steps=max_steps_per_target, on_step=on_step, battery=battery
            )
            full_path.extend(path_ext)
            report.append((start, reached, used))
            pos = new_pos
    elif pos == start:
        print("\n✅ Already at start; no return needed.")
    else:
        if battery <= 0:
            print("\n🔋 Battery empty before return. Mission ends where it stopped.")

    return pos, full_path, report, battery
