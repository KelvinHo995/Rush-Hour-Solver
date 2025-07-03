def backtracking_dfs(state, path, visited_masks, max_depth=50):
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
        return path + [state]
    
    moves, successors = state.get_successors()
    
    for i, (move, next_state) in enumerate(zip(moves, successors)):
        result = backtracking_dfs(
            next_state, 
            path + [state], 
            visited_masks, 
            max_depth, 
        )

        if result is not None:
            #print(f"  Solution found through this branch!")
            return result
        
        print(f"  Move {i+1} failed, trying next move...")

    visited_masks.remove(current_mask)
    
    print(f"  All moves failed at depth {len(path)}, backtracking...")
    
    return None

def dfs_solver(initial_state, max_depth=50):
    print(f"=== Bắt đầu Backtracking DFS (max_depth={max_depth}) ===")
    print(initial_state)
    
    visited_masks = set()
    
    result = backtracking_dfs(
        initial_state, 
        [], 
        visited_masks, 
        max_depth, 
    )
    
    print(f"=== Kết thúc tìm kiếm ===")
    print(f"Số mask đã thăm: {len(visited_masks)}")
    
    return result
