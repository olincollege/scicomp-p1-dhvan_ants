# ant.py
import random
import numpy as np
import config

class Ant:
    """
    Simulates a single ant agent based on the Watmough & Edelstein-Keshet (1995) model.
    
    Attributes:
        pos (tuple): Current (x, y) coordinates of the ant.
        direction (tuple): Current direction vector (dx, dy).
        mode (int): Current behavioral state (0 = Explore, 1 = Follow).
    """
       
    # Emperically defined list of directions.
    # Will make the ant move in that direction if added its current position.
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
    
    # Turning probabilities derived from Watmough (1995) Figure 3.
    # The paper's kernel (B_n) gives the TOTAL probability for a turn angle magnitude.
    # We divide by 2 to split that probability equally between Left and Right turns.
    # The first element is the probability of moving straight (0 degrees).
    # It's calculated by subtracting the rest of the probabilities from 1.
    WEIGHTS = [
        1.0 - (config.TURNING_KERNEL[0] + config.TURNING_KERNEL[1] + config.TURNING_KERNEL[2] + config.TURNING_KERNEL[3]),
        config.TURNING_KERNEL[0] / 2,
        config.TURNING_KERNEL[0] / 2,
        config.TURNING_KERNEL[1] / 2,
        config.TURNING_KERNEL[1] / 2,
        config.TURNING_KERNEL[2] / 2,
        config.TURNING_KERNEL[2] / 2,
        config.TURNING_KERNEL[3]
    ]
    
    # Dictionary that represents the modes of the ant
    MODE = {
        "Explore": 0,
        "Follow": 1
    }
        
    def __init__(self, init_pos):
        self.pos = init_pos
        # Restrict initial heading to diagonals (NE, SE, SW, NW).
        # The paper notes orientation is chosen from a "specified set".
        # The distinct "X" pattern in Figure 3 implies this set consisted of the four diagonal vectors.
        initial_directions = self.VALID_DIRECTIONS[1::2]
        
        self.direction = random.choice(initial_directions)
        
        # Normalize the paper's 0-255 integer fidelity scale to a 0-1 probability
        self.FIDELITY = [config.FIDELITY / 256, 1 - (config.FIDELITY / 256)]
        
        self.mode = self.MODE["Explore"]
        
    def move(self, grid):
            """
            Updates the ant's position based on pheromone sensing and random walks.
            
            Implements the motion rules from Section 2 of the paper:
            1. Checks for trails using the "Fork Algorithm".
            2. Decides to follow or explore based on Fidelity.
            3. Turns using the weighted kernel if exploring.
            
            Args:
                grid (np.ndarray): The 2D pheromone grid.
                
            Returns:
                bool: True if the ant remains in bounds, False if it leaves the grid.
            """
            # Returns a valid direction vector (dx, dy) if a trail is found,
            # or (0, 0) to signal that no distinct trail was detected (random walk).
            trail_direction = self.check_for_trail(grid)

            # Fidelity Logic:
            # We check fidelity if we are ALREADY following a trail, 
            # OR if we are exploring and just encountered one.
            if(self.mode == self.MODE["Follow"] or trail_direction != (0, 0)):
                
                # Fideility Check: 0 = Stay/Start Following, 1 = Lose Trail.
                fidelity = random.choices([0, 1], self.FIDELITY)[0]
                
                # Re-verify trail existence. Even if we passed the fidelity check (0),
                # we can only 'Follow' if a physical trail actually exists (!= 0,0).
                # If trail_direction is (0,0) here, it means we ran out of pheromone 
                # while in Follow mode, forcing a switch to Explore.
                if(trail_direction != (0, 0) and fidelity == 0):
                    self.direction = trail_direction
                    self.mode = self.MODE["Follow"]
                else:
                    self.mode = self.MODE["Explore"]
            
            # If we are exploring (or if the trail check above failed/returned (0,0)),
            # we perform a random turn using the weighted kernel.
            if(self.mode == self.MODE["Explore"] or trail_direction == (0, 0)):
                self.direction = self.turn()
                
            # Update position.
            # self.direction is guaranteed to be a valid unit vector from VALID_DIRECTIONS,
            # allowing for direct vector addition.
            self.pos = np.add(self.pos, self.direction)
            
            # Return status for the boundary check.
            # Note: Optimization trade-off. We calculate the out-of-bounds position first, 
            # then flag it for removal in the main loop.
            return self.in_bounds(self.pos)
    
    def turn(self):
            """
            Calculates a new direction based on the probabilistic Turning Kernel.
            
            Uses the kernel weights defined in config.py to simulate the ant's random turning behavior.
            """
            # Get the index of the ant's current global heading (0-7).
            direction_idx = self.VALID_DIRECTIONS.index(self.direction)
            
            # Start the relative list with the "Straight" direction (offset 0).
            relative_idx = [direction_idx]
            
            # Build a list of neighbor indices relative to the ant's current heading.
            # The goal is to map global grid directions into a local perspective:
            # [Straight, Left45, Right45, Left90, Right90, Left135, Right135].
            # We use modular arithmetic (% 8) to wrap around the compass bounds.
            for i in range(1, 7, 2):
                offset = (i // 2) + 1  # Calculates offsets: 1 (45 deg), 2 (90 deg), 3 (135 deg)
                left_direction = (direction_idx + offset) % 8
                right_direction = (direction_idx - offset) % 8
                
                relative_idx.append(left_direction)
                relative_idx.append(right_direction)
                
            # Append the 180-degree (U-turn) index, which acts as the "rear" and has no Left/Right pair.
            relative_idx.append((direction_idx + 4) % 8)
            
            # Convert the relative indices back into actual (dx, dy) direction vectors.
            # This list now strictly matches the order of probabilities defined in self.WEIGHTS.
            relative_directions = []
            for idx in relative_idx:
                relative_directions.append(self.VALID_DIRECTIONS[idx])
                
            # Choose a new direction using the weighted probability distribution.
            return random.choices(relative_directions, self.WEIGHTS)[0]
        
    def check_for_trail(self, grid):
            """
            Scans the forward-facing neighborhood to decide steering direction.
            
            Implements the "Fork Algorithm" from Section 2 of the paper,
            prioritizing straight movement and handling ambiguous trails.
            """
            previous_position = self.pos
            previous_direction = self.direction
            
            # We need to look relative to the ant's current heading.
            # This helper rotates the compass so index 0 is always "Forward".
            relative_direction_list = self.get_relative_directions(self.VALID_DIRECTIONS.index(previous_direction))
            
            # Scan indices [0, 1, 7] corresponding to Front, Front-Right, and Front-Left.
            # We ignore side/rear neighbors to simulate the antennae's limited forward field of view.
            idx_check = [0, 1, 7]
            concentrations = []
            for idx in idx_check:
                rel_dir = relative_direction_list[idx]
                rel_pos = np.add(previous_position, rel_dir)
                
                # Assume that there is no trail outside of the grid
                if(not self.in_bounds(rel_pos)):
                    concentrations.append(0.0)
                    continue
                    
                concentration = grid[rel_pos[0], rel_pos[1]]
                concentrations.append(concentration)
                
            concentrations = np.array(concentrations)
            
            max_concentration = np.max(concentrations)
            num_max = np.count_nonzero(concentrations == max_concentration)
            
            # Paper Rule (a): "Continue moving forward if the trail continues straight ahead".
            # If the forward cell (index 0) has ANY pheromone, we prioritize maintaining momentum.
            if(concentrations[0] > 0.0): 
                return relative_direction_list[idx_check[0]]
            
            # Paper Rule (b): "Move as if exploring if both branches are of equal concentration"[.
            # If we see multiple max values (e.g., equal left/right fork), we return (0,0).
            # This triggers the "Turn" logic in move(), causing a random exploration step.
            # We don't have to worry about if the forward and left values were the ones with
            # Equal concentration, since we would have already returned a value if there was anything
            # detected in front of the ant
            if(num_max > 1):
                return (0, 0)

            # Paper Rule (c): "Follow the stronger of the two branches".
            # We identified a single strongest neighbor that isn't forward. Turn towards it.
            max_idx = np.where(concentrations == max_concentration)[0][0]
            
            if(max_concentration > 0.0):
                return relative_direction_list[idx_check[max_idx]]

            # Fallback: No trail found at all.
            return (0, 0)
        
    def get_relative_directions(self, direction_idx):
        """
        Rotates the global direction list to be relative to the ant's current heading.
        
        Effectively sets the provided index as 'Forward' (Index 0) for local sensing.
        """
        return self.VALID_DIRECTIONS[direction_idx:] + self.VALID_DIRECTIONS[0:direction_idx]
        
    def get_pos(self):
        """Returns the current (row, col) grid coordinates."""
        return self.pos
    
    def get_mode(self):
        """Returns the current behavioral state (0 = Explore, 1 = Follow)."""
        return self.mode
    
    def in_bounds(self, position):
        """
        Checks if a coordinate pair is within the simulation grid boundaries.
        
        Used to enforce the 'Absorbing Boundary Conditions'.
        """
        x = position[0]
        y = position[1]
        
        if(x >= 0 and x < config.GRID_SIZE and y >= 0 and y < config.GRID_SIZE):
            return True
        return False