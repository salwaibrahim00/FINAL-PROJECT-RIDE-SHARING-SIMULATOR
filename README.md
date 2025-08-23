1. Ride-Sharing Simulation 

This is a ride-sharing simulator in Python. Riders request cars, and the system finds the closest available car using Quadtree and Dijkstra's algorithm.

You can see how cars move, track wait times, and check driver utilization.

2. Project Files
RiderSimulationfinal/
│── simulation.py        # Main program
│── quadtree.py          # Quadtree for car locations
│── dijkstra.py          # Shortest path algorithm
│── rider.py             # Rider class
│── graph.py             # City map and graph
│── map.csv              # Map data (optional)
│── README.md            # This file

3.  Requirements

Python 3.8 or higher

Library: matplotlib

Install matplotlib:

pip install matplotlib

 4. How to Run

Open Command Prompt

Go to the project folder:

cd "C:\Users\salwa\OneDrive\Desktop\RiderSimulationfinal"


Run the simulation:

python simulation.py

5.  Optional Settings

You can change simulation settings with these options:

python simulation.py --max-time 200 --mean-arrival-time 10 --map-file map.csv

Option	What it does	Default
--max-time	How long the simulation runs	100
--mean-arrival-time	Average time between riders	5
--map-file	Map file to use	map.csv
6. How It Works

Cars are placed on the map.

Riders appear randomly.

Quadtree finds the 3–5 closest cars fast.

Dijkstra finds the fastest route for each car.

The closest car is assigned to the rider.

Pickup and dropoff events are scheduled automatically.

Metrics like wait time and driver utilization are tracked.

A visualization is created showing car locations and summary metrics.

6. Output
TIME 2.35: Car 1 picked up Rider 1
TIME 5.67: Rider 1 dropped off by Car 1


7. Visualization (simulation_summary.png):

Left: Car positions on the map

Right: Metrics: wait time, trip duration, rides per car, driver utilization


Salwa Ibrahim
University of Advancing Technology
