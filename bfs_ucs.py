from collections import deque
import heapq

def bfs_solver(initial_state):
    print(f"=== Bắt đầu BFS ===")
    print(initial_state)

    visited_masks = set()
    queue = deque()

    # Queue chứa tuple: (state hiện tại, path, move_seq)
    queue.append((initial_state, [], []))
    visited_masks.add(initial_state.get_mask())

    expanded_nodes = 0

    while queue:
        current_state, path, move_seq = queue.popleft()
        expanded_nodes += 1

        if current_state.is_goal():
            print(f"  GOAL FOUND at depth {len(path)}!")
            return path + [current_state], move_seq

        moves, successors = current_state.get_successors()
        for move, next_state in zip(moves, successors):
            next_mask = next_state.get_mask()
            if next_mask not in visited_masks:
                visited_masks.add(next_mask)
                queue.append(
                    (next_state, path + [current_state], move_seq + [move])
                )

    print(f"=== Kết thúc tìm kiếm (không tìm thấy đích) ===")
    print(f"Số nút đã mở rộng: {expanded_nodes}")
    return None, None



def ucs_solver(initial_state):
    print(f"=== Bắt đầu UCS ===")
    print(initial_state)

    visited_masks = set()
    queue = []

    # (tổng cost, state, path, move_seq)
    heapq.heappush(queue, (0, initial_state, [], []))
    visited_masks.add(initial_state.get_mask())

    expanded_nodes = 0

    while queue:
        total_cost, current_state, path, move_seq = heapq.heappop(queue)
        expanded_nodes += 1

        if current_state.is_goal():
            print(f"  GOAL FOUND with cost {total_cost}!")
            return path + [current_state], move_seq, total_cost

        moves, successors = current_state.get_successors()
        for move, next_state in zip(moves, successors):
            cost = move.cost  # Bạn tự định nghĩa move.cost
            next_mask = next_state.get_mask()
            if next_mask not in visited_masks:
                visited_masks.add(next_mask)
                heapq.heappush(
                    queue,
                    (total_cost + cost,
                     next_state,
                     path + [current_state],
                     move_seq + [move])
                )

    print(f"=== Kết thúc tìm kiếm (không tìm thấy đích) ===")
    print(f"Số nút đã mở rộng: {expanded_nodes}")
    return None, None, None
