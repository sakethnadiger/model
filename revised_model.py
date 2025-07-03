import math
import time
import copy
import random

class Plane():
    def __init__(self, id, location, status):
        self.id = id
        self.location = location
        self.status = status
        
    def get_id(self):
        return self.id
    
    def set_location(self, new_location):
        self.location = new_location
    
    def get_location(self):
        return self.location
    
    def set_status(self, new_status):
        self.status = new_status
    
    def get_status(self):
        return self.status


turnover = 120  # minutes

plane1 = Plane(1, "X", "idle")
plane2 = Plane(2, "X", "idle")
plane3 = Plane(3, "X", "idle")

flights = [
    {"id": "fl1", "origin": "X", "destination": "Y", "departure": "0600", "arrival": "0800", "duration": 120, "plane_number": plane1, "delay": 0},
    {"id": "fl2", "origin": "X", "destination": "Z", "departure": "0830", "arrival": "1000", "duration": 90, "plane_number": plane2, "delay": 0},
    {"id": "fl3", "origin": "Y", "destination": "X", "departure": "1000", "arrival": "1130", "duration": 90, "plane_number": plane1, "delay": 0},
    {"id": "fl4", "origin": "X", "destination": "W", "departure": "0845", "arrival": "1015", "duration": 90, "plane_number": plane3, "delay": 0}
]

# Add original departure and num_swaps field
for flight in flights:
    flight["original_departure"] = flight["departure"]
    flight["num_swaps"] = 0  # Limit swaps per flight

def hourToMin(hhmm):
    return int(hhmm[:2]) * 60 + int(hhmm[2:])

def minToHHMM(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}{mins:02d}"

def delay_cost(delay):
    if delay <= 30:
        return 0
    elif delay <= 180:
        return (delay - 30) * 20
    else:
        return int(20 * 150 + 200 * (math.exp(0.05 * (delay - 180)) - 1))



def find_available_swap(delayed_flight):
    current_plane = delayed_flight["plane_number"]
    for f in flights:
        if f["id"] == delayed_flight["id"]:
            continue
        if delayed_flight.get("swapped") or f.get("swapped"):
            continue
        # Check swap count limit
        if delayed_flight["num_swaps"] >= 1 or f["num_swaps"] >= 1:
            continue
        if current_plane.get_location() == f["plane_number"].get_location() and current_plane.get_id() != f["plane_number"].get_id():
            if current_plane.get_status() == "idle" and f["plane_number"].get_status() == "idle":
                time_diff = hourToMin(f["departure"]) - hourToMin(delayed_flight["original_departure"])
                if 0 <= time_diff <= turnover:
                    if delayed_flight["delay"] > f["delay"]:
                        return f
    return None

# Beta distribution which produces a random number between 0 and max_val but heavily weights it towards smaller numbers, realistic for delays as smaller delays more likely than larger delays
def weighted_random_beta(alpha=2, beta=12, max_val=400):
    val = random.betavariate(alpha, beta)
    return int(val * max_val)

def h(flights, iterations = 10000):
    flights_copy = copy.deepcopy(flights)
    
    def total_cost(flights):
        return sum(delay_cost(flight["delay"]) for flight in flights)
    
    original_cost = total_cost(flights)
    
    total = 0

    for _ in range(iterations):
        potential_swap_flights = copy.deepcopy(flights_copy)
        random_delay = weighted_random_beta()
        random_flight = random.choice(flights)
        random_flight["delay"] = random_delay
        
        # choose two random flights from the list
        F1, F2 = random.sample(potential_swap_flights, 2)
        
        # check if they are valid to be swapped
        if F1["plane_number"].get_location() == F2["plane_number"].get_location() and F1["plane_number"].get_id() != F2["plane_number"].get_id():
            if F1["plane_number"].get_status() == "idle" and F2["plane_number"].get_status() == "idle":
                swap_flights(F1, F2)
                
                potential_cost = total_cost(potential_swap_flights)
                
                total += potential_cost
            else:
                total += original_cost
        else:
            total += original_cost
    
    mean_cost = total / iterations
    mean_difference = original_cost - mean_cost
    
    return mean_cost, mean_difference
                    

def swap_flights(delayed_flight, swap_flight):
    if delayed_flight["num_swaps"] >= 1 or swap_flight["num_swaps"] >= 1:
        return  # Prevent multiple swaps per flight

    original_plane = delayed_flight["plane_number"]
    delayed_flight["plane_number"] = swap_flight["plane_number"]
    swap_flight["plane_number"] = original_plane
    delayed_flight["delay"] = 0
    delayed_flight["swapped"] = True
    swap_flight["swapped"] = True

    delayed_flight["num_swaps"] += 1
    swap_flight["num_swaps"] += 1

    print(f"Swap occurred: Flight {delayed_flight['id']} swapped with Flight {swap_flight['id']}")

    simulate_delay(0, delayed_flight["id"])
    new_delay = max(0, int(hourToMin(delayed_flight["arrival"]) + 1.1 * turnover - hourToMin(swap_flight["departure"])))
    simulate_delay(new_delay, swap_flight["id"])

def check_possible_swap(flight_id, delay):
    for flight in flights:
        if flight["id"] == flight_id and not flight.get("swapped"):
            swap_flight = find_available_swap(flight)
            if swap_flight:
                swap_flights(flight, swap_flight)
                return True
    return False

def simulate_delay(delay, flight_id):
    for i, flight in enumerate(flights):
        if flight["id"] == flight_id:
            flight["delay"] += delay
            departure_min = hourToMin(flight["departure"]) + delay
            arrival_min = hourToMin(flight["arrival"]) + delay
            flight["departure"] = minToHHMM(departure_min)
            flight["arrival"] = minToHHMM(arrival_min)
            print(f"Flight {flight['id']} delayed by {flight['delay']} minutes")
            plane = flight["plane_number"]
            for j in range(i + 1, len(flights)):
                if flights[j]["plane_number"] == plane:
                    if hourToMin(flight["arrival"]) + turnover > hourToMin(flights[j]["departure"]):
                        next_delay = hourToMin(flight["arrival"]) + turnover - hourToMin(flights[j]["departure"])
                        simulate_delay(next_delay, flights[j]["id"])
                    break
            break


time_range = 24 * 60

for t in range(time_range):
    for f in flights:
        f["swapped"] = False

    if t == 0:
        simulate_delay(40, "fl2")

    for flight in flights:
        if t == hourToMin(flight["original_departure"]) and flight["delay"] > 0:
            check_possible_swap(flight["id"], flight["delay"])

        if t == hourToMin(flight["departure"]):
            print(f"[{flight['departure']}] : Flight {flight['id']} departed from {flight['origin']} to {flight['destination']} plane {flight['plane_number'].get_id()}")
            flight['plane_number'].set_status("inflight")

        if t == hourToMin(flight["arrival"]):
            print(f"[{flight['arrival']}] : Flight {flight['id']} arrived to {flight['destination']} from {flight['origin']} plane {flight['plane_number'].get_id()}")
            flight['plane_number'].set_location(flight['destination'])
            flight['plane_number'].set_status("idle")
            print(f"Plane {flight['plane_number'].get_id()} new location set to {flight['plane_number'].get_location()}")

    # time.sleep(0.01)

total_cost = 0
for flight in flights:
    cost = delay_cost(flight["delay"])
    print(f"Flight {flight['id']}: Delay {flight['delay']} mins → Cost: ${cost}")
    total_cost += cost
print(f"\nTotal Cost: ${total_cost}")

