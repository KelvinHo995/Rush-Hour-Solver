import heapq
from collections import defaultdict
from itertools import count

def ucs_solver(initial_state):
    import time
    start_time = time.time()
    print("=== Bắt đầu UCS ===")

    counter = count()
    visited_g = defaultdict(lambda: float("inf"))
    state_map = {}
    open_set = []

    init_mask = initial_state.get_mask()
    g = 0
    f = g  # UCS: f = g

    heapq.heappush(open_set, (f, next(counter), g, init_mask, [], []))
    visited_g[init_mask] = g
    state_map[init_mask] = initial_state

    step = 0
    while open_set:
        f, _, g, current_mask, path, move_seq = heapq.heappop(open_set)
        state = state_map[current_mask]
        step += 1

        if state.is_goal():
            print(f"UCS tìm thấy lời giải sau {step} bước expanded.")
            print(f"Thời gian: {time.time() - start_time:.2f} giây")
            return path + [state], move_seq

        moves, successors = state.get_successors()
        for move, next_state in zip(moves, successors):
            next_mask = next_state.get_mask()
            cost = 1  # Mỗi bước = 1
            new_g = g + cost
            new_f = new_g  # UCS: f = g

            if new_g < visited_g[next_mask]:
                visited_g[next_mask] = new_g
                state_map[next_mask] = next_state
                heapq.heappush(open_set, (new_f, next(counter), new_g, next_mask, path + [state], move_seq + [move]))

    print("UCS không tìm thấy lời giải.")
    return None, None
