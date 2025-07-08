from copy import deepcopy
from vehicle import Vehicle, H, V

ONLY_WALLS = 18411139144890810879

class State:
    vehicle_orientation = []
    vehicle_weight = []

    def __init__(self, vehicle_list, init_static=True):
        self.vehicle_mask = []
        self.hor_mask = ONLY_WALLS
        self.ver_mask = ONLY_WALLS

        for vehicle in vehicle_list:
            mask = vehicle.get_mask()

            self.vehicle_mask.append(mask)

            if vehicle.get_orientation() == H:
                self.hor_mask |= vehicle.mask
            else:
                self.ver_mask |= vehicle.mask

            if init_static:
                self.vehicle_orientation.append(vehicle.get_orientation())
                self.vehicle_weight.append(vehicle.get_weight())

    @classmethod
    def from_masks(cls, vehicle_mask):
        vehicle_list = []

        for i, mask in enumerate(vehicle_mask):
            vehicle = Vehicle(mask, cls.vehicle_orientation[i])
            vehicle_list.append(vehicle)

        return cls(vehicle_list, False)
    
    def __hash__(self):
        return hash((self.hor_mask, self.ver_mask))

    def __str__(self):
        res = ""
        
        mask = self.get_mask()

        for i in range(56, -1, -8):
            res += str(bin(mask >> i & 0b11111111))[2:] + '\n'
        
        return res
    
    def __eq__(self, other):
        return self.hor_mask == other.hor_mask and self.ver_mask == other.ver_mask
    
    def __lt__(self, other):
        if self.hor_mask == other.hor_mask:
            return self.ver_mask < other.ver_mask
        return self.hor_mask < other.hor_mask
    
    def is_goal(self):
        return (self.hor_mask & (1 << 33)) and (self.hor_mask & (1 << 34))
    
    def get_separate_mask(self):
        return self.hor_mask, self.ver_mask
    
    def get_mask(self):
        return self.hor_mask | self.ver_mask
    
    def get_vehicle_mask(self, id):
        return self.vehicle_mask[id]
    
    def get_vehicle_weight(self, id):
        return self.vehicle_weight[id]
    
    def get_vehicle_orientation(self, id):
        return self.vehicle_orientation[id]
    
    def deepcopy(self):
        return deepcopy(self)
    
    def move_vehicle(self, id, step):
        current_mask = self.vehicle_mask[id]
        orientation = self.vehicle_orientation[id]

        next_mask = Vehicle(current_mask, orientation).move(step).get_mask()

        occupied_mask = self.get_mask() ^ current_mask
        collision = occupied_mask & next_mask
        
        if not collision:
            #Cập nhật vehicle trong danh sách (uhuhuhhuh tìm mãi ko ra bug chỗ này)
            self.vehicle_mask[id] = next_mask

            if orientation == H:
                self.hor_mask ^= current_mask
                self.hor_mask |= next_mask
            else:
                self.ver_mask ^= current_mask
                self.ver_mask |= next_mask
            
            return True

        return False
    
    def get_successors(self):
        moves = []
        next_states = []

        for i in range(len(self.vehicle_mask)):
            #Tiến
            next_state = State.from_masks(self.vehicle_mask.copy())
            if next_state.move_vehicle(i, 1):
                moves.append((i, 1))
                next_states.append(next_state)

            #Lùi
            next_state = State.from_masks(self.vehicle_mask.copy())
            if next_state.move_vehicle(i, -1):
                moves.append((i, -1))
                next_states.append(next_state)

        return moves, next_states
