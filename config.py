# config.py

# Parameters for the Ant Trail Formation simulation.
# All values are based on Watmough & Edelstein-Keshet (1995) to reproduce Figure 3.

# Environment

# The paper uses a 256x256 grid for all experiments.
GRID_SIZE = 256

# Simulation duration. Figure 3 shows the state at t=1500.
TIMESTEPS = 1500


# Ant Behavior

# Fidelity (phi): Probability (0-255) that an ant follows a trail.
# 255 = High Fidelity (Fig 3a)
# 251 = Medium Fidelity (Fig 3b)
# 247 = Low Fidelity (Fig 3c)
FIDELITY = 255

# Deposition Rate (tau): Pheromone added per step.
# A value of 8 matches the standard run in Figure 3.
DEPOSITION_RATE = 8

# Evaporation Rate: Pheromone removed per step per cell.
EVAPORATION_RATE = 1

# Spawning 

# Initial Burst: Number of ants released at t=0.
# The text says "one per iteration" (set this to 0 for strict adherence).
# However, to actually get the density seen in Figure 3 within 1500 steps, 
# you need a burst to kickstart the trails.
INITIAL_BURST_SIZE = 0

# Stop adding ants after this timestep.
# Prevents the grid from becoming a chaotic mess if running longer than the paper's 1500 steps.
# Also neccessary to replicate the papers numbers for number of ants at 1500 steps
TIMESTEP_STOP = 750


# Movement (Turning Kernel) 

# Probability distribution for random turns when exploring.
# Values from Figure 2 caption.
# [0]: +/- 45 deg
# [1]: +/- 90 deg
# [2]: +/- 135 deg
# [3]: 180 deg (U-Turn)
# The leftover probability (1.0 - sum) is for moving Straight (0 deg).
TURNING_KERNEL = [
    0.360,
    0.047,
    0.008,
    0.004
]