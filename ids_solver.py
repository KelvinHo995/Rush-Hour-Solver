
def depth_limited_dfs(state, limit, visited, path):
    if state in visited:
        return None
    visited.add(state)

    if state.is_goal():
        return path + [state]
    
    if limit == 0:
        return None  # đã hết độ sâu giới hạn

    moves, successors = state.get_successors()
    for succ in successors:
        result = depth_limited_dfs(succ, limit - 1, visited, path + [state])
        if result:
            return result

    return None

def iterative_deepening_search(initial_state, max_depth=50):
    for depth in range(max_depth + 1):
        visited = set()
        print(f"Đang thử với độ sâu giới hạn: {depth}")
        result = depth_limited_dfs(initial_state, limit=depth, visited=visited, path=[])
        if result:
            print(f" Tìm thấy lời giải ở độ sâu {depth}")
            return result
    print(" Không tìm thấy lời giải trong giới hạn độ sâu.")
    return None
