"""
CBC Weak Force Simulation
Parity violation (left bias = 1.000)
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

L = 31
MAX_STEPS = 500
NUM_TRIALS = 100

STATES = {
    "0": np.array([1, 0]),
    "90": np.array([0, 1]),
    "180": np.array([-1, 0]),
    "270": np.array([0, -1])
}
STATE_LIST = ["0", "90", "180", "270"]

def angle_to_state(angle):
    angle = angle % 360
    if angle < 45 or angle >= 315:
        return "0"
    elif angle < 135:
        return "90"
    elif angle < 225:
        return "180"
    else:
        return "270"

def create_vortex(center_x, center_y, handedness='left', radius=5):
    grid = [[None for _ in range(L)] for _ in range(L)]
    grid[center_x][center_y] = "0"
    for r in range(1, radius + 1):
        for angle in range(0, 360, 30):
            rad = np.radians(angle)
            x = int(round(center_x + r * np.cos(rad)))
            y = int(round(center_y + r * np.sin(rad)))
            if 0 <= x < L and 0 <= y < L and grid[x][y] is None:
                if handedness == 'left':
                    phase = angle % 360
                else:
                    phase = (-angle) % 360
                grid[x][y] = angle_to_state(phase)
    return grid

def place_neutron(grid, center_x, center_y):
    grid[center_x][center_y] = "270"
    return grid

def get_neighbors(grid, x, y):
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < L and 0 <= ny < L and grid[nx][ny] is not None:
            neighbors.append(grid[nx][ny])
    return neighbors

def update_cell(grid, x, y):
    current = grid[x][y]
    if current is None:
        return None
    neighbors = get_neighbors(grid, x, y)
    if not neighbors:
        return current
    v_sum = np.array([0.0, 0.0])
    for n in neighbors:
        if n is not None:
            v_sum += STATES[n]
    if np.linalg.norm(v_sum) < 1e-10:
        return current
    dots = {s: np.dot(v_sum, STATES[s]) for s in STATE_LIST}
    best_state = max(dots, key=dots.get)
    return best_state

def update_grid(grid):
    new_grid = [[None for _ in range(L)] for _ in range(L)]
    for i in range(L):
        for j in range(L):
            if grid[i][j] is not None:
                new_grid[i][j] = update_cell(grid, i, j)
    return new_grid

def simulate_weak_force(handedness):
    cx, cy = L//2, L//2
    grid = create_vortex(cx, cy, handedness)
    grid = place_neutron(grid, cx, cy)
    initial_grid = [row[:] for row in grid]
    for step in range(MAX_STEPS):
        grid = update_grid(grid)
        if grid[cx][cy] != "270":
            # 放射方向を測定
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                x, y = cx + dx, cy + dy
                if 0 <= x < L and 0 <= y < L and grid[x][y] not in ["0", "180"]:
                    if dx == 1:
                        return "right"
                    elif dx == -1:
                        return "left"
                    elif dy == 1:
                        return "down"
                    elif dy == -1:
                        return "up"
            return None
    return None

def main():
    print("=== CBC Weak Force Simulation ===")
    for handedness in ["left", "right"]:
        directions = []
        for _ in range(NUM_TRIALS):
            direction = simulate_weak_force(handedness)
            if direction:
                directions.append(direction)
        left_count = directions.count("left")
        right_count = directions.count("right")
        total = len(directions)
        bias = (left_count - right_count) / total if total > 0 else 0
        print(f"{handedness}: bias={bias:.3f} (left={left_count}, right={right_count})")

if __name__ == "__main__":
    main()
