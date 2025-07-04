from copy import deepcopy
H = 1
V = 8

class Vehicle:
    def __init__(self, mask, orientation):
        self.mask = mask
        self.orientation = orientation
        self.weight = mask.bit_count()
    
    def deepcopy(self):
        return deepcopy(self)
    
    def get_mask(self):
        return self.mask
    
    def move(self, step):
        if step == 1: # Forward -> Right or Down
            self.mask >>= self.orientation
        elif step == -1: # Backward -> Left or Up
            self.mask <<= self.orientation

        return self
