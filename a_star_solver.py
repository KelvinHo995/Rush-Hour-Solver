import heapq
from state import State
from collections import defaultdict
from itertools import count

# === CONSTANTS ===
RED_CAR_MASK = (1 << 37) | (1 << 36)  # Giả định xe đỏ luôn có mask như vậy (vị trí (3,2)-(3,3))
BLOCKING_PATH_MASK = sum(1 << bit for bit in [35, 34, 33])  # các ô từ sau xe đỏ đến goal
MAX_OPEN_SET_SIZE = 100000

# === UTILITY FUNCTIONS ===

def popcount(x):
    return x.bit_count()

def distance_from_bits(red_car_mask):
    # Tìm vị trí bit bên phải nhất (tức đầu xe đỏ hướng ra goal)
    lsb = (red_car_mask & -red_car_mask)  
    return 6 - (lsb & 7)

def fast_heuristic(state):
    red_car_bits = state.get_red_car_mask()
    blocking_bits = state.get_mask() & BLOCKING_PATH_MASK
    return popcount(blocking_bits) + distance_from_bits(red_car_bits)

def reconstruct_path(came_from, current_mask, state_map):
    path = []
    moves = []

    while current_mask in came_from:
        parent_mask, move = came_from[current_mask]
        path.append(state_map[current_mask])
        moves.append(move)
        current_mask = parent_mask

    path.append(state_map[current_mask])  # initial_state
    path.reverse()
    moves.reverse()
    return path, moves

# === A* SOLVER ===

def a_star_solver(initial_state):
    import time
    start_time = time.time()
    print("=== Bắt đầu A* Search ===")

    counter = count()
    visited_g = defaultdict(lambda: float("inf"))  # lưu g nhỏ nhất từng gặp
    open_set = []
    state_map = {}  # bitmask → state object
    came_from = {}

    init_mask = initial_state.get_mask()    
    g = 0
    h = fast_heuristic(initial_state)
    f = g + h

    heapq.heappush(open_set, (f, g, init_mask)) #INITIALIZE 
    visited_g[init_mask] = g
    state_map[init_mask] = initial_state

    step = 0
    while open_set:
        f, g, current_mask = heapq.heappop(open_set)
        state = state_map[current_mask] #lấy lại state từ current_bitmask để check_goal, thay vì lưu state vào trong heapq
        step += 1

        if state.is_goal():
            print(f"🎯 Đã tìm thấy lời giải sau {step} lần expanded.")
            print(f"⏱️ Thời gian: {time.time() - start_time:.2f} giây")
            path, moves = reconstruct_path(came_from, current_mask, state_map)
            return path, moves, [visited_g[state.get_mask()] + fast_heuristic(state) for state in path]

        if g > visited_g[current_mask]:
            continue

        moves, successors = state.get_successors()

        for move, next_state in zip(moves, successors):
            next_mask = next_state.get_mask()
            new_g = g + state.vehicle_list[move[0]].get_weight()
            new_h = fast_heuristic(next_state)
            new_f = new_g + new_h

            if new_g < visited_g[next_mask]:
                visited_g[next_mask] = new_g
                state_map[next_mask] = next_state
                came_from[next_mask] = (current_mask, move)
                heapq.heappush(open_set, (new_f, new_g, next_mask))

        if len(open_set) > MAX_OPEN_SET_SIZE:
            open_set = heapq.nsmallest(MAX_OPEN_SET_SIZE // 2, open_set)
            heapq.heapify(open_set)

    print("❌ Không tìm thấy lời giải.")
    return None, None, None
