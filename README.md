# Collision Simulator in Realtime Graphs

This project simulates collisions between balls in a 2D space using Pygame and Pymunk, and visualizes the collision data in real-time using Matplotlib.

## Features

- Simulates collisions between multiple balls with random initial positions and velocities.
- Displays the simulation using Pygame.
- Plots the number of collisions and average collisions per second in real-time using Matplotlib.

## Requirements

- Python 3.x
- Pygame
- Pymunk
- Matplotlib

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/sttzia/Collision-Simulator-in-Realtime-Graphs--CoPilot-GitHub-
   cd Collision-Simulator-in-Realtime-Graphs--CoPilot-GitHub-
   ```

2. Install the required packages:
   ```sh
   pip install pygame pymunk matplotlib
   ```

## Usage

Run the simulation:

```sh
python Simulating_Collisions.py
```

## How It Works

- The `Ball` class represents a ball in the simulation with properties like position, velocity, and size.
- The `create_segment` function creates static boundary segments to contain the balls.
- The `collision_handler` function increments the collision count whenever a collision occurs.
- The `run_pygame` function runs the Pygame simulation in a separate thread, displaying the balls and collision statistics.
- The Matplotlib `FuncAnimation` updates the collision data plots in real-time.

## Visualization

The simulation window displays:

- The balls moving and colliding within the boundaries.
- The total number of collisions.
- The average collisions per second, minute, and hour.

The Matplotlib window displays:

- A plot of the number of collisions over time.
- A plot of the average collisions per second over time.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
