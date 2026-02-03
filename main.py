# main.py

from ant import Ant
from gui import GUI
import numpy as np
import time

class Simulation:
    DEPOSITION_RATE = 8
    EVAPORATION_RATE = 1
    
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
            for ant in self.released_ants[:]:
                in_bounds = ant.move(self.grid)
                if(not in_bounds): 
                    self.released_ants.remove(ant)
                    continue
                position = ant.get_pos()
                ant_pos.append(position)
                self.grid[position[0], position[1]] += self.DEPOSITION_RATE + 1

            self.grid = np.maximum(self.grid - self.EVAPORATION_RATE, 0)                
                        
            running = self.gui.loop(ant_pos, self.grid)
            tick += 1
            time.sleep(0.01)
            
        self.gui.quit_gui()
        
        
if __name__ == "__main__":
    sim = Simulation()
    sim.loop()