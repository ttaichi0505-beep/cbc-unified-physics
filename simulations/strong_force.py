"""
CBC Strong Force Simulation
Proton: stable, Neutron: unstable
"""

import numpy as np
import matplotlib.pyplot as plt

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
                grid[x][y] = "0" if phase < 45 or phase >= 315 else "90" if phase < 135 else "180" if phase < 225 else "270"
    return grid

def place_particle(grid, center_x, center_y, particle_type):
    if particle_type == "proton":
        grid[center_x][center_y] = "0"
    elif particle_type == "neutron":
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

def simulate_strong_force(particle_type, handedness):
    cx, cy = L//2, L//2
    grid = create_vortex(cx, cy, handedness)
    grid = place_particle(grid, cx, cy, particle_type)
    for step in range(MAX_STEPS):
        grid = update_grid(grid)
        center_state = grid[cx][cy]
        initial_center_state = "0" if particle_type == "proton" else "270"
        if center_state != initial_center_state:
            return step
    return None

def main():
    print("=== CBC Strong Force Simulation ===")
    for particle in ["proton", "neutron"]:
        decay_count = 0
        for _ in range(NUM_TRIALS):
            step = simulate_strong_force(particle, "left")
            if step is not None:
                decay_count += 1
        stability = (NUM_TRIALS - decay_count) / NUM_TRIALS * 100
        print(f"{particle}: stability={stability:.1f}%")

if __name__ == "__main__":
    main()
