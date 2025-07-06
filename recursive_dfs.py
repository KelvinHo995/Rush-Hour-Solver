def backtracking_dfs(state, path, move_seq, visited_masks, max_depth=50):
    current_mask = state.get_mask()

    if len(path) > max_depth:
        print(f"  Reached max depth {max_depth}, backtracking...")
        return None
    
    if current_mask in visited_masks:
        print(f"  Mask already visited, backtracking...")
        return None
    
    visited_masks.add(current_mask)
    
    if state.is_goal():
        print(f"  GOAL FOUND at depth {len(path)}!")
        return path + [state], move_seq
    
    moves, successors = state.get_successors()
    
    for i, (move, next_state) in enumerate(zip(moves, successors)):
        new_path = path + [state]
        new_move_seq = move_seq + [move]

        result_path, result_moves = backtracking_dfs(
            next_state, 
            new_path,
            new_move_seq,
            visited_masks, 
            max_depth, 
        )

        if result_path is not None:
            #print(f"  Solution found through this branch!")
            return result_path, result_moves
        
        print(f"  Move {i+1} failed, trying next move...")

    visited_masks.remove(current_mask)
    print(f"  All moves failed at depth {len(path)}, backtracking...")
    
    return None, None

def dfs_solver(initial_state, max_depth=50):
    print(f"=== Bắt đầu Backtracking DFS (max_depth={max_depth}) ===")
    print(initial_state)
    
    visited_masks = set()
    result_path, result_moves = backtracking_dfs(
        initial_state, 
        [], 
        [],
        visited_masks, 
        max_depth, 
    )
    
    print(f"=== Kết thúc tìm kiếm ===")
    print(f"Số mask đã thăm: {len(visited_masks)}")
    
    return result_path, result_moves
