from state import State
from vehicle import Vehicle
from a_star_solver import a_star_solver

H = 1
mask = (1 << 37) | (1 << 36)  # vị trí xe đỏ: (3,2)-(3,3)
red_car = Vehicle(mask, H)
initial_state = State(vehicle_list=[red_car])

print("=== TRẠNG THÁI BAN ĐẦU ===")
print(initial_state)

path = a_star_solver(initial_state)

if path:
    print(f"✅ Tìm thấy lời giải với {len(path) - 1} bước:")
    for idx, s in enumerate(path):
        print(f"Bước {idx}:")
        print(s)
else:
    print("❌ Không tìm thấy lời giải.")
