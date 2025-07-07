from state import State, H, V
from vehicle import Vehicle
from a_star_solver import a_star_solver

def make_map_1():
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


mask = (1 << 37) | (1 << 36)  # vị trí xe đỏ: (3,2)-(3,3)
red_car = Vehicle(mask, H)
# initial_state = State(vehicle_list=[red_car])
initial_state = make_map_1()

print("=== TRẠNG THÁI BAN ĐẦU ===")
print(initial_state)

path, moves, total_cost = a_star_solver(initial_state)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("=== TRẠNG THÁI BAN ĐẦU ===\n")
    f.write(str(initial_state) + "\n")

    if path:
        f.write(f"(Kiểm tra path) Tìm thấy lời giải với {len(path)-1} bước:\n")
        f.write(f"Total cost = {total_cost}\n")
        f.write(f"(Kiểm tra moves) Tìm thấy lời giải với {len(moves)} bước:\n\n")
        for i in range(len(moves)):
            f.write(f"Bước {i+1}: Move = {moves[i]} \n")
            f.write(str(path[i+1]) + "\n")  # path[0] là initial_state

    else:
        f.write(" Không tìm thấy lời giải.\n")
