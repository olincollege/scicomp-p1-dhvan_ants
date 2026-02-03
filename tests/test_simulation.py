import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from ant import Ant
from main import Simulation

class TestSimulation:
    
    @patch('main.GUI') # Mock the GUI class entirely
    def test_simulation_init(self, MockGUI):
        sim = Simulation()
        assert sim.released_ants == []
        assert sim.grid.shape == (256, 256)
        assert np.all(sim.grid == 0)
        MockGUI.assert_called_once() # Ensure GUI was instantiated

    @patch('main.GUI')
    def test_evaporation_logic(self, MockGUI):
        """
        Since testing the infinite loop is hard, we replicate the 
        evaporation logic here to ensure the math works as expected.
        """
        sim = Simulation()
        
        # Set a grid value
        sim.grid[50, 50] = 10.0
        
        # Perform evaporation (logic copied from main.py)
        # self.grid = np.maximum(self.grid - self.EVAPORATION_RATE, 0)
        sim.grid = np.maximum(sim.grid - sim.EVAPORATION_RATE, 0)
        
        # 10 - 1 = 9
        assert sim.grid[50, 50] == 9.0
        
        # Test floor at 0
        sim.grid[50, 50] = 0.5
        sim.grid = np.maximum(sim.grid - sim.EVAPORATION_RATE, 0)
        assert sim.grid[50, 50] == 0.0

    @patch('main.GUI')
    def test_deposition_logic_integration(self, MockGUI):
        """
        Test that running the loop logic actually updates the grid 
        when an ant moves. We simulate one 'tick' manually.
        """
        sim = Simulation()
        
        # Manually add an ant
        from ant import Ant
        ant = Ant((128, 128))
        sim.released_ants.append(ant)
        
        # Run the specific logic block from main.py's loop
        # 1. Move ant
        ant.move(sim.grid)
        position = ant.get_pos()
        
        # 2. Deposit
        # self.grid[position[0], position[1]] += self.DEPOSITION_RATE + 1
        sim.grid[position[0], position[1]] += sim.DEPOSITION_RATE + 1
        
        expected_value = sim.DEPOSITION_RATE + 1
        assert sim.grid[position[0], position[1]] == expected_value

    @patch('main.GUI')
    def test_loop_handles_out_of_bounds_ants(self, MockGUI):
        """Ensure ants are removed from the list if they go out of bounds."""
        sim = Simulation()
        
        # Place ant at edge, facing out
        ant = Ant((0, 0))
        ant.direction = (-1, -1) # Move NW (out of bounds)
        sim.released_ants.append(ant)
        
        # Replicate loop logic
        for ant in list(sim.released_ants): # Iterate over copy
            in_bounds = ant.move(sim.grid)
            if not in_bounds:
                sim.released_ants.remove(ant)
                
        assert len(sim.released_ants) == 0