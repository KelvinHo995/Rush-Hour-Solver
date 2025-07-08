import heapq
from collections import defaultdict

def reconstruct_path(came_from, current_masks, state_map):
    path = []
    moves = []

    while current_masks in came_from:
        parent_masks, move = came_from[current_masks]
        path.append(state_map[current_masks])
        moves.append(move)
        current_masks = parent_masks

    path.append(state_map[current_masks])  # initial_state
    path.reverse()
    moves.reverse()
    return path, moves

def ucs_solver(initial_state):
    import time
    start_time = time.time()
    print("=== Bắt đầu UCS ===")

    visited_g = defaultdict(lambda: float("inf"))
    state_map = {}
    open_set = []
    came_from = {}

    init_masks = initial_state.get_separate_mask()

    heapq.heappush(open_set, (0, init_masks))
    visited_g[init_masks] = 0
    state_map[init_masks] = initial_state

    step = 0
    while open_set:
        g, current_masks = heapq.heappop(open_set)
        state = state_map[current_masks]
        step += 1

        if state.is_goal():
            print(f"UCS tìm thấy lời giải sau {step} bước expanded.")
            print(f"Thời gian: {time.time() - start_time:.2f} giây")
            path, moves = reconstruct_path(came_from, current_masks, state_map)
            costs = [visited_g[state.get_separate_mask()] for state in path]
            return path, moves, costs

        moves, successors = state.get_successors()
        for move, next_state in zip(moves, successors):
            next_masks = next_state.get_separate_mask()
            new_g = g + state.get_vehicle_weight(move[0])

            if new_g < visited_g[next_masks]:
                visited_g[next_masks] = new_g
                state_map[next_masks] = next_state
                came_from[next_masks] = (current_masks, move)
                heapq.heappush(open_set, (new_g, next_masks))

    print("UCS không tìm thấy lời giải.")
    return None, None, None
