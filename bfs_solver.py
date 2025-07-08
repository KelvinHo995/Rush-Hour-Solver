from collections import deque

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

def bfs_solver(initial_state):
    import time
    start_time = time.time()
    print("=== Bắt đầu BFS ===")

    visited_masks = set()
    state_map = {}
    came_from = {}
    open_set = deque()  # FIFO Queue cho BFS

    init_masks = initial_state.get_separate_mask()

    visited_masks.add(init_masks)
    open_set.append(init_masks)
    state_map[init_masks] = initial_state

    step = 0
    while open_set:
        current_masks = open_set.popleft()
        state = state_map[current_masks]
        step += 1

        moves, successors = state.get_successors()
        for move, next_state in zip(moves, successors):
            next_masks = next_state.get_separate_mask()

            # Early goal test
            if next_state.is_goal():
                print(f"BFS tìm thấy lời giải sau {step} bước expanded.")
                print(f"Thời gian: {time.time() - start_time:.2f} giây")

                state_map[next_masks] = next_state
                came_from[next_masks] = (current_masks, move)
                path, moves = reconstruct_path(came_from, next_masks, state_map)

                return path, moves, None

            if next_masks in visited_masks:
                continue

            visited_masks.add(next_masks)
            state_map[next_masks] = next_state
            came_from[next_masks] = (current_masks, move)
            open_set.append(next_masks)

            
    print("BFS không tìm thấy lời giải.")
    return None, None, None
