import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from ant import Ant

class TestAnt:
    
    @pytest.fixture
    def grid_256(self):
        """Creates an empty 256x256 grid for testing."""
        return np.zeros((256, 256))

    def test_initialization(self):
        ant = Ant((128, 128))
        assert np.array_equal(ant.pos, (128, 128))
        assert ant.mode == Ant.MODE["Explore"]
        assert ant.direction in Ant.VALID_DIRECTIONS

    def test_in_bounds(self):
        """Test boundary detection logic."""
        ant = Ant((0,0))
        
        # Test valid positions
        assert ant.in_bounds((0, 0)) is True
        assert ant.in_bounds((255, 255)) is True
        assert ant.in_bounds((100, 100)) is True

        # Test invalid positions
        assert ant.in_bounds((-1, 0)) is False
        assert ant.in_bounds((0, -1)) is False
        assert ant.in_bounds((256, 0)) is False
        assert ant.in_bounds((0, 256)) is False

    def test_get_relative_directions(self):
        """Test that the direction list rotates correctly."""
        ant = Ant((0,0))
        # Set direction to North (0, -1), which is index 0 in VALID_DIRECTIONS
        ant.direction = (0, -1) 
        idx = Ant.VALID_DIRECTIONS.index(ant.direction)
        
        rels = ant.get_relative_directions(idx)
        
        # The first item should be the current direction
        assert rels[0] == (0, -1)
        # The list should contain all 8 directions
        assert len(rels) == 8

    @patch('random.choices')
    def test_turn_selection(self, mock_choices):
        """Test that turn() returns a direction based on weights."""
        ant = Ant((100, 100))
        ant.direction = (0, -1) # Facing North
        
        # Mock random.choices to return 'South' (0, 1) - index 4
        # Note: In the code, turn logic is stochastic. We force the outcome.
        expected_dir = (0, 1)
        mock_choices.return_value = [expected_dir]
        
        new_dir = ant.turn()
        assert new_dir == expected_dir

    def test_check_for_trail_finds_max(self, grid_256):
        """Test that ant detects high concentration values."""
        ant = Ant((100, 100))
        ant.direction = (0, -1) # Facing North
        
        # Place a "pheromone" trail to the North-East (1, -1)
        # Coordinates: y=99, x=101 (numpy uses [y, x])
        grid_256[101, 99] = 0   # South (relative to ant pos (100,100) looking North? No, grid is [x,y] usually)
        
        # Note: Your code uses grid[pos[0], pos[1]]. 
        # If pos is (x, y), then grid is accessed as [x, y].
        # Ant at 100, 100. NE is (1, -1). New pos: 101, 99.
        target_pos = (101, 99)
        grid_256[target_pos[0], target_pos[1]] = 50.0 
        
        # Logic check:
        # Ant direction is North (0, -1). 
        # get_relative_directions starts at North.
        # It scans neighbors. It should find the 50.0 value.
        
        result_dir = ant.check_for_trail(grid_256)
        
        # Based on logic: if max_concentration > 4.0 and < 60.0
        # It should return the direction of the max concentration.
        assert result_dir == (1, -1)

    def test_check_for_trail_ignores_low_concentration(self, grid_256):
        """Test that ant ignores trails that are too weak."""
        ant = Ant((100, 100))
        ant.direction = (0, -1)
        
        target_pos = (101, 99) # NE
        grid_256[target_pos[0], target_pos[1]] = 2.0 # Too low (threshold is 4.0)
        
        result_dir = ant.check_for_trail(grid_256)
        assert result_dir == (0, 0) # Should return no trail found

    def test_check_for_trail_immediate_front(self, grid_256):
        """Test the logic: if(concentrations[0] > 0): return relative_direction_list[0]"""
        ant = Ant((100, 100))
        ant.direction = (0, -1) # North
        
        # Place trail directly North (100, 99)
        grid_256[100, 99] = 10.0
        
        result_dir = ant.check_for_trail(grid_256)
        assert result_dir == (0, -1)

    @patch('random.choices')
    def test_move_updates_position(self, mock_choices, grid_256):
        """Test the integration of move() logic."""
        ant = Ant((100, 100))
        ant.direction = (1, 0) # East
        
        # Mock random choices to return a specific turn direction if needed
        # And mock the 'fidelity' check in move()
        # choices returns a list. 
        # move() calls choices for fidelity, then potentially turn() calls choices.
        # Let's assume explore mode, no trail.
        
        # We enforce that turn() returns (1, 0) (Keep going East)
        mock_choices.return_value = [(1, 0)] 
        
        ant.move(grid_256)
        
        # Previous (100, 100) + East (1, 0) = (101, 100)
        assert np.array_equal(ant.pos, (101, 100))