# navigator.py
# Tiny stepper helpers (no OOP, simple prints)

from movement_utils import choose_step_toward_smart

def take_steps_toward(current, target, nfz_mask, max_steps=5):
    """
    Move up to max_steps toward target using a greedy rule with a tiny memory:
    avoid immediately stepping back to the previous cell (unless stuck).
    Returns (new_pos, path_extension) where path_extension excludes the starting cell.
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


def walk_to_target(current, target, nfz_mask, max_steps, on_step=None):
    """
    Keep stepping toward `target` until reached or `max_steps` used.
    Greedy U/D/L/R with Manhattan; tie breaks random; avoids instant backtracking.
    Returns (new_pos, path_ext, reached, steps_used).
    """
    pos = current
    prev = None
    path_ext = []
    steps_used = 0
    reached = False

    for _ in range(max_steps):
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
        if on_step is not None:
            on_step(pos)
        print(f"Step {steps_used}: moved to {pos} (toward {target})")

        if pos == target:
            reached = True
            break

    if reached:
        print("🎯 Reached target!")
    else:
        print(f"⏹ Stopped after {steps_used} steps (target not reached).")

    return pos, path_ext, reached, steps_used


def visit_targets_in_order(start, targets, nfz_mask, max_steps_per_target, on_step=None):
    """
    Visit each target in sequence using walk_to_target.
    Returns (final_pos, full_path, report)
      - final_pos: last position after all attempts
      - full_path: list of all visited cells starting with 'start'
      - report: list of tuples (target, reached_bool, steps_used)
    """
    pos = start
    full_path = [start]
    report = []

    for i, tgt in enumerate(targets, start=1):
        print(f"\n🎯 Target #{i}: {tgt}")
        new_pos, path_ext, reached, used = walk_to_target(
            pos, tgt, nfz_mask, max_steps=max_steps_per_target, on_step=on_step
        )
        full_path.extend(path_ext)
        report.append((tgt, reached, used))
        pos = new_pos

    return pos, full_path, report
