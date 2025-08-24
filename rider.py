# rider.py
class Rider:
    def __init__(self, rider_id, start_location, destination):
        self.id = rider_id
        self.start_location = start_location
        self.destination = destination

        # instrumentation (for rubric: request, pickup, dropoff times)
        self.status = "waiting"      # waiting, in_car, completed
        self.request_time = None
        self.pickup_time = None
        self.dropoff_time = None

        # derived metrics filled by simulation
        self.wait_time = 0.0
        self.trip_duration = 0.0

    def request_ride(self, t):
        self.status = "waiting"
        self.request_time = t

    def get_picked_up(self, t):
        self.status = "in_car"
        self.pickup_time = t

    def complete_ride(self, t):
        self.status = "completed"
        self.dropoff_time = t

    def is_waiting(self):
        return self.status == "waiting"

    def is_in_car(self):
        return self.status == "in_car"

    def is_completed(self):
        return self.status == "completed"

    def __repr__(self):
        return f"Rider(id={self.id}, start={self.start_location}, dest={self.destination}, status='{self.status}')"
