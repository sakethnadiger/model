import time


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
    

global turnover
turnover = 120

plane1 = Plane(1, "A", "idle")
plane2 = Plane(2, "B", "idle")
plane3 = Plane(3, "C", "idle")
plane4 = Plane(4, "D", "idle")
plane5 = Plane(5, "E", "idle")

available_planes = [plane1, plane2, plane3, plane4, plane5]

global flights
flights = [
    {"id":"fl1", "origin":"A", "destination":"B", "departure":"0000", "arrival":"0130", "duration":90, "plane_number":plane1, "delay":0},
    {"id":"fl2", "origin":"B", "destination":"D", "departure":"0330", "arrival":"0510", "duration":100, "plane_number":plane1, "delay":0},
    {"id":"fl3", "origin":"A", "destination":"B", "departure":"0100", "arrival":"0230", "duration":90, "plane_number":plane2, "delay":0},
    {"id":"fl4", "origin":"B", "destination":"C", "departure":"0430", "arrival":"0640", "duration":130, "plane_number":plane2, "delay":0}
]

time_range = 1440 # day

def hourToMin(hours:str):
    return int(hours[0:2]) * 60 + int(hours[2:])

def minToHHMM(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}{mins:02d}"

def simulate_delay(delay, flight_id):
    for i, flight in enumerate(flights):
        if flight["id"] == flight_id:
            flight["delay"] += delay
            
            original_departure = hourToMin(flight["departure"])
            original_arrival = hourToMin(flight["arrival"])
            
            flight["departure"] = minToHHMM(original_departure + delay)
            flight["arrival"] = minToHHMM(original_arrival + delay)
            
            
            print(f"Flight {flight['id']} delayed by {flight['delay']} minutes")
            
            plane = flight["plane_number"]
            
            for j in range(i + 1, len(flights)):
                if flights[j]["plane_number"] == plane:
                    # check if delay breaks turnover period
                    if hourToMin(flight["arrival"]) + turnover > hourToMin(flights[j]["departure"]):
                        required_delay = (hourToMin(flight["arrival"]) + turnover) - hourToMin(flights[j]["departure"])
                        simulate_delay(required_delay, flights[j]["id"])
                    break
                
            break
        
# simulate_delay(40, "fl3")

for t in range(time_range):
    
    for flight in flights:
        
        if t == hourToMin(flight['departure']):
            print(f"[{flight['departure']}] : Flight {flight['id']} departed from {flight['origin']} to {flight['destination']} plane {flight['plane_number'].get_id()}")#
            flight['plane_number'].set_status("inflight")
            
        if t == hourToMin(flight['arrival']):
            print(f"[{flight['arrival']}] : Flight {flight['id']} arrived to {flight['destination']} from {flight['origin']} plane {flight['plane_number'].get_id()}")
            flight['plane_number'].set_location(flight['destination'])
            flight['plane_number'].set_status("idle")
            print(f"Plane {flight['plane_number'].get_id()} new location set to {flight['plane_number'].get_location()}")
            
    print(minToHHMM(t))
    time.sleep(0.1)

    


