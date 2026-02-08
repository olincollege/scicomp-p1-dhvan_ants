# ant.py

import random
import numpy as np

class Ant:
       
    VALID_DIRECTIONS = [
        (0, -1),   # North (0)
        (1, -1),  # NE (1)
        (1, 0),   # East (2)
        (1, 1),   # SE (3)
        (0, 1),  # South (4)
        (-1, 1), # SW (5)
        (-1, 0),  # West (6)
        (-1, -1),   # NW (7)
    ]
    
    TURNING_KERNEL = [
        0.360 / 2,
        0.047 / 2,
        0.008 / 2,
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
    
    MODE = {
        "Explore": 0,
        "Follow": 1
    }
        
    def __init__(self, init_pos):
        
        self.pos = init_pos
        initial_directions = self.VALID_DIRECTIONS[1::2]
        self.direction = random.choice(initial_directions)
        
        fid = 255 / 256
        self.FIDELITY = [fid, 1 - fid]
        
        self.mode = self.MODE["Explore"]
        
    def move(self, grid):
        trail_direction = self.check_for_trail(grid)

        if(self.mode == self.MODE["Follow"] or trail_direction != (0, 0)):
            fidelity = random.choices([0, 1], self.FIDELITY)[0]
            if(trail_direction != (0, 0) and fidelity == 0):
                self.direction = trail_direction
                self.mode = self.MODE["Follow"]
            else:
                self.mode = self.MODE["Explore"]
        
        if(self.mode == self.MODE["Explore"] or trail_direction == (0, 0)):
            self.direction = self.turn()
            
        self.pos = np.add(self.pos, self.direction)
        
        return self.in_bounds(self.pos)
    
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
            
        return random.choices(relative_directions, self.WEIGHTS)[0]
    
    def check_for_trail(self, grid):
        previous_position = self.pos
        previous_direction = self.direction
        
        relative_direction_list = self.get_relative_directions(self.VALID_DIRECTIONS.index(previous_direction))
        idx_check = [0, 1, 7]
        concentrations = []
        for idx in idx_check:
            rel_dir = relative_direction_list[idx]
            rel_pos = np.add(previous_position, rel_dir)
            
            if(not self.in_bounds(rel_pos)):
                concentrations.append(0.0)
                continue
                
            concentration = grid[rel_pos[0], rel_pos[1]]
            concentrations.append(concentration)
            
        concentrations = np.array(concentrations)
        
        max_concentration = np.max(concentrations)
        num_max = np.count_nonzero(concentrations == max_concentration)
        
        
        if(concentrations[0] > 0.0): return relative_direction_list[idx_check[0]]
        
        if(num_max > 1):
            return (0, 0)

        max_idx = np.where(concentrations == max_concentration)[0][0]
        
        if(max_concentration > 0.0):
            return relative_direction_list[idx_check[max_idx]]

        return (0, 0)
        
    def get_relative_directions(self, direction_idx):
        return self.VALID_DIRECTIONS[direction_idx:] + self.VALID_DIRECTIONS[0:direction_idx]
    
    def get_pos(self):
        return self.pos
    
    def get_mode(self):
        return self.mode
    
    def in_bounds(self, position):
        x = position[0]
        y = position[1]
        
        if(x >= 0 and x < 256 and y >= 0 and y < 256):
            return True
        return False 