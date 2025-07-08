import heapq
from state import State
from collections import defaultdict, deque
import time

class Solver:
    def __init__(self, inital_state):
        self.initial_state = inital_state

    def reconstruct_path(self, came_from, current_masks, state_map):
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

    def solve(self):
        raise NotImplementedError("Subclasses must implement this method")

class BFSSolver(Solver):
    def __init__(self, initial_state):
        super().__init__(inital_state=initial_state)
    
    def solve(self):
        return self.bfs_solver()

    def bfs_solver(self):
        initial_state = self.initial_state

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
                    path, moves = self.reconstruct_path(came_from, next_masks, state_map)

                    return path, moves, None

                if next_masks in visited_masks:
                    continue

                visited_masks.add(next_masks)
                state_map[next_masks] = next_state
                came_from[next_masks] = (current_masks, move)
                open_set.append(next_masks)

                
        print("BFS không tìm thấy lời giải.")
        return None, None, None
    
class IDSSolver(Solver):
    def __init__(self, initial_state):
        super().__init__(inital_state=initial_state)
    
    def solve(self):
        return self.ids_solver()
    
    def dfs(self, state, path, move_seq, visited_masks, max_depth=50):
        current_mask = state.get_separate_mask()

        if len(path) > max_depth:
            return None, None
        
        if current_mask in visited_masks:
            return None, None
        
        visited_masks.add(current_mask)
        
        moves, successors = state.get_successors()
        
        for move, next_state in zip(moves, successors):
            new_path = path + [next_state]
            new_move_seq = move_seq + [move]

            if next_state.is_goal():
                return new_path, new_move_seq

            result_path, result_moves = self.dfs(
                next_state, 
                new_path,
                new_move_seq,
                visited_masks, 
                max_depth, 
            )

            if result_path is not None:
                return result_path, result_moves
                
        return None, None

    def ids_solver(self, max_depth=50):
        initial_state = self.initial_state
        print(f"=== Bắt đầu IDS ===")
        
        for depth in range(max_depth + 1):
            print(f"\n Đang thử với độ sâu giới hạn là: {depth}")
            visited_masks = set()

            result_path, result_moves = self.dfs(
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
                return result_path, result_moves, None

        print("Không tìm thấy lời giải.")
        return None, None, None
    
class UCSSolver(Solver):
    def __init__(self, initial_state):
        super().__init__(inital_state=initial_state)
    
    def solve(self):
        return self.ucs_solver()
    
    def ucs_solver(self):
        initial_state = self.initial_state
        start_time = time.time()
        print("=== Bắt đầu UCS ===")

        visited_g = defaultdict(lambda: float("inf"))
        state_map = {}
        open_set = []
        came_from = {}

        init_masks = initial_state.get_separate_mask()

        heapq.heappush(open_set, (0, init_masks))
        visited_g[init_masks] = 0
        state_map[init_masks] = initial_state

        step = 0
        while open_set:
            g, current_masks = heapq.heappop(open_set)
            state = state_map[current_masks]
            step += 1

            if state.is_goal():
                print(f"UCS tìm thấy lời giải sau {step} bước expanded.")
                print(f"Thời gian: {time.time() - start_time:.2f} giây")
                path, moves = self.reconstruct_path(came_from, current_masks, state_map)
                costs = [visited_g[state.get_separate_mask()] for state in path]
                return path, moves, costs

            moves, successors = state.get_successors()
            for move, next_state in zip(moves, successors):
                next_masks = next_state.get_separate_mask()
                new_g = g + state.get_vehicle_weight(move[0])

                if new_g < visited_g[next_masks]:
                    visited_g[next_masks] = new_g
                    state_map[next_masks] = next_state
                    came_from[next_masks] = (current_masks, move)
                    heapq.heappush(open_set, (new_g, next_masks))

        print("UCS không tìm thấy lời giải.")
        return None, None, None

class AStarSolver(Solver):
    BLOCKING_PATH_MASK = sum(1 << bit for bit in [35, 34, 33])  # các ô từ sau xe đỏ đến goal
    MAX_OPEN_SET_SIZE = 100000

    def __init__(self, initial_state):
        super().__init__(inital_state=initial_state)
    
    def solve(self):
        return self.a_star_solver()
    
    def popcount(x):
        return x.bit_count()

    def distance_from_bits(red_car_mask):
        # Tìm vị trí bit bên phải nhất (tức đầu xe đỏ hướng ra goal)
        lsb = (red_car_mask & -red_car_mask)  
        return 6 - (lsb & 7)

    def fast_heuristic(self, state):
        red_car_bits = state.get_vehicle_mask(0)
        blocking_bits = state.get_mask() & self.BLOCKING_PATH_MASK
        return self.popcount(blocking_bits) + self.distance_from_bits(red_car_bits)
    
    def a_star_solver(self):
        initial_state = self.initial_state
        start_time = time.time()
        print("=== Bắt đầu A* Search ===")

        visited_g = defaultdict(lambda: float("inf"))  # lưu g nhỏ nhất từng gặp
        open_set = []
        state_map = {}  # bitmask → state object
        came_from = {}

        init_masks = initial_state.get_separate_mask()    
        g = 0
        h = self.fast_heuristic(initial_state)
        f = g + h

        heapq.heappush(open_set, (f, g, init_masks)) #INITIALIZE 
        visited_g[init_masks] = g
        state_map[init_masks] = initial_state

        step = 0
        while open_set:
            f, g, current_masks = heapq.heappop(open_set)
            state = state_map[current_masks] #lấy lại state từ current_bitmask để check_goal, thay vì lưu state vào trong heapq
            step += 1

            if state.is_goal():
                print(f"🎯 Đã tìm thấy lời giải sau {step} lần expanded.")
                print(f"⏱️ Thời gian: {time.time() - start_time:.2f} giây")
                path, moves = self.reconstruct_path(came_from, current_masks, state_map)
                return path, moves, [visited_g[state.get_separate_mask()] + self.fast_heuristic(state) for state in path]

            if g > visited_g[current_masks]:
                continue

            moves, successors = state.get_successors()

            for move, next_state in zip(moves, successors):
                next_masks = next_state.get_separate_mask()
                new_g = g + state.get_vehicle_weight(move[0])
                new_h = self.fast_heuristic(next_state)
                new_f = new_g + new_h

                if new_g < visited_g[next_masks]:
                    visited_g[next_masks] = new_g
                    state_map[next_masks] = next_state
                    came_from[next_masks] = (current_masks, move)
                    heapq.heappush(open_set, (new_f, new_g, next_masks))

            if len(open_set) > self.MAX_OPEN_SET_SIZE:
                open_set = heapq.nsmallest(self.MAX_OPEN_SET_SIZE // 2, open_set)
                heapq.heapify(open_set)

        print("❌ Không tìm thấy lời giải.")
        return None, None, None
