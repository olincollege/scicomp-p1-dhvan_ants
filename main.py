# main.py

from ant import Ant
from gui import GUI
import config
import numpy as np
import random
import pickle
import pygame

class Simulation:    
    """
    Orchestrates the Ant Colony simulation.
    
    Manages the grid environment, ant population, and time-stepping.
    
    Note on Spawning:
    This implementation supports an 'Initial Burst' of ants (configured in config.py).
    While the paper specifies a rate of 'one per iteration', 
    a burst is often necessary to reproduce the density of Figure 3 
    within the 1500-step limit.
    """
    if (config.RANDOM_SEED != None and config.RANDOM_SEED != ""):
        random.seed(config.RANDOM_SEED)
    
    def __init__(self):
        self.released_ants: list[Ant] = []
        self.gui = GUI()
        # Initialize the pheromone grid to zero concentration.
        self.grid = np.zeros((config.GRID_SIZE, config.GRID_SIZE))
        
    def loop(self, screenshot_filename):
        """
        Main execution loop.
        
        Performs the following steps per tick:
        1. Evaporates pheromone linearly (grid - EVAPORATION_RATE).
        2. Spawns new ants based on release settings.
        3. Moves all ants and deposits pheromone.
        4. Updates the GUI.
        """
        running = True
        tick = 0
                        
        # Paper Ambiguity: The text specifies "releasing ants at a rate of one per iteration".
        # However, empirically, the distinct "X" pattern in Figure 3 only emerges 
        # if the environment is primed with a strong initial burst.
        # Without this, the 1500-step limit is too short for a single stream to build the network.
        for _ in range(config.INITIAL_BURST_SIZE):
            new_ant = Ant((config.GRID_SIZE // 2, config.GRID_SIZE // 2))
            self.released_ants.append(new_ant)
            
        
        while running and tick < config.TIMESTEPS:
            # Evaporate BEFORE movement.
            # This ensures ants interact with the most up-to-date grid state for this tick.
            # If we evaporated after, ants would be sensing "old" pheromone that should have decayed.
            self.grid = np.maximum(self.grid - config.EVAPORATION_RATE, 0)  
            
            # Paper Ambiguity: Figure 3 captions show roughly 500 ants total at step 1500.
            # A constant release rate of 1/tick would result in 1500+ ants.
            # To match the visual density of the benchmark, we stop spawning at a cutoff point.
            if(tick < config.TIMESTEP_STOP):
                new_ant = Ant((config.GRID_SIZE // 2, config.GRID_SIZE // 2))
                self.released_ants.append(new_ant)
            
            ant_pos = []
            # Use slice copy [:] to allow removing ants during iteration
            for ant in self.released_ants[:]:
                old_position = ant.get_pos()
                in_bounds = ant.move(self.grid)
                
                # Absorbing boundaries: ants leaving the lattice are removed
                if(not in_bounds): 
                    self.released_ants.remove(ant)
                    continue
                
                # Deposition: Ants add pheromone to their previous location (Rule 2)
                # Adding the deposition rate + 1 here is neccessary due to the immediate
                # evaporation in the next tick (at the top of the loop)
                self.grid[old_position[0], old_position[1]] += config.DEPOSITION_RATE + 1
                position = ant.get_pos()
                ant_pos.append(position)

                        
            running = self.gui.loop(ant_pos, self.grid)
            tick += 1
            print(f'\rProgress: {round((tick / config.TIMESTEPS) * 100, 1)}%', end="")
            # time.sleep(0.01)
            
        print("\nSIMULATION DONE")
        
        if screenshot_filename:
            # We access the 'screen' surface from your GUI instance
            pygame.image.save(self.gui.screen, screenshot_filename)
            print(f"Screenshot saved to {screenshot_filename}")
            
        # self.calculate_stats()
        
        # while running:
        #     running = self.gui.loop(ant_pos, self.grid)
        
        self.gui.quit_gui()
        
        return self.calculate_stats()

        
    def calculate_stats(self):
        """
        Calculates the Followers-to-Lost (F/L) ratio (p. 360).
        
        A higher ratio indicates a stronger, more defined trail network.
        """
        ants_mode = [0, 0]
        for ant in self.released_ants:
            if ant.mode == 0:
                ants_mode[0] += 1
            elif ant.mode == 1:
                ants_mode[1] += 1
                
        if ants_mode[0] == 0:
            F_L_RATIO = 0
        else:
            F_L_RATIO = ants_mode[1] / ants_mode[0]
        
        print(F_L_RATIO)
        
        print(ants_mode)
        
        return (F_L_RATIO, ants_mode)
        
if __name__ == "__main__":
    sim = Simulation()
    print(sim.loop("runs/experiments/ExC.png"))