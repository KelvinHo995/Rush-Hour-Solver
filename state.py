from copy import deepcopy
from vehicle import Vehicle, H, V

ONLY_WALLS = 18411139144890810879

class State:
    def __init__(self, vehicle_list):
        self.vehicle_list = deepcopy(vehicle_list)
        self.hor_mask = ONLY_WALLS
        self.ver_mask = ONLY_WALLS

        for vehicle in vehicle_list:
            if vehicle.orientation == H:
                self.hor_mask |= vehicle.get_mask()
            else:
                self.ver_mask |= vehicle.get_mask()

    def __hash__(self):
        # return hash((self.hor_mask, self.ver_mask))
        return self.get_mask()

    def __str__(self):
        res = ""
        
        mask = self.get_mask()

        for i in range(56, -1, -8):
            res += str(bin(mask >> i & 0b11111111))[2:] + '\n'
        
        return res
    
    def __eq__(self, other):
        return self.hor_mask == other.hor_mask and self.ver_mask == other.ver_mask
    
    def is_goal(self):
        return (self.hor_mask & (1 << 33)) and (self.hor_mask & (1 << 34))
    
    def get_mask(self):
        return self.hor_mask | self.ver_mask
    
    def get_red_car_mask(self):
        return self.vehicle_list[0].get_mask()
    
    def deepcopy(self):
        return deepcopy(self)
    
    def move_vehicle(self, id, step):
        vehicle = self.vehicle_list[id]
        moved_vehicle = vehicle.deepcopy().move(step)

        occupied_mask = self.get_mask() ^ vehicle.get_mask()
        collision = occupied_mask & moved_vehicle.get_mask()
        
        if not collision:
            #Cập nhật vehicle trong danh sách (uhuhuhhuh tìm mãi ko ra bug chỗ này)
            self.vehicle_list[id] = moved_vehicle

            if vehicle.orientation == H:
                self.hor_mask ^= vehicle.get_mask()
                self.hor_mask |= moved_vehicle.get_mask()
            else:
                self.ver_mask ^= vehicle.get_mask()
                self.ver_mask |= moved_vehicle.get_mask()
            
            return True

        return False
    
    def get_successors(self):
        moves = []
        next_states = []

        for i in range(len(self.vehicle_list)):
            #Tiến
            next_state = self.deepcopy()
            if next_state.move_vehicle(i, 1):
                moves.append((i, 1))
                next_states.append(next_state.deepcopy())

            #Lùi
            next_state = self.deepcopy()
            if next_state.move_vehicle(i, -1):
                moves.append((i, -1))
                next_states.append(next_state.deepcopy())

        return moves, next_states
