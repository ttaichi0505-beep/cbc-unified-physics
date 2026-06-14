"""
CBC Electromagnetic Force Simulation
Same charge repels, opposite charge attracts
"""

import numpy as np
import matplotlib.pyplot as plt

L = 21
MAX_STEPS = 200
NUM_TRIALS = 5
FIELD_PROPAGATION_STEPS = 8

STATES = {
    "0": np.array([1, 0]),
    "90": np.array([0, 1]),
    "180": np.array([-1, 0]),
    "270": np.array([0, -1])
}
STATE_LIST = ["0", "90", "180", "270"]

def create_vacuum(L):
    grid = [[None for _ in range(L)] for _ in range(L)]
    for i in range(L):
        for j in range(L):
            idx = (i + j) % 4
            grid[i][j] = STATE_LIST[idx]
    return grid

def get_neighbors(grid, x, y):
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < L and 0 <= ny < L:
            neighbors.append(grid[nx][ny])
    return neighbors

def update_vacuum_with_sources(grid, sources):
    new_grid = [[None for _ in range(L)] for _ in range(L)]
    for i in range(L):
        for j in range(L):
            is_source = any(i == sx and j == sy for sx, sy, _ in sources)
            if is_source:
                continue
            if grid[i][j] is not None:
                current = grid[i][j]
                neighbors = get_neighbors(grid, i, j)
                if not neighbors:
                    new_grid[i][j] = current
                else:
                    v_sum = np.array([0.0, 0.0])
                    for n in neighbors:
                        if n is not None:
                            v_sum += STATES[n]
                    if np.linalg.norm(v_sum) < 1e-10:
                        new_grid[i][j] = current
                    else:
                        dots = {s: np.dot(v_sum, STATES[s]) for s in STATE_LIST}
                        best_state = max(dots, key=dots.get)
                        if np.random.random() < 0.05:
                            new_grid[i][j] = np.random.choice(STATE_LIST)
                        else:
                            new_grid[i][j] = best_state
    for sx, sy, state in sources:
        new_grid[sx][sy] = state
    return new_grid

def get_vacuum_force(grid, x, y, state):
    left_state = grid[x-1][y] if x-1 >= 0 else None
    right_state = grid[x+1][y] if x+1 < L else None
    if left_state is None or right_state is None:
        return 0.0
    v_self = STATES[state]
    left_match = np.dot(STATES[left_state], v_self)
    right_match = np.dot(STATES[right_state], v_self)
    fx = left_match - right_match
    if state == "0":
        return fx * 5.0
    else:
        return fx * 1.5

def simulate_once(charge1, charge2, initial_distance):
    grid = create_vacuum(L)
    cx, cy = L//2, L//2
    px1, py1 = cx, cy
    px2, py2 = cx + initial_distance, cy
    vx1, vx2 = 0.0, 0.0
    distances = []
    for step in range(MAX_STEPS):
        sources = [((px1, py1), 1, charge1), ((px2, py2), 2, charge2)]
        for _ in range(FIELD_PROPAGATION_STEPS):
            grid = update_vacuum_with_sources(grid, sources)
        force1 = get_vacuum_force(grid, px1, py1, charge1)
        force2 = get_vacuum_force(grid, px2, py2, charge2)
        dt = 0.1
        damping = 0.95
        vx1 = vx1 * damping + force1 * dt
        vx2 = vx2 * damping + force2 * dt
        new_px1 = px1 + int(np.round(np.clip(vx1, -1, 1)))
        new_px2 = px2 + int(np.round(np.clip(vx2, -1, 1)))
        if 0 <= new_px1 < L and new_px1 != px2:
            px1 = new_px1
            vx1 *= 0.5
        if 0 <= new_px2 < L and new_px2 != px1:
            px2 = new_px2
            vx2 *= 0.5
        dist = abs(px1 - px2)
        distances.append(dist)
        if dist < 1.0 or dist > L:
            break
    return distances

def main():
    print("Same charge (0° & 0°)")
    same = simulate_once("0", "0", 3)
    print(f"Initial: 3.00, Final: {same[-1]:.2f}")
    print("Opposite charge (0° & 180°)")
    diff = simulate_once("0", "180", 3)
    print(f"Initial: 3.00, Final: {diff[-1]:.2f}")

if __name__ == "__main__":
    main()
