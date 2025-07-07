from collections import deque, defaultdict
from itertools import count

def bfs_solver(initial_state):
    import time
    start_time = time.time()
    print("=== Bắt đầu BFS ===")

    counter = count()
    visited_g = defaultdict(lambda: float("inf"))  # Lưu g nhỏ nhất đã gặp
    state_map = {}
    open_set = deque()  # FIFO Queue cho BFS

    init_mask = initial_state.get_mask()
    g = 0
    f = g  # BFS: f = g

    open_set.append((f, next(counter), g, init_mask, [], []))
    visited_g[init_mask] = g
    state_map[init_mask] = initial_state

    step = 0
    while open_set:
        f, _, g, current_mask, path, move_seq = open_set.popleft()
        state = state_map[current_mask]
        step += 1

        if state.is_goal():
            print(f"BFS tìm thấy lời giải sau {step} bước expanded.")
            print(f"Thời gian: {time.time() - start_time:.2f} giây")
            return path + [state], move_seq

        moves, successors = state.get_successors()
        for move, next_state in zip(moves, successors):
            next_mask = next_state.get_mask()
            new_g = g + 1
            new_f = new_g  # BFS: f = g

            if new_g < visited_g[next_mask]:
                visited_g[next_mask] = new_g
                state_map[next_mask] = next_state
                open_set.append((new_f, next(counter), new_g, next_mask, path + [state], move_seq + [move]))

    print("BFS không tìm thấy lời giải.")
    return None, None
