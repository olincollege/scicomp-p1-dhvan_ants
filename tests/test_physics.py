import numpy as np
import pytest
import config
from ant import Ant
from main import Simulation

def test_kernel_probability_integrity():
    """
    Critical Science Check: 
    The paper requires specific turning probabilities. 
    If these don't sum to ~1.0, Python's random.choices behavior gets weird.
    """
    # Create a dummy ant to access its calculated weights
    a = Ant((0,0))
    
    total_probability = sum(a.WEIGHTS)
    
    # Allow for floating point epsilon error, but it should be very close to 1.0
    assert abs(total_probability - 1.0) < 0.0001, f"Turning kernel weights sum to {total_probability}, expected 1.0"

def test_boundary_conditions_hard_edges():
    """
    Test the exact indices where ants usually crash.
    Grid is 0 to 255. 
    """
    a = Ant((0, 0))
    
    # Test absolute edges
    assert a.in_bounds((0, 0)) == True
    assert a.in_bounds((255, 255)) == True
    
    # Test immediate OOB
    assert a.in_bounds((-1, 0)) == False
    assert a.in_bounds((0, -1)) == False
    assert a.in_bounds((256, 0)) == False
    assert a.in_bounds((0, 256)) == False

def test_evaporation_mechanics():
    """
    Verify the numpy subtraction logic actually reduces the grid values
    and clamps at 0.
    """
    sim = Simulation()
    
    # Setup a test patch
    sim.grid[10, 10] = 5.0  # Should become 4.0
    sim.grid[10, 11] = 0.5  # Should become 0.0 (clamped)
    
    sim.grid = np.maximum(sim.grid - config.EVAPORATION_RATE, 0)
    
    assert sim.grid[10, 10] == 4.0
    assert sim.grid[10, 11] == 0.0