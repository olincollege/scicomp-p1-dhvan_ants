import random
import numpy as np

class Ant:
       
    VALID_DIRECTIONS = [
        (0, -1),   # North (0)
        (1, -1),  # NE (1)
        (1, 0),   # East (2)
        (1, 1),   # SE (3)
        (0, 1),  # South (4)
        (-1, 1), # SW (3)
        (-1, 0),  # West (2)
        (-1, -1),   # NW (1)
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
    
    MODE = {
        "Explore": 0,
        "Follow": 1
    }
    
    def __init__(self, init_pos):
        self.pos = init_pos
        self.direction = random.choice(self.VALID_DIRECTIONS)
        
        self.mode = self.MODE["Explore"]
        
    def move(self, grid):
        surrounding_concentrations = []
        for direction in self.VALID_DIRECTIONS:
            if(self.direction[0] == -direction[0] and self.direction[1] == -direction[1]):
                surrounding_concentrations.append(0.0)
                continue
            surrounding_square = np.add(self.pos, direction)
            if(not self.in_bounds(surrounding_square)): 
                surrounding_concentrations.append(0.0)
                continue
            surrounding_concentrations.append(grid[surrounding_square[0], surrounding_square[1]])
        
        forward_idx = self.VALID_DIRECTIONS.index(self.direction)
        if(surrounding_concentrations[forward_idx] > 7.0):
            follow_step = self.direction
            self.mode = self.MODE["Follow"]
        else:
            max_concentration = max(surrounding_concentrations)
            max_idx = np.where(np.array(surrounding_concentrations) == max_concentration)[0]            
            
            if(len(max_idx) > 1):
                self.mode = self.MODE["Explore"]
            elif(max_concentration > 7.0):
                idx = surrounding_concentrations.index(max_concentration)
                follow_step = self.VALID_DIRECTIONS[idx]
                self.mode = self.MODE["Follow"]
            else:
                self.mode = self.MODE["Explore"]
       
        if(self.mode == self.MODE["Follow"]):
            lost_trail = random.choices([0, 1], [0.95, 0.05])[0]
            if(lost_trail == 1):
                self.mode = self.MODE["Explore"]
            else:
                self.direction = follow_step
            
        if(self.mode == self.MODE["Explore"]):
            self.direction = self.turn()

        self.pos = np.add(self.pos, self.direction)
        
        if(not self.in_bounds(self.pos)): return False
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
            
        return random.choices(relative_directions, self.WEIGHTS)[0]
    
    def get_pos(self):
        return self.pos
    
    def in_bounds(self, position):
        x = position[0]
        y = position[1]
        
        if(x >= 0 and x < 256 and y >= 0 and y < 256):
            return True
        return False 