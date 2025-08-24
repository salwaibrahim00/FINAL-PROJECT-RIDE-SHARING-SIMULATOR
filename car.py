# car.py


# Constants
TRAVEL_SPEED_FACTOR = 0.5  # Time per unit distance (for placeholder navigation)

class Car:
   def __init__(self, car_id, location):
       """
       Initialize a car for the ride-sharing simulation.
       
       Args:
           car_id: Unique identifier for the car
           location: Tuple (x, y) representing car's current position
       """
       self.id = car_id
       self.location = location
       self.route = []         # Planned path to destination
       self.route_time = 0     # Expected travel time for current route
       
       # Status control - tracks car's current operational state
       self.status = "available"  # available, en_route_to_pickup, en_route_to_destination
       self.assigned_rider = None  # Link to rider when dispatched

   def calculate_route(self, destination, graph=None):
       """
       Calculate route to destination using pathfinding algorithm.
       Currently uses Manhattan distance as placeholder for realistic pathfinding.
       
       Args:
           destination: Tuple (x, y) representing target location
           graph: Graph object for pathfinding (None for prototype)
       """
       if graph:
           # For final version with your graph and pathfinding:
           # Use Dijkstra's algorithm or A* for optimal routing
           pass
       
       # Placeholder calculation for prototype (Manhattan distance)
       # In real implementation, this would use actual road network
       distance = abs(self.location[0] - destination[0]) + abs(self.location[1] - destination[1])
       self.route_time = distance * TRAVEL_SPEED_FACTOR
       self.route = [self.location, destination]  # Simple two-point route

   def is_available(self):
       """
       Check if car is available for assignment.
       Used by simulation to filter available fleet for dispatch.
       """
       return self.status == "available"

   def assign_rider(self, rider):
       """
       Assign a rider to this car and set status.
       Transitions car from available to pickup mode.
       """
       self.assigned_rider = rider
       self.status = "en_route_to_pickup"
       # Calculate route to pickup location for time estimation
       self.calculate_route(rider.start_location)

   def complete_pickup(self):
       """
       Mark that car has completed pickup.
       Transitions from pickup phase to dropoff phase of trip.
       """
       if self.assigned_rider:
           # Move car to rider's pickup location
           self.location = self.assigned_rider.start_location
           self.status = "en_route_to_destination"
           # Calculate route to final destination
           self.calculate_route(self.assigned_rider.destination)

   def complete_dropoff(self):
       """
       Mark that car has completed dropoff.
       Returns car to available state and clears assignment.
       """
       if self.assigned_rider:
           # Move car to dropoff location
           self.location = self.assigned_rider.destination
           # Reset car to available state
           self.status = "available"
           self.assigned_rider = None
           self.route = []
           self.route_time = 0

   def __str__(self):
       """
       String representation of the car for debugging and logging.
       Shows current status and assignment information.
       """
       rider_info = f" (assigned to Rider {self.assigned_rider.id})" if self.assigned_rider else ""
       return f"Car {self.id} at {self.location} - Status: {self.status}{rider_info}"

   def __repr__(self):
       """
       Technical representation of the car for development debugging.
       Provides concise object state information.
       """
       return f"Car(id={self.id}, location={self.location}, status='{self.status}')"