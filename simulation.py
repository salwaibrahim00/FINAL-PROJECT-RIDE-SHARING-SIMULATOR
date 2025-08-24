import heapq
import random
import os
import matplotlib.pyplot as plt  # Library to create plots for visualization
from quadtree import Quadtree, Rectangle
from dijkstra import find_shortest_path
from rider import Rider
from graph import Graph


# Car class
class Car:
    def __init__(self, car_id, start_position):
        self.car_id = car_id  # Unique identifier for the car
        self.position = start_position  # Current (x, y) position
        self.available = True  # True if the car can take a ride
        self.rides_completed = 0  # Counter of completed trips

    def __repr__(self):
        # Helpful for printing car info during debugging
        return f"Car({self.car_id}, pos={self.position}, available={self.available})"


# RideSharingSimulation class
class RideSharingSimulation:
    def __init__(self, max_time=100, mean_arrival_time=5, map_file='map.csv'):
        # Core simulation parameters
        self.max_time = max_time  # Total time to run the simulation
        self.mean_arrival_time = mean_arrival_time  # Average time between rider requests
        self.current_time = 0  # Tracks the simulation's current time
        self.next_rider_id = 1  # Unique ID counter for riders

        # Load city map into Graph
        self.graph = Graph()
        map_file_path = os.path.join(os.path.dirname(__file__), map_file)
        self.graph.load_map_data(map_file_path)  # Load CSV map data into graph

        # Setup Quadtree for fast spatial queries
        min_x, min_y, max_x, max_y = self.graph.get_bounds()
        boundary = Rectangle(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
        # Quadtree helps quickly find nearest available cars for riders
        self.quadtree = Quadtree(boundary, capacity=4)

        # Initialize simulation state
        self.cars = []  # List to store Car objects
        self.events = []  # Min-heap priority queue for events
        self.completed_rides = []  # Keep track of completed rides
        self.trip_data = []  # Detailed trip data for metrics
        self.total_riders_generated = 0  # Count of riders generated

    # Add a car to simulation
    def add_car(self, car):
        self.cars.append(car)
        self.quadtree.insert(car.position, car)  # Add car to spatial index

    # Generate a rider request randomly
    def generate_rider_request(self):
        min_x, min_y, max_x, max_y = self.graph.get_bounds()
        # Random start and end positions within map bounds
        start_x = random.uniform(min_x, max_x)
        start_y = random.uniform(min_y, max_y)
        end_x = random.uniform(min_x, max_x)
        end_y = random.uniform(min_y, max_y)

        rider = Rider(self.next_rider_id, (start_x, start_y), (end_x, end_y))
        self.total_riders_generated += 1
        self.next_rider_id += 1
        return rider

    # Main event loop
    def run(self):
        # Start simulation with first rider request at time 0
        heapq.heappush(self.events, (0, "rider_request", None))

        # Process events until no events left or max_time is reached
        while self.events and self.current_time < self.max_time:
            time, event_type, data = heapq.heappop(self.events)  # Get next event
            if time > self.max_time:
                break  # Ignore events beyond simulation end time
            self.current_time = time

            # Dispatch event to correct handler
            if event_type == "rider_request":
                self.handle_rider_request()
            elif event_type == "pickup_arrival":
                car, rider = data
                self.handle_pickup_arrival(car, rider)
            elif event_type == "ride_complete":
                car, rider = data
                self.handle_ride_complete(car, rider)

    # Handle a new rider request
    def handle_rider_request(self):
        rider = self.generate_rider_request()
        rider.request_time = self.current_time

        # Use Quadtree to find nearest available cars (efficient search)
        k_nearest = self.quadtree.find_k_nearest(rider.start_location, k=5)

        best_car = None
        best_time = float('inf')

        # Evaluate travel time to rider using Dijkstra for each candidate car
        for car_location in k_nearest:
            car = self.quadtree.get_car_at_location(car_location)
            if car and car.available:
                car_node = self.graph.find_nearest_vertex(car.position)
                rider_node = self.graph.find_nearest_vertex(rider.start_location)
                _, travel_time = find_shortest_path(self.graph, car_node, rider_node)
                if travel_time < best_time:
                    best_time = travel_time
                    best_car = car

        if best_car:
            # Assign car and remove temporarily from quadtree (unavailable)
            self.quadtree.remove(best_car.position)
            best_car.available = False

            # Schedule pickup and dropoff
            pickup_time = self.current_time + best_time
            pickup_node = self.graph.find_nearest_vertex(rider.start_location)
            dest_node = self.graph.find_nearest_vertex(rider.destination)
            _, ride_duration = find_shortest_path(self.graph, pickup_node, dest_node)
            dropoff_time = pickup_time + ride_duration

            # Track wait time and trip duration
            rider.wait_time = pickup_time - self.current_time
            rider.trip_duration = ride_duration

            # Add events to priority queue
            heapq.heappush(self.events, (pickup_time, "pickup_arrival", (best_car, rider)))
            heapq.heappush(self.events, (dropoff_time, "ride_complete", (best_car, rider)))

        # Schedule next rider dynamically (Poisson process)
        if self.current_time < self.max_time:
            next_request_time = self.current_time + random.expovariate(1.0 / self.mean_arrival_time)
            if next_request_time < self.max_time:
                heapq.heappush(self.events, (next_request_time, "rider_request", None))

    # Handle pickup arrival
    def handle_pickup_arrival(self, car, rider):
        car.position = rider.start_location  # Update car location
        print(f"TIME {self.current_time:.2f}: Car {car.car_id} picked up Rider {rider.id}")

    # Handle ride completion
    def handle_ride_complete(self, car, rider):
        car.position = rider.destination
        car.available = True
        car.rides_completed += 1

        # Save trip data for later analysis
        self.trip_data.append({
            'rider_id': rider.id,
            'car_id': car.car_id,
            'wait_time': rider.wait_time,
            'trip_duration': rider.trip_duration,
            'completion_time': self.current_time
        })
        self.completed_rides.append((rider.id, car.car_id, self.current_time))
        self.quadtree.insert(car.position, car)  # Car becomes available again

        # Print event for clarity
        print(f"TIME {self.current_time:.2f}: Rider {rider.id} dropped off by Car {car.car_id}")

    # Calculate simulation metrics
    def calculate_metrics(self):
        if not self.trip_data:
            # If no rides completed, return zero metrics
            return {
                "total_trips": 0,
                "total_riders_generated": self.total_riders_generated,
                "avg_wait_time": 0,
                "avg_trip_duration": 0,
                "rides_per_car": {car.car_id: car.rides_completed for car in self.cars},
                "driver_utilization": {car.car_id: 0 for car in self.cars}
            }

        total_rides = len(self.trip_data)
        avg_wait = sum(trip['wait_time'] for trip in self.trip_data) / total_rides
        avg_duration = sum(trip['trip_duration'] for trip in self.trip_data) / total_rides
        rides_per_car = {car.car_id: car.rides_completed for car in self.cars}

        # Driver utilization = fraction of time car was busy
        driver_utilization = {}
        for car in self.cars:
            busy_time = sum(trip['trip_duration'] for trip in self.trip_data if trip['car_id'] == car.car_id)
            driver_utilization[car.car_id] = busy_time / self.max_time

        return {
            "total_trips": total_rides,
            "total_riders_generated": self.total_riders_generated,
            "avg_wait_time": avg_wait,
            "avg_trip_duration": avg_duration,
            "rides_per_car": rides_per_car,
            "driver_utilization": driver_utilization
        }

    # Create a visualization of the simulation
    def create_visualization(self, filename='simulation_summary.png'):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Left plot: city map with final car positions
        for node_id, neighbors in self.graph.adjacency_list.items():
            x1, y1 = self.graph.node_coordinates[node_id]
            for neighbor_id, _ in neighbors:
                x2, y2 = self.graph.node_coordinates[neighbor_id]
                ax1.plot([x1, x2], [y1, y2], 'lightgray', linewidth=0.5)

        car_x = [car.position[0] for car in self.cars]
        car_y = [car.position[1] for car in self.cars]
        ax1.scatter(car_x, car_y, c='red', s=100, marker='s', label='Cars')
        ax1.set_title('Final Car Locations')
        ax1.set_xlabel('X Coordinate')
        ax1.set_ylabel('Y Coordinate')
        ax1.legend()
        ax1.grid(True)

        # Right plot: simulation metrics summary
        metrics = self.calculate_metrics()
        ax2.clear()
        metrics_text = f"""SIMULATION RESULTS

Total Riders: {metrics['total_riders_generated']}
Completed Trips: {metrics['total_trips']}
Avg Wait Time: {metrics['avg_wait_time']:.2f}
Avg Trip Duration: {metrics['avg_trip_duration']:.2f}

RIDES PER CAR:"""
        for car_id, rides in metrics['rides_per_car'].items():
            metrics_text += f"\nCar {car_id}: {rides} rides"
        metrics_text += "\n\nDRIVER UTILIZATION:"
        for car_id, util in metrics['driver_utilization'].items():
            metrics_text += f"\nCar {car_id}: {util:.2%}"

        ax2.text(0.1, 0.9, metrics_text, fontsize=10, verticalalignment='top',
                 fontfamily='monospace', transform=ax2.transAxes)
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')

        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.show()
        print(f"Visualization saved as {filename}")

        return metrics


# === Main block with argparse ===
if __name__ == "__main__":
    import argparse

    # Setup command-line arguments
    parser = argparse.ArgumentParser(description="Run the Ride-Sharing Simulation")
    parser.add_argument("--max-time", type=int, default=100, help="Maximum simulation time")
    parser.add_argument("--mean-arrival-time", type=float, default=5, help="Mean arrival time for riders")
    parser.add_argument("--map-file", type=str, default="map.csv", help="Path to the map CSV file")
    args = parser.parse_args()

    # Initialize simulation with arguments
    sim = RideSharingSimulation(max_time=args.max_time,
    mean_arrival_time=args.mean_arrival_time,
    map_file=args.map_file)

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
