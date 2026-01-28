import pygame
import numpy as np

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((256 * 3, 256 * 3))
        self.clock = pygame.time.Clock()
        
    def loop(self, ant_pos = (0, 0), grid = []):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): 
                pygame.quit()
                return False
            
        self.screen.fill('black')
        for pos in ant_pos:
            self.draw_ant((pos[0] * 3, pos[1] * 3))
            
        self.draw_grid(grid)

        pygame.display.flip()
        self.clock.tick(60)
        return True
        
    def quit_gui(self):
        pygame.quit()

    def draw_ant(self, position):
        pygame.draw.circle(self.screen, "red", position, 3)
        
    def draw_grid(self, grid):
        blue = pygame.Color(0, 0, 255)
        for y, x in np.ndindex(grid.shape):
            value = grid[y, x]
            if(value > 0):
                light_value = 80 - (value * 5)
                blue.hsla = (240, 100, light_value, 100)
                pygame.draw.circle(self.screen, blue, (y * 3, x * 3), 3)
        
