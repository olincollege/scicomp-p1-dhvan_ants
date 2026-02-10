# Project 1: ANTS!
**Author**: Dhvan Shah

**Paper**: Watmough, J. & Edelstein-Keshet, L. (1995). *"Modelling the Formation of Trail Networks by Foraging Ants"*

## Project Overview
This project implements an Agent Based Model to simulate the formation of trails by foraging ants. The simulation explores how simple, local interactions allow a colony to solve complex pathfinding problems without a centralized controller

The main requirement was to replicate **Figure 3** from the source paper, demonstrating the *straightness* of an ant network is inversely related to an individual ant's "fidelity" to the pheromone signal.

### Scientific Background
The model relies on three governing rules derived from the paper:
1. **Pheromone Deposition**: Ants deposit a fixed amount of pheromone at their current location
2. **Evaporation**: Pheromone trails decay linearly over time, creating a feedback loop where only reinforced trails survive
3. **The Fork Algorithm**: When sensing a trail, ants make decision based on these rules:
    - If the trail continues straight, the ant will follow the trail
    - If the trail splits, the ant will follow the stronger branch
    - If the branches are equal, the ant will move as if it was exploring

## Benchmark
The primary objective was to replicate **Figure 3** from the source paper. 

### Benchmark Metrics
1. **Visual**: A distinct "X" pattern emerging from the center
2. **Follower-to-Lost Ratio**: A measure of network efficiency

### Figure 3.a
![Fig 3.a from the source paper](media/F3_a.png)

**Fidelity:** 255 / 256

**Number of Follower Ants:** 468

**Number of Lost Ants:** 32

**F-L Ratio:** 14.625

### Figure 3.b
![Fig 3.b from the source paper](media/F3_b.png)

**Fidelity:** 251 / 256

**Number of Follower Ants:** 396

**Number of Lost Ants:** 89

**F-L Ratio:** 4.449

### Figure 3.c
![Fig 3.c from the source paper](media/F3_c.png)

**Fidelity:** 247 / 256

**Number of Follower Ants:** 297

**Number of Lost Ants:** 91

**F-L Ratio:** 3.264

## Replication

To make sure the randomness of the model is accounted for, but I still get usable numbers, I ran the simulation for each case 10 times, and averaged the F-L ratio to get my final number. The below screenshots are what I consider matching the paper the closest. The rest of the screenshots are in runs/case<1,2,3>

### Case 1

![Case 1 run of my model](media/C1.png)

**Fidelity:** 255 / 256

**Average Number of Follower Ants:** 731.1

**Average Number of Lost Ants:** 49.4

**Average F-L Ratio:** 15.150

### Case 2

![Case 2 run of my model](media/C2.png)

**Fidelity:** 251 / 256

**Average Number of Follower Ants:** 483.6

**Average Number of Lost Ants:** 134.0

**Average F-L Ratio:** 3.628

### Case 3

![Case 3 run of my model](media/C4.png)

**Fidelity:** 247 / 256

**Average Number of Follower Ants:** 381.9

**Average Number of Lost Ants:** 181.7

**Average F-L Ratio:** 2.122


## Initial Burst Hypothesis
While implementing this model, I encountered a significant discrepancy between the paper's text description and its visual results. This required straying from the literal instructions to accurately reproduce the papers results. 

### The Discrepancy
The paper states that ants are released "at a rate of one per iteration"
- At *t = 1500*, a rate of 1 ant per tick implies around 1500 ants (minus boundary losses)
- The caption of figure 3 clearly states that only around 500 ants remained at *t = 1500*
- Running the simulation with strictly 1 ant per tick results in an overcrowded grid. The sheer volume of new agents drowns out the pheromone signals, not only preventing the delicate "X" pattern from appearing within the 1500-step limit, but also resulting in completely different numbers for follower and explorer ants. 
- Whilst the F-L Ratio might still be the same, this discrepancy required some tweaking to the model in order to get the output to match figure 3

### Solution
I hypothesized that the authors of the papers likely primed their grid with a set number of ants. To test this, I implemented an optional Burst mode, where the first tick sends out 120 ants as opposed to just 1. 

### Experiment A: No Burst

### Experiment B: Burst, no limit

### Experiment C: Burst, 1000 tick limit

## Capabilities
- **Variable Fidelity**: Can simulate high vs. low fidelity systems by adjusting `FIDELITY` in `config.py`
- **Scientific Validation**: Includes unit tests `tests/` that verify the fork algorithm and deposition logic (amongst other edge case tests) as specified in the paper
- **Real-Time Visualization**: Uses `Pygame` to render ants and pheromone trails at 60FPS

## Limitations
- **Burst Model**: Makes the assumption that the authors left out a crucial aspect of their model
- **Grid Size**: Limited to a maximum of 512x512 grid size for any reasonable computational speed. Optimizations required to reach bigger grid sizes
- **Color Scale**: Requires manual tuning of pheromone trail color scales in order to match source papers output. Source paper does say they had to do a similar thing though.

## File Structure
- `main.py`: Simulation loop. Handles time-stepping, evaporation and spawning
- `ant.py`: Agent logic. Contains crucial `move()`, `turn()`, `check_for_trail()` methods
- `gui.py`: Visualization. Maps pheromone concentration to a blue gradient, and displays ants as red circles
- `config.py`: Central control file for most scientific parameters
- `tests/`: Unit tests validating logic

## Usage

### Requirements
- Python 3.12+
- `pip install -r requirements.txt`

### Reproducing Figure 3.a
1. Open `config.py`
2. Set `FIDELITY = 255`
3. OPTIONAL, set or unset `RANDOM_SEED`
4. `python main.py`
5. F-L Ratio will print to terminal upon completion (1500 timesteps)

### Running unit tests
1. `pytest`
