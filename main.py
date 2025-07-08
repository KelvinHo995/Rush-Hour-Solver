from state import State
from vehicle import Vehicle, H, V
from recursive_dfs import *

# mask = (1 << 37) | (1 << 36)  # Xe nằm ngang tại (3,2)-(3,3)
# red_car = Vehicle(mask, H)
# initial_state = State(vehicle_list=[red_car])
ve1 = Vehicle((1 << 37) | (1 << 36), H)  #red car
ve2 = Vehicle((1 << 43) | (1 << 35), V)  
ve3 = Vehicle((1 << 34) | (1 << 42) | (1 << 50), V)
ve4 = Vehicle((1 << 49) | (1 << 41) | (1 << 33), V)
ve5 = Vehicle((1 << 26) | (1 << 25), H)
ve6 = Vehicle((1 << 28) | (1 << 20), V)
ve7 = Vehicle((1 << 27) | (1 << 19), V)
ve8 = Vehicle((1 << 14) | (1 << 13), H)
ve9 = Vehicle((1 << 10) | (1 << 9), H)
initial_state = State([ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9])

path, moves = dfs_solver(initial_state, max_depth=50)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("=== TRẠNG THÁI BAN ĐẦU ===\n")
    f.write(str(initial_state) + "\n")
    f.write(f"Horizontal mask: {bin(initial_state.hor_mask)}\n")
    f.write(f"Vertical mask: {bin(initial_state.ver_mask)}\n")
    f.write(f"Is goal: {initial_state.is_goal()}\n\n")

    if path and moves:
        f.write(f"(Kiểm tra path) Tìm thấy lời giải với {len(path)-1} bước:\n")
        f.write(f"(Kiểm tra moves) Tìm thấy lời giải với {len(moves)} bước:\n\n")
        for idx, s in enumerate(path):
            f.write(f"--- State a{idx} ---\n")
            f.write(str(s) + "\n")
            
        for idx, s in enumerate(moves):
            f.write(f"--- Bước b{idx} ---\n")
            f.write(str(s) + "\n")
    else:
        f.write(" Không tìm thấy lời giải.\n")
