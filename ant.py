import random
import numpy as np

class Ant:
       
    VALID_DIRECTIONS = [
        (0, -1),   # North (0)
        (1, -1),  # NE (1)
        (-1, -1),   # NW (1)
        (1, 0),   # East (2)
        (-1, 0),  # West (2)
        (1, 1),   # SE (3)
        (-1, 1), # SW (3)
        (0, 1),  # South (4)
    ]
    
    TURNING_KERNEL = [
        0.360,
        0.047,
        0.008,
        0.004
    ]
    
    WEIGHTS = [
        1.0 - (2 * TURNING_KERNEL[0] + 2 * TURNING_KERNEL[1] + 2 * TURNING_KERNEL[2] + TURNING_KERNEL[3]),
        TURNING_KERNEL[0],
        TURNING_KERNEL[0],
        TURNING_KERNEL[1],
        TURNING_KERNEL[1],
        TURNING_KERNEL[2],
        TURNING_KERNEL[2],
        TURNING_KERNEL[3]
    ]
    
    def __init__(self, init_pos):
        self.pos = init_pos
        self.direction = random.choice(self.VALID_DIRECTIONS)
        
    def move(self, grid):
        self.turn()
        self.pos = np.add(self.pos, self.direction)

        if(not self.in_bounds()): return False
        return True
    
    def turn(self):
        direction_idx = self.VALID_DIRECTIONS.index(self.direction)
        relative_idx = [direction_idx]
        for i in range(1, 7, 2):
            left_direction = (direction_idx + ((i // 2) + 1)) % 8
            right_direction = (direction_idx - ((i // 2) + 1)) % 8
            
            relative_idx.append(left_direction)
            relative_idx.append(right_direction)
            
        relative_idx.append((direction_idx + 4) % 8)
        relative_directions = []
        for idx in relative_idx:
            relative_directions.append(self.VALID_DIRECTIONS[idx])
            
        self.direction = random.choices(relative_directions, self.WEIGHTS)[0]
            
    
    def get_pos(self):
        return self.pos
    
    def in_bounds(self):
        x = self.pos[0]
        y = self.pos[1]
        
        if(x >= 0 and x < 256 and y >= 0 and y < 256):
            return True
        return False 