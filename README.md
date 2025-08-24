# Ride-Sharing Simulator

## About This Project

This is my final project for University of Advancing Technology - a ride-sharing simulator built in Python. The system matches riders with the closest available cars using Quadtree for spatial indexing and Dijkstra's algorithm for finding the shortest paths. You can watch how cars move around, track wait times, and see how efficiently drivers are being used.

## Project Files

```
RiderSimulationfinal/
│── simulation.py      # Main program that runs everything
│── quadtree.py       # Quadtree implementation for finding nearby cars
│── dijkstra.py       # Shortest path algorithm 
│── rider.py          # Rider class
│── graph.py          # City map and graph structure
│── map.csv           # Map data (optional)
│── README.md         # This file
```

## Requirements

- Python 3.8 or higher
- matplotlib library

To install matplotlib:
```
pip install matplotlib
```

## How to Run

1. Open Command Prompt/Terminal
2. Navigate to the project folder:
   ```
   cd "C:\Users\salwa\OneDrive\Desktop\RiderSimulationfinal"
   ```
3. Run the simulation:
   ```
   python simulation.py
   ```

## Optional Settings

You can customize the simulation with these parameters:

```
python simulation.py --max-time 200 --mean-arrival-time 10 --map-file map.csv
```

| Option | What it does | Default |
|--------|-------------|---------|
| `--max-time` | How long the simulation runs | 100 |
| `--mean-arrival-time` | Average time between new riders | 5 |
| `--map-file` | Map file to use | map.csv |

## How It Works

1. Cars are placed on the map at the start
2. Riders appear randomly based on the arrival time setting
3. When a rider requests a ride, the Quadtree quickly finds the 3-5 closest cars
4. Dijkstra's algorithm calculates the fastest route for each potential car
5. The system assigns the closest car to the rider
6. Pickup and dropoff events are scheduled automatically
7. The simulation tracks metrics like wait time and driver utilization throughout


## Visualization

The simulation creates a file called `simulation_summary.png` that shows:
- **Left side**: Car positions on the map
- **Right side**: Summary metrics including:
  - Average wait time
  - Trip duration
  - Number of rides per car
  - Driver utilization percentage

## Key Features

- Fast car-rider matching using Quadtree spatial indexing
- Optimal route calculation with Dijkstra's algorithm
- Real-time tracking of simulation metrics
- Visual output showing system performance
- Configurable simulation parameters

## Performance Metrics Tracked

- **Wait Time**: How long riders wait for their car to arrive
- **Trip Duration**: Total time from pickup to dropoff
- **Driver Utilization**: Percentage of time drivers are busy vs idle
- **Rides per Car**: Distribution of rides across the fleet

## Technical Implementation

The simulation uses an event-driven approach where each pickup and dropoff is scheduled as an event. The Quadtree data structure allows for efficient O(log n) nearest neighbor searches, while Dijkstra's algorithm ensures we always find the shortest path between any two points on the map.

---

**Author:** Salwa Ibrahim  
**University:** University of Advancing Technology  
**Course:** Final Project
