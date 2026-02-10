# gui.py

import pygame
import numpy as np
import config

class GUI:
    """
    Handles the real-time visualization of the simulation.
    
    Renders the discrete grid state using Pygame, mapping pheromone 
    concentrations to visual color gradients (Blue) and ants to agents (Red).
    """
    
    def __init__(self):
        """
        Initializes the Pygame window.
        
        Scales the internal simulation grid by a factor of 3 for visibility 
        on standard displays (256x256 pixels is too small to see details).
        """
        pygame.init()
        self.screen = pygame.display.set_mode((config.GRID_SIZE * 3, config.GRID_SIZE * 3), flags=pygame.HIDDEN)
        self.clock = pygame.time.Clock()
        
    def loop(self, ant_pos = (0, 0), grid = []):
        """
        Executes a single render cycle.
        
        Args:
            ant_pos (list): List of (row, col) tuples for all active ants.
            grid (np.ndarray): The current pheromone concentration matrix.
            
        Returns:
            bool: False if the user closed the window (stopping the sim), True otherwise.
        """
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): 
                pygame.quit()
                return False
            
        self.screen.fill('black')
        # Draw all ants first
        for pos in ant_pos:
            self.draw_ant((pos[0] * 3, pos[1] * 3))
            
        # Draw the pheromone trails on top of the ants
        self.draw_grid(grid)

        pygame.display.flip()
        self.clock.tick(60)
        return True
        
    def quit_gui(self):
        """Clean exit for the display window."""
        pygame.quit()

    def draw_ant(self, position):
        """Renders a single ant as a red circle."""
        pygame.draw.circle(self.screen, "red", position, 4.5)
        
    def draw_grid(self, grid):
        """
        Renders the pheromone field as a heatmap.
        
        Iterates through the grid and maps pheromone concentration to color lightness.
        Dark Blue = Low Concentration -> Bright Blue/White = High Concentration.
        """
        blue = pygame.Color(0, 0, 255)
        
        # Optimize rendering: only draw cells with active pheromone
        # (Drawing 256*256 circles every frame is expensive, but most cells are empty)
        for y, x in np.ndindex(grid.shape):
            value = grid[y, x]
            if(value > 0):
                # Map concentration value to HSL Lightness (0-100).
                # The 0.075 multiplier scales the raw value to a visible range.
                # Cap at 100 to prevent color wrapping errors.
                # light_value = min(100, 0 + (value * 0.075))
                light_value = min(100, 0 + (value * config.GUI_TRAIL_SCALE))
                blue.hsla = (240, 100, light_value, 100)
                # Draw scaled pixel (x3 size)
                pygame.draw.circle(self.screen, blue, (y * 3, x * 3), 3)