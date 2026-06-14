"""
CBC Gravity Simulation
Mass attracts mass
"""

import numpy as np
import matplotlib.pyplot as plt

L = 31
MAX_STEPS = 200
NUM_TRIALS = 10

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
            grid[i][j] = "90" if (i + j) % 2 == 0 else "270"
    return grid

def place_mass(grid, cx, cy, radius=3):
    for r in range(radius):
        for angle in range(0, 360, 60):
            rad = np.radians(angle)
            x = int(round(cx + r * np.cos(rad)))
            y = int(round(cy + r * np.sin(rad)))
            if 0 <= x < L and 0 <= y < L:
                grid[x][y] = "0"
    return grid

def place_test_particle(grid, cx, cy, distance=5):
    grid[cx + distance][cy] = "0"
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

def get_particle_position(grid, target_state="0", exclude_pos=None):
    for i in range(L):
        for j in range(L):
            if grid[i][j] == target_state and (exclude_pos is None or (i, j) != exclude_pos):
                return (i, j)
    return None

def simulate_gravity():
    cx, cy = L//2, L//2
    grid = create_vacuum(L)
    grid = place_mass(grid, cx, cy)
    grid = place_test_particle(grid, cx, cy, distance=5)
    
    initial_pos = get_particle_position(grid, exclude_pos=(cx, cy))
    
    for step in range(MAX_STEPS):
        grid = update_grid(grid)
        new_pos = get_particle_position(grid, exclude_pos=(cx, cy))
        if new_pos is None:
            break
        if new_pos == (cx, cy):
            break
    
    final_pos = get_particle_position(grid, exclude_pos=(cx, cy))
    if initial_pos is None or final_pos is None:
        return 0.0
    displacement = np.sqrt((final_pos[0] - initial_pos[0])**2 + (final_pos[1] - initial_pos[1])**2)
    return displacement

def main():
    print("=== CBC Gravity Simulation ===")
    displacements = []
    for _ in range(NUM_TRIALS):
        disp = simulate_gravity()
        displacements.append(disp)
    avg_disp = np.mean(displacements)
    print(f"Average displacement: {avg_disp:.2f} pixels")
    if avg_disp > 1.0:
        print("Result: Attraction confirmed")
    else:
        print("Result: No significant attraction")

if __name__ == "__main__":
    main()
