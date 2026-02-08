# main.py

from ant import Ant
from gui import GUI
import numpy as np
import random

class Simulation:
    DEPOSITION_RATE = 8
    EVAPORATION_RATE = 1
    
    random.seed("Dhvan Shah")
    
    def __init__(self):
        self.released_ants: list[Ant] = []
        self.gui = GUI()
        self.grid = np.zeros((256, 256))
        
    def loop(self):
        running = True
        tick = 0
        max_timestep = 1500
        
        num_ants_released = 0
        
        for _ in range(120):
            new_ant = Ant((128, 128))
            self.released_ants.append(new_ant)
            num_ants_released += 1
            
        release_interval = 2
        
        while running and tick < max_timestep:
            self.grid = np.maximum(self.grid - self.EVAPORATION_RATE, 0)  
            
            if(tick % release_interval == 0):
                new_ant = Ant((128, 128))
                self.released_ants.append(new_ant)
                num_ants_released += 1
            
            ant_pos = []
            for ant in self.released_ants[:]:
                old_position = ant.get_pos()
                in_bounds = ant.move(self.grid)
                if(not in_bounds): 
                    self.released_ants.remove(ant)
                    continue
                self.grid[old_position[0], old_position[1]] += self.DEPOSITION_RATE + 1
                position = ant.get_pos()
                ant_pos.append(position)

                        
            running = self.gui.loop(ant_pos, self.grid)
            tick += 1
            print(f'\rProgress: {round((tick / max_timestep) * 100, 1)}%', end="")
            # time.sleep(0.01)
            
        print("\nSIMULATION DONE")
        print(f"Average ants released = {num_ants_released / 1500}")
        self.calculate_stats()
        self.gui.quit_gui()
        
    def calculate_stats(self):
        ants_mode = [0, 0]
        for ant in self.released_ants:
            if ant.mode == 0:
                ants_mode[0] += 1
            elif ant.mode == 1:
                ants_mode[1] += 1
                
        F_L_RATIO = ants_mode[1] / ants_mode[0]
        
        print(F_L_RATIO)
        
        print(ants_mode)
        
if __name__ == "__main__":
    sim = Simulation()
    sim.loop()