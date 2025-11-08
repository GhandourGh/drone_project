import heapq
from grid_utils import in_bounds


def neighbors4(row, col):
    return [
        (row - 1, col),      # Up
        (row + 1, col),      # Down
        (row, col - 1),      # Left
        (row, col + 1)       # Right
    ]


def valid_neighbors(row, col, no_fly_zone_mask):
    return [
        (neighbor_row, neighbor_col)
        for neighbor_row, neighbor_col in neighbors4(row, col)
        if in_bounds(neighbor_row, neighbor_col) and not no_fly_zone_mask[neighbor_row, neighbor_col]
    ]


def manhattan(cell_a, cell_b):
    return abs(cell_a[0] - cell_b[0]) + abs(cell_a[1] - cell_b[1])


def a_star_path(start_cell, goal_cell, no_fly_zone_mask):
    open_cells_heap = []
    heapq.heappush(open_cells_heap, (manhattan(start_cell, goal_cell), 0, start_cell))

    cell_came_from = {}
    cost_so_far = {start_cell: 0}
    visited_cells = set()

    while open_cells_heap:
        current_f, current_cost, current_cell = heapq.heappop(open_cells_heap)

        if current_cell in visited_cells:
            continue
        visited_cells.add(current_cell)

        if current_cell == goal_cell:
            path = [current_cell]
            while current_cell in cell_came_from:
                current_cell = cell_came_from[current_cell]
                path.append(current_cell)
            return list(reversed(path))

        row, col = current_cell
        for neighbor in valid_neighbors(row, col, no_fly_zone_mask):
            if neighbor in visited_cells:
                continue

            new_cost = current_cost + 1

            if new_cost < cost_so_far.get(neighbor, float('inf')):
                cell_came_from[neighbor] = current_cell
                cost_so_far[neighbor] = new_cost
                priority = new_cost + manhattan(neighbor, goal_cell)
                heapq.heappush(open_cells_heap, (priority, new_cost, neighbor))
    return None


def a_star_next_step(current_cell, target_cell, no_fly_zone_mask):
    if current_cell == target_cell:
        return None

    path = a_star_path(current_cell, target_cell, no_fly_zone_mask)
    if not path or len(path) < 2:
        return None

    return path[1]

