from state import State

def backtracking_dfs(state, path, move_seq, visited_masks, max_depth=50):
    current_mask = state.get_separate_mask()

    if len(path) > max_depth:
        # print(f"  Reached max depth {max_depth}, backtracking...")
        return None, None
    
    if current_mask in visited_masks:
        # print(f"  Mask already visited, backtracking...")
        return None, None
    
    visited_masks.add(current_mask)
    
    # if state.is_goal():
    #     print(f"  GOAL FOUND at depth {len(path)}!")
    #     return path + [state], move_seq
    
    moves, successors = state.get_successors()
    
    for move, next_state in zip(moves, successors):
        new_path = path + [next_state]
        new_move_seq = move_seq + [move]

        if next_state.is_goal():
            return new_path, new_move_seq

        result_path, result_moves = backtracking_dfs(
            next_state, 
            new_path,
            new_move_seq,
            visited_masks, 
            max_depth, 
        )

        if result_path is not None:
            return result_path, result_moves
        
        # print(f"  Move {i+1} failed, trying next move...")

    #visited_masks.remove(current_mask)
    
    return None, None

def ids_solver(initial_state, max_depth=50):
    print(f"=== Bắt đầu IDS ===")
    print(initial_state)
    
    for depth in range(max_depth + 1):
        print(f"\n Đang thử với độ sâu giới hạn là: {depth}")
        visited_masks = set()

        result_path, result_moves = backtracking_dfs(
            initial_state, 
            [initial_state], 
            [],
            visited_masks, 
            depth, 
        )
        if result_path is not None:
            print(f"Tìm thấy lời giải ở độ sâu {depth}")
            print(f"Số mask đã thăm: {len(visited_masks)}")
            print(f"=== Kết thúc tìm kiếm ===")
            return result_path, result_moves

    print("Không tìm thấy lời giải.")
    return None, None