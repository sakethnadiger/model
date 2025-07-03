import copy
import random
import math


def higher_level_heuristic(iterations):
    turnover = 120

    def hourToMin(hhmm):
        return int(hhmm[:2]) * 60 + int(hhmm[2:])

    def minToHHMM(minutes):
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}{mins:02d}"

    class Plane():
        def __init__(self, id, location, status="idle"):
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

    # simulates the delay by setting one flight to have a delay and pushing the delay to future flights using the same plane
    def simulate_delay(delay, flight_id):
        for i, flight in enumerate(flight_tests):
            if flight["id"] == flight_id:
                flight["delay"] += delay
                departure_min = hourToMin(flight["departure"]) + delay
                arrival_min = hourToMin(flight["arrival"]) + delay
                flight["departure"] = minToHHMM(departure_min)
                flight["arrival"] = minToHHMM(arrival_min)
                plane = flight["plane_number"]
                for j in range(i + 1, len(flight_tests)):
                    if flight_tests[j]["plane_number"] == plane:
                        if hourToMin(flight["arrival"]) + turnover > hourToMin(flight_tests[j]["departure"]):
                            next_delay = hourToMin(flight["arrival"]) + turnover - hourToMin(flight_tests[j]["departure"])
                            simulate_delay(next_delay, flight_tests[j]["id"])
                        break
                break


    # uses a statistical distribution to skew random delay chosen so it is generally lower than 60 mins (~61% chance of being below 60 mins when alpha is 2 and beta is 12).
    # If beta is increased the skew moves more towards the left, producing a smaller delay most of the time, which is more realistic
    def weighted_random_beta(alpha=4, beta=18, max_val=240):
        val = random.betavariate(alpha, beta)
        return int(val * max_val)


    def delay_cost(delay):
        if delay <= 30:
            return 0
        elif delay <= 180:
            return (delay - 30) * 20
        else:
            return int(20 * 150 + 200 * (math.exp(0.05 * (delay - 180)) - 1))


    def swap_flights(flight1, flight2, current_time=0):
        plane1 = flight1["plane_number"]
        plane2 = flight2["plane_number"]
        
        flight1["plane_number"], flight2["plane_number"] = plane2, plane1
        
        flight1["delay"] = 0
        flight2["delay"] = 0
        

        simulate_delay(0, flight1["id"])
        simulate_delay(0, flight2["id"])


    def h(flights, iterations=1000):
        flights_copy = copy.deepcopy(flights)
        
        def total_cost(flights):
            return sum(delay_cost(flight["delay"]) for flight in flights)
        
        original_cost = total_cost(flights)
        total = 0

        for _ in range(iterations):
            potential_swap_flights = copy.deepcopy(flights_copy)
            random_delay = weighted_random_beta()
            random_flight = random.choice(potential_swap_flights)
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

    plane1 = Plane(1, "A")
    plane2 = Plane(2, "B")
    plane3 = Plane(3, "A")
    plane4 = Plane(4, "C")

    global flight_tests
    flight_tests = [
        {"id": "fl1", "origin": "A", "destination": "B", "departure": "0600", "arrival": "0730", "duration": 90, "plane_number": plane1, "delay": 0},
        {"id": "fl2", "origin": "B", "destination": "C", "departure": "0800", "arrival": "0930", "duration": 90, "plane_number": plane1, "delay": 0},
        {"id": "fl3", "origin": "C", "destination": "A", "departure": "1000", "arrival": "1130", "duration": 90, "plane_number": plane1, "delay": 0},

        {"id": "fl4", "origin": "B", "destination": "D", "departure": "0630", "arrival": "0800", "duration": 90, "plane_number": plane2, "delay": 0},
        {"id": "fl5", "origin": "D", "destination": "E", "departure": "0830", "arrival": "1000", "duration": 90, "plane_number": plane2, "delay": 0},

        {"id": "fl6", "origin": "A", "destination": "F", "departure": "0700", "arrival": "0830", "duration": 90, "plane_number": plane3, "delay": 0},
        {"id": "fl7", "origin": "F", "destination": "G", "departure": "0930", "arrival": "1100", "duration": 90, "plane_number": plane3, "delay": 0},

        {"id": "fl8", "origin": "C", "destination": "H", "departure": "0900", "arrival": "1030", "duration": 90, "plane_number": plane4, "delay": 0},
        {"id": "fl9", "origin": "H", "destination": "I", "departure": "1100", "arrival": "1230", "duration": 90, "plane_number": plane4, "delay": 0},
    ]

    for f in flight_tests:
        simulate_delay(weighted_random_beta(), f["id"])

    mean_cost, mean_diff = h(flight_tests, 1000)
    original_cost = sum(delay_cost(flight['delay']) for flight in flight_tests)
    return original_cost, mean_cost, mean_diff,  ((mean_diff / original_cost) * 100)
    
original_cost, mean_cost, mean_diff, percentage_diff = higher_level_heuristic(10000)

print(f"Heuristic original cost ${original_cost:,} \nHeuristic new cost after swaps ${round(mean_cost, 2):,} \nHeuristic mean difference in cost ${round(mean_diff, 2):,} \nHeuristic percentage difference in cost {round(percentage_diff, 2)}%")