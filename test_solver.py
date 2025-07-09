from state import State
from vehicle import Vehicle
from solver import IDSSolver, BFSSolver, AStarSolver, UCSSolver
H = 1  # Horizontal
V = 8  # Vertical

def make_map_1():
    # Ví dụ: 1 map Rush Hour đơn giản
    ve1 = Vehicle((1 << 37) | (1 << 36), H)  # Xe đỏ
    ve2 = Vehicle((1 << 43) | (1 << 35), V)
    ve3 = Vehicle((1 << 34) | (1 << 42) | (1 << 50), V)
    ve4 = Vehicle((1 << 49) | (1 << 41) | (1 << 33), V)
    ve5 = Vehicle((1 << 26) | (1 << 25), H)
    ve6 = Vehicle((1 << 28) | (1 << 20), V)
    return State([ve1, ve2, ve3, ve4, ve5, ve6])

def make_map_2():
    ve1 = Vehicle((1 << 37) | (1 << 36), H)  #red car
    ve2 = Vehicle((1 << 43) | (1 << 35), V)  
    ve3 = Vehicle((1 << 34) | (1 << 42) | (1 << 50), V)
    ve4 = Vehicle((1 << 49) | (1 << 41) | (1 << 33), V)
    ve5 = Vehicle((1 << 26) | (1 << 25), H)
    ve6 = Vehicle((1 << 28) | (1 << 20), V)
    ve7 = Vehicle((1 << 27) | (1 << 19), V)
    ve8 = Vehicle((1 << 14) | (1 << 13), H)
    ve9 = Vehicle((1 << 10) | (1 << 9), H)
    return State([ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9])

def run_solver(solver_func, initial_state, solver_name):
    print(f"\n=== {solver_name} ===")
    path, moves, costs = solver_func(initial_state)

    if path:
        print(f"{solver_name} tìm thấy lời giải với {len(path) - 1} bước.")
        for i in range(len(moves)):
            print(f"Bước {i+1}: Move = {moves[i]}")
            print(path[i+1])
    else:
        print(f"{solver_name} không tìm thấy lời giải.")

if __name__ == "__main__":
    initial_state = make_map_2()
    print("=== TRẠNG THÁI BAN ĐẦU ===")
    print(initial_state)

    solver = IDSSolver(initial_state, trace=True)
    path, moves, costs, peak = solver.solve()
