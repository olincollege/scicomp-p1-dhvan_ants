import numpy as np
import pytest
from ant import Ant
import config

@pytest.fixture
def clean_grid():
    return np.zeros((config.GRID_SIZE, config.GRID_SIZE))

def test_fork_algorithm_rule_a_momentum(clean_grid):
    """
    Paper Rule (a): 'Continue moving forward if the trail continues straight ahead.'
    Even if the side branch is STRONGER, momentum wins.
    """
    # 1. Setup Ant facing EAST at (100, 100)
    ant = Ant((100, 100))
    ant.direction = (0, 1) # (dy, dx) -> (0, 1) is East
    
    # 2. Setup Pheromones
    # Straight ahead (East) -> (100, 101)
    clean_grid[100, 101] = 5.0
    
    # Front-Left (NE) -> (99, 101) - Make this HUGE
    clean_grid[99, 101] = 1000.0 
    
    # 3. Check decision
    chosen_dir = ant.check_for_trail(clean_grid)
    
    # Should choose (0, 1) [Straight] because index 0 had > 0 pheromone
    assert chosen_dir == (0, 1), "Ant failed Rule A: Should prioritize straight momentum over strong side trail."

def test_fork_algorithm_rule_c_strongest_branch(clean_grid):
    """
    Paper Rule (c): 'Follow the stronger of the two branches.'
    If straight is empty, pick the winner between Left/Right.
    """
    # 1. Setup Ant facing EAST
    ant = Ant((100, 100))
    ant.direction = (0, 1)
    
    # 2. Setup Pheromones
    # Straight ahead is EMPTY
    clean_grid[100, 101] = 0.0
    
    # Front-Right (SE) -> (101, 101) - Weak
    clean_grid[101, 101] = 10.0
    
    # Front-Left (NE) -> (99, 101) - Strong
    clean_grid[99, 101] = 50.0
    
    # 3. Check decision
    chosen_dir = ant.check_for_trail(clean_grid)
    
    # Should pick NE (-1, 1)
    # Note: Validate your vector math here. (99, 101) - (100, 100) = (-1, 1)
    assert chosen_dir == (-1, 1), "Ant failed Rule C: Should pick the stronger branch."

def test_fork_algorithm_rule_b_ambiguity(clean_grid):
    """
    Paper Rule (b): 'Move as if exploring if both branches are of equal concentration.'
    """
    ant = Ant((100, 100))
    ant.direction = (0, 1) # East
    
    # Straight empty
    clean_grid[100, 101] = 0.0
    
    # Left and Right are EQUAL
    clean_grid[101, 101] = 20.0
    clean_grid[99, 101] = 20.0
    
    chosen_dir = ant.check_for_trail(clean_grid)
    
    # Should return (0,0) which triggers the random walk logic in move()
    assert chosen_dir == (0, 0), "Ant failed Rule B: Should return (0,0) on ambiguous fork."

def test_relative_direction_rotation():
    """
    Sanity check on the math helper. 
    If I face North, 'Front' is index 0.
    If I face East, 'Front' is index 2 (in the global list).
    """
    ant = Ant((0,0))
    
    # Facing North (0, -1) which is index 0 in VALID_DIRECTIONS
    ant.direction = (0, -1)
    rels = ant.get_relative_directions(0)
    assert rels[0] == (0, -1), "Relative 0 should be North when facing North"
    
    # Facing East (1, 0) which is index 2 in VALID_DIRECTIONS
    ant.direction = (1, 0)
    rels = ant.get_relative_directions(2)
    assert rels[0] == (1, 0), "Relative 0 should be East when facing East"
    # Check that 'Left' (Index 7 relative) is correct
    # If facing East, Left is North-East or North? 
    # Global: N, NE, E, SE, S, SW, W, NW
    # Rotated: E, SE, S, SW, W, NW, N, NE
    # Index 7 is NE.
    assert rels[7] == (1, -1)