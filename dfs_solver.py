def dfs(initial_state, max_depth=100):
    stack = [(initial_state, [], 0)]  # (state, path, depth)
    visited = set()

    while stack:
        state, path, depth = stack.pop()

        if state in visited or depth > max_depth:
            continue
        visited.add(state)

        if state.is_goal():
            return path + [state]

        moves, successors = state.get_successors()

        for succ in reversed(successors):  # đảo ngược để đi sâu trước
            stack.append((succ, path + [state], depth + 1))

    return None
