from movement_utils import manhattan, a_star_next_step

def assign_and_run_multi_drones(drone_starts, targets, nfz_mask, max_steps_per_target, on_step, battery_each):
    n = len(drone_starts)
    positions = list(drone_starts)
    batteries = [battery_each] * n
    assigned = [None] * n
    reachable_targets = set(t for t in targets if not nfz_mask[t[0], t[1]])
    reached_targets = set()

    while (reachable_targets or any(assigned)) and any(b > 0 for b in batteries):
        available = list(reachable_targets - set(t for t in assigned if t is not None))
        for i in range(n):
            # Assign new target if idle
            if batteries[i] > 0 and assigned[i] is None and available:
                nearest = min(available, key=lambda t: manhattan(positions[i], t))
                assigned[i] = nearest
                available.remove(nearest)
            # Move toward target
            target = assigned[i]
            if target is not None and batteries[i] > 0:
                if positions[i] == target:
                    reachable_targets.discard(target)
                    assigned[i] = None
                    reached_targets.add(target)
                else:
                    nxt = a_star_next_step(positions[i], target, nfz_mask)
                    if nxt is not None:
                        positions[i] = nxt
                        batteries[i] -= 1
                        if on_step:
                            on_step(i, positions[i], batteries[i])
                        if positions[i] == target:
                            reachable_targets.discard(target)
                            assigned[i] = None
                            reached_targets.add(target)
                    else:
                        assigned[i] = None

    # Unreachable/left targets
    unreachable_targets = set(targets) - reached_targets
    return positions, batteries, reached_targets, unreachable_targets





