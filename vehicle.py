from copy import deepcopy
H = 1
V = 8

class Vehicle:
    def __init__(self, mask, orientation):
        self.mask = mask
        if orientation == V:
            self.mask |= 1
    
    def deepcopy(self):
        return deepcopy(self)
    
    def get_mask(self):
        return (self.mask & ~1)
    
    def get_orientation(self):
        if self.mask & 1 == 1:
            return V
        return H
    
    def get_weight(self):
        return self.get_mask().bit_count()
    
    def move(self, step):
        orientation = self.get_orientation()
        self.mask &= ~1

        if step == 1: # Forward -> Right or Down
            self.mask >>= orientation
        elif step == -1: # Backward -> Left or Up
            self.mask <<= orientation

        if orientation == V:
            self.mask |= 1
            
        return self

    def get_position(self):
        msb = self.mask.bit_length() - 1
        row = 6 - (msb >> 3)
        column = 6 - (msb & 7)

        return row, column
