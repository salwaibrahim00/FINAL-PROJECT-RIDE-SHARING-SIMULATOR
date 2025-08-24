# # main.py
import os
from simulation import RideSharingSimulation
from simulation import Car

# Initialize simulation

sim = RideSharingSimulation(max_time=100, mean_arrival_time=5, map_file='map.csv')

# Add cars at specific positions on the map
sim.add_car(Car(1, (0, 0)))   # Top-left
sim.add_car(Car(2, (8, 0)))   # Top-right
sim.add_car(Car(3, (0, 6)))   # Bottom-left
sim.add_car(Car(4, (4, 4)))   # Center
sim.add_car(Car(5, (8, 6)))   # Bottom-right

# Run the simulation

sim.run()

# Print summary metrics
metrics = sim.calculate_metrics()
print("\n--- SIMULATION SUMMARY ---")
print(f"Total riders generated: {metrics['total_riders_generated']}")
print(f"Completed trips: {metrics['total_trips']}")
print(f"Average wait time: {metrics['avg_wait_time']:.2f}")
print(f"Average trip duration: {metrics['avg_trip_duration']:.2f}\n")

print("Driver utilization per car:")
for car_id, util in metrics['driver_utilization'].items():
    print(f"Car {car_id}: {util*100:.2f}%")

print(f"\nAverage driver utilization: {sum(metrics['driver_utilization'].values())/len(metrics['driver_utilization'])*100:.2f}%")

# Optional: create visualization

sim.create_visualization("simulation_summary.png")
