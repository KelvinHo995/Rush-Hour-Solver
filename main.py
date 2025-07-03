from state import State
from vehicle import Vehicle
from dfs_solver import dfs
from ids_solver import iterative_deepening_search
H = 1
mask = (1 << 37) | (1 << 36)  # Xe nằm ngang tại (3,2)-(3,3)
red_car = Vehicle(mask, H)
initial_state = State(vehicle_list=[red_car])

#path = dfs(initial_state, max_depth=20)
path = iterative_deepening_search(initial_state, max_depth=20)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("=== TRẠNG THÁI BAN ĐẦU ===\n")
    f.write(str(initial_state) + "\n")
    f.write(f"Horizontal mask: {bin(initial_state.hor_mask)}\n")
    f.write(f"Vertical mask: {bin(initial_state.ver_mask)}\n")
    f.write(f"Is goal: {initial_state.is_goal()}\n\n")

    if path:
        f.write(f" Tìm thấy lời giải với {len(path)-1} bước:\n\n")
        for idx, s in enumerate(path):
            f.write(f"--- Bước {idx} ---\n")
            f.write(str(s) + "\n")
    else:
        f.write(" Không tìm thấy lời giải.\n")
