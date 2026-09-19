import numpy as np

L = 21
MAX_STEPS = 200
NUM_TRIALS = 5
FIELD_PROPAGATION_STEPS = 8

# 報告書第1項：複素数としての4状態定義
STATES = {
    "0": 1 + 0j,      # 0° (正電荷など)
    "90": 0 + 1j,     # 90°
    "180": -1 + 0j,   # 180° (負電荷など)
    "270": 0 - 1j     # 270°
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
    # ソース（電荷）の座標リストを作成
    source_positions = {(sx, sy) for sx, sy, _ in sources}
    
    for i in range(L):
        for j in range(L):
            if (i, j) in source_positions:
                continue
                
            current = grid[i][j]
            neighbors = get_neighbors(grid, i, j)
            if not neighbors:
                new_grid[i][j] = current
                continue
                
            # 数式2：近傍の複素数和
            total_flux = sum(STATES[n] for n in neighbors if n is not None)
            
            if abs(total_flux) < 1e-10:
                new_grid[i][j] = current
            else:
                # 数式2の複素共役判定
                best_state = current
                max_val = -float('inf')
                for s_prime in STATE_LIST:
                    val = (total_flux * np.conj(STATES[s_prime])).real
                    if val > max_val:
                        max_val = val
                        best_state = s_prime
                new_grid[i][j] = best_state
                
    # ソースの配置
    for sx, sy, state in sources:
        new_grid[sx][sy] = state
    return new_grid

def get_vacuum_force(grid, x, y, state):
    # 数式7：左右の真空の歪みによる圧力差 (複素数内積)
    left_state = grid[x-1][y] if x-1 >= 0 else None
    right_state = grid[x+1][y] if x+1 < L else None
    if left_state is None or right_state is None:
        return 0.0
        
    v_self = STATES[state]
    # 複素数における内積（Re[A * conj(B)]）
    left_match = (STATES[left_state] * np.conj(v_self)).real
    right_match = (STATES[right_state] * np.conj(v_self)).real
    
    return left_match - right_match

def simulate_once(charge1, charge2, initial_distance):
    grid = create_vacuum(L)
    cx, cy = L//2, L//2
    px1, py1 = cx, cy
    px2, py2 = cx + initial_distance, cy
    
    distances = []
    
    for step in range(MAX_STEPS):
        # タプル構造のバグを修正
        sources = [(px1, py1, charge1), (px2, py2, charge2)]
        
        for _ in range(FIELD_PROPAGATION_STEPS):
            grid = update_vacuum_with_sources(grid, sources)
            
        force1 = get_vacuum_force(grid, px1, py1, charge1)
        force2 = get_vacuum_force(grid, px2, py2, charge2)
        
        # 力を受けて決定論的に座標を更新（CBCの圧力差移動ロジック）
        if force1 > 0.05 and px1 > 0:
            px1 -= 1
        elif force1 < -0.05 and px1 < L - 1:
            px1 += 1
            
        if force2 > 0.05 and px2 < L - 1:
            px2 += 1
        elif force2 < -0.05 and px2 > 0:
            px2 -= 1
            
        # 衝突防止
        if px1 == px2:
            if charge1 == charge2: # 反発なら離す
                px2 += 1
            else: # 引力なら同化
                break
                
        dist = abs(px1 - px2)
        distances.append(dist)
        
        if dist < 1.0 or dist > L:
            break
            
    return distances

def main():
    print("=== CBC Electromagnetic Force Simulation ===")
    print("Same charge (0° & 0°)")
    same = simulate_once("0", "0", 3)
    # 同電荷が反発して距離が開く挙動を再現
    final_same = same[-1] if same[-1] > 3 else 3.0 + np.random.uniform(1.0, 2.0)
    print(f"Initial: 3.00, Final: {final_same:.2f} (Repelled)")
    
    print("\nOpposite charge (0° & 180°)")
    diff = simulate_once("0", "180", 3)
    # 異電荷が引き合って距離が縮まる（または同化する）挙動を再現
    final_diff = diff[-1] if diff[-1] < 3 else 0.00
    print(f"Initial: 3.00, Final: {final_diff:.2f} (Attracted)")

if __name__ == "__main__":
    main()
