from ant import Ant
from gui import GUI
import numpy as np

class Simulation:
    DEPOSITION_RATE = 12
    EVAPORATION_RATE = 4
    def __init__(self):
        self.released_ants: list[Ant] = []
        self.gui = GUI()
        self.grid = np.zeros((256, 256))
        
    def loop(self):
        running = True
        tick = 0
        while running:
            new_ant = Ant((128, 128))
            self.released_ants.append(new_ant)
            
            ant_pos = []
            for ant in self.released_ants:
                in_bounds = ant.move(self.grid)
                if(not in_bounds): continue
                position = ant.get_pos()
                ant_pos.append(position)
                
                self.grid[position[0], position[1]] = self.DEPOSITION_RATE + 1
                
            self.grid = np.maximum(self.grid - 1, 0)
                
                        
            running = self.gui.loop(ant_pos, self.grid)
            tick += 1
            
        self.gui.quit_gui()
        
        
if __name__ == "__main__":
    sim = Simulation()
    sim.loop()