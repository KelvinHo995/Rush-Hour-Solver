from state import State
from vehicle import Vehicle, H, V
from recursive_dfs import ids_solver

ve1 = Vehicle((1 << 37) | (1 << 36), H)  #red car
ve2 = Vehicle((1 << 43) | (1 << 35), V)  
ve3 = Vehicle((1 << 34) | (1 << 42) | (1 << 50), V)
ve4 = Vehicle((1 << 49) | (1 << 41) | (1 << 33), V)
ve5 = Vehicle((1 << 26) | (1 << 25), H)
ve6 = Vehicle((1 << 28) | (1 << 20), V)
ve7 = Vehicle((1 << 27) | (1 << 19), V)
ve8 = Vehicle((1 << 14) | (1 << 13), H)
ve9 = Vehicle((1 << 10) | (1 << 9), H)
initial_state = State([ve1, ve2, ve3, ve4, ve5, ve6, ve7])

path, moves = ids_solver(initial_state, max_depth=50)
with open("output.txt", "w", encoding="utf-8") as f:
    if path:
        f.write(f"Giải thành công với {len(path)-1} bước:\n\n")
        for i in range(len(moves)):
            f.write(f"Bước {i+1}: Move = {moves[i]} \n")
            f.write(str(path[i+1]) + "\n")  # path[0] là initial_state
    else:
        f.write("Không tìm được lời giải.\n")
