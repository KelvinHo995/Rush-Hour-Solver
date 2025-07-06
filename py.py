from collections import deque
import heapq

def breadth_first_search(start_state):
    explored = set()
    frontier = deque()
    frontier.append((start_state, []))
    explored.add(state_signature(start_state))

    nodes_visited = 0

    while frontier:
        state, steps = frontier.popleft()
        nodes_visited += 1

        if check_goal(state):
            return steps + [state], nodes_visited

        for successor in expand_state(state):
            sig = state_signature(successor)
            if sig not in explored:
                explored.add(sig)
                frontier.append((successor, steps + [state]))

    return None, nodes_visited


def uniform_cost_search(start_state):
    seen_costs = {}
    priority_queue = []
    tie_breaker = 0  # To ensure stable ordering

    heapq.heappush(priority_queue, (0, tie_breaker, [], start_state))
    seen_costs[state_signature(start_state)] = 0
    tie_breaker += 1

    nodes_processed = 0

    while priority_queue:
        accumulated_cost, _, trajectory, state = heapq.heappop(priority_queue)
        nodes_processed += 1

        if check_goal(state):
            return trajectory + [state], nodes_processed

        for successor in expand_state(state):
            move_weight = 1  # Base move cost
            for label in state:
                if state[label][:2] != successor[label][:2]:
                    size = state[label][2]
                    move_weight = size * 1  # One step
                    break

            total_cost = accumulated_cost + move_weight
            sig = state_signature(successor)

            if sig not in seen_costs or total_cost < seen_costs[sig]:
                seen_costs[sig] = total_cost
                heapq.heappush(priority_queue, (total_cost, tie_breaker, trajectory + [state], successor))
                tie_breaker += 1

    return None, nodes_processed
