import heapq
from state import State
from collections import defaultdict, deque
import time
import tracemalloc

class Solver:
    def __init__(self, inital_state, trace=None):
        self.initial_state = inital_state
        self.trace = trace

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
    def __init__(self, initial_state, trace=None):
        super().__init__(inital_state=initial_state, trace=trace)
    
    def solve(self):
        return self.bfs_solver()

    def bfs_solver(self):
        initial_state = self.initial_state

        if self.trace == 'other':
            start_time = time.time()
        if self.trace == 'memory':
            tracemalloc.start(1)

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
                    # print(f"BFS tìm thấy lời giải sau {step} bước expanded.")
                    # print(f"Thời gian: {time.time() - start_time:.2f} giây")

                    if self.trace == 'other':
                        total_time = time.time() - start_time
                        return step, total_time
                    if self.trace == 'memory':
                        _, peak = tracemalloc.get_traced_memory()
                        # print(f"Mức dữ liệu sử dụng tối đa: {peak / 1024 / 1024:.2f} MB")
                        tracemalloc.stop()
                        return peak / 1024 / 1024

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
        return (None,) * 3
    
class IDSSolver(Solver):    
    def __init__(self, initial_state, trace=None):
        super().__init__(inital_state=initial_state, trace=trace)
        self.step = 0
    
    def solve(self):
        return self.ids_solver()
    
    def dfs(self, state, path, move_seq, min_length, max_depth):
        current_masks = state.get_separate_mask()

        if len(move_seq) >= max_depth:
            return None, None
        
        if min_length[current_masks] <= len(move_seq):
            return None, None
        
        self.step += 1
        min_length[current_masks] = len(move_seq)
        
        moves, successors = state.get_successors()
        
        for move, next_state in zip(moves, successors):
            path.append(next_state)
            move_seq.append(move)

            if next_state.is_goal():
                return path, move_seq

            result_path, result_moves = self.dfs(
                next_state, 
                path,
                move_seq,
                min_length,
                max_depth, 
            )

            if result_path is not None:
                return result_path, result_moves
            
            path.pop()
            move_seq.pop()
                
        return None, None

    def ids_solver(self, max_depth=88):
        if self.trace == 'other':
            start_time = time.time()
        elif self.trace == 'memory':
            tracemalloc.start(1)
        initial_state = self.initial_state
        # print(f"=== Bắt đầu IDS ===")
        
        for depth in range(4, max_depth + 1, 4):
            # print(f"\n Đang thử với độ sâu giới hạn là: {depth}")
            min_length = defaultdict(lambda: float('inf'))

            result_path, result_moves = self.dfs(
                initial_state, 
                [initial_state], 
                [],
                min_length, 
                max_depth=depth, 
            )

            if result_path:
                break

        # Found nothing -> return
        if result_path is None:
            print("Không tìm thấy lời giải.")
            return (None,) * 3
        
        # Found a solution at depth 
        # Check depth - 2
        min_length = defaultdict(lambda: float('inf'))
        test_path, test_moves = self.dfs(
            initial_state, 
            [initial_state], 
            [],
            min_length, 
            max_depth=depth - 2, 
        )

        if test_path:  # depth - 2 exists -> check depth - 3
            result_path, result_moves = test_path, test_moves

            min_length = defaultdict(lambda: float('inf'))
            test_path, test_moves = self.dfs(
                initial_state, 
                [initial_state], 
                [],
                min_length, 
                max_depth=depth - 3, 
            )

            if test_path:
                result_path, result_moves = test_path, test_moves
        else: # else depth - 2 does not have a solution -> check depth - 1
            min_length = defaultdict(lambda: float('inf'))
            test_path, test_moves = self.dfs(
                initial_state, 
                [initial_state], 
                [],
                min_length, 
                max_depth=depth - 1, 
            )

            if test_path:
                result_path, result_moves = test_path, test_moves

        # print(f"Tìm thấy lời giải ở độ sâu {depth}")
        # print(f"Số mask đã thăm: {len(min_length)}")
        # print(f"Thời gian: {time.time() - start_time:.2f} giây")
        if self.trace == 'other':
            total_time = time.time() - start_time
            return self.step, total_time
        if self.trace == 'memory':
            _, peak = tracemalloc.get_traced_memory()
            # print(f"Mức dữ liệu sử dụng tối đa: {peak / 1024 / 1024:.2f} MB")
            tracemalloc.stop()
            return peak / 1024 / 1024
        
        # print(f"=== Kết thúc tìm kiếm ===")

        return result_path, result_moves, None    
        
class UCSSolver(Solver):
    def __init__(self, initial_state, trace=None):
        super().__init__(inital_state=initial_state, trace=trace)
    
    def solve(self):
        return self.ucs_solver()
    
    def ucs_solver(self):
        if self.trace == 'memory':
            tracemalloc.start(1)
        elif self.trace == 'other':
            start_time = time.time()

        initial_state = self.initial_state
        
        # print("=== Bắt đầu UCS ===")

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
                # print(f"UCS tìm thấy lời giải sau {step} bước expanded.")
                # print(f"Thời gian: {time.time() - start_time:.2f} giây")
                if self.trace == 'other':
                    total_time = time.time() - start_time
                    return step, total_time
                if self.trace == 'memory':
                    _, peak = tracemalloc.get_traced_memory()
                    # print(f"Mức dữ liệu sử dụng tối đa: {peak / 1024 / 1024:.2f} MB")
                    tracemalloc.stop()
                    return peak / 1024 / 1024

                path, moves = self.reconstruct_path(came_from, current_masks, state_map)
                costs = [visited_g[state.get_separate_mask()] for state in path[1:]]

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
        return (None,) * 3

class AStarSolver(Solver):
    BLOCKING_PATH_MASK = sum(1 << bit for bit in [35, 34, 33])  # các ô từ sau xe đỏ đến goal
    MAX_OPEN_SET_SIZE = 100000

    def __init__(self, initial_state, trace=None):
        super().__init__(inital_state=initial_state, trace=trace)
    
    def solve(self):
        return self.a_star_solver()

    def fast_heuristic(self, state):
        red_car_bits = state.get_vehicle_mask(0)

        lsb = (red_car_bits & -red_car_bits).bit_length() - 1
        dis_to_goal = ((lsb & 7) - 1)

        blocking_bits = ((1 << lsb) - 1) ^ ((1 << 33) - 1)
        blocking_bits &= state.get_mask()

        return dis_to_goal + blocking_bits.bit_count()
    
    def a_star_solver(self):
        if self.trace == 'memory':
            tracemalloc.start(1)
        elif self.trace == 'other':
            start_time = time.time()

        initial_state = self.initial_state

        # print("=== Bắt đầu A* Search ===")

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
                # print(f"🎯 Đã tìm thấy lời giải sau {step} lần expanded.")
                # print(f"⏱️ Thời gian: {time.time() - start_time:.2f} giây")
                if self.trace == 'other':
                    total_time = time.time() - start_time
                    return step, total_time
                if self.trace == 'memory':
                    _, peak = tracemalloc.get_traced_memory()
                    # print(f"Mức dữ liệu sử dụng tối đa: {peak / 1024 / 1024:.2f} MB")
                    tracemalloc.stop()
                    return peak / 1024 / 1024
                
                path, moves = self.reconstruct_path(came_from, current_masks, state_map)
                costs = [visited_g[state.get_separate_mask()] + self.fast_heuristic(state) for state in path[1:]]
             
                return path, moves, costs 

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
        return (None,) * 3
