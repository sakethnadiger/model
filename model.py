import networkx as nx
import matplotlib.pyplot as plt
import math
import re

flight_graph = nx.DiGraph()

# hourly operational cost for airline
HOURLY_COST = 2000

available_planes = ["plane1", "plane2", "plane3", "plane4"]

# define dictionary to store data for every flight {id, origin, destination, departure, arrival, duration, plane_number, delay}
# assume flights list is ordered and that flights are added in order of id
# id format: fl##
global flights
flights = [
    {"id":"fl1", "origin":"JFK", "destination":"LHR", "departure":"1830", "arrival":"0630", "duration":7, "plane_number":"plane1", "delay":0},
    {"id":"fl2", "origin":"LHR", "destination":"CDG", "departure":"0745", "arrival":"1000", "duration":1.25, "plane_number":"plane1", "delay":0},
    {"id":"fl3", "origin":"HND", "destination":"DXB", "departure":"2200", "arrival":"0400", "duration":11, "plane_number":"plane2", "delay":0},
    {"id":"fl4", "origin":"AMS", "destination":"SIN", "departure":"2000", "arrival":"1450", "duration":12.8, "plane_number":"plane3", "delay":0}
]

def add_flight(id, origin, destination, departure, arrival, duration, plane_number, delay):
    flights.append({"id":id, "origin":origin, "destination":destination, "departure":departure, "arrival":arrival, "duration":duration, "plane_number":plane_number, "delay":delay})

add_flight("fl5", "JFK", "ORD", "0800", "1045", 2.75, "plane4", 0)


for flight in flights:
    origin = flight["origin"]
    departure = flight["departure"]
    destination = flight["destination"]
    arrival = flight["arrival"]
    cost = int(flight["duration"]*HOURLY_COST)
    flight_graph.add_edge(f"{origin}:{departure}", f"{destination}:{arrival}", weight=cost)


def display():
    plt.figure(figsize=(10, 8))
    nx.draw(flight_graph, pos=nx.circular_layout(flight_graph), with_labels=True, node_size=2000)

    edge_labels = nx.get_edge_attributes(flight_graph, 'weight')
    nx.draw_networkx_edge_labels(flight_graph, pos=nx.circular_layout(flight_graph), edge_labels=edge_labels)

    plt.axis('off')
    plt.show()

# added delay in minutes
def simulate_delay_splitting(added_delay, delayed_flight_id):
    if added_delay  <= 30: cost = 0
    if added_delay  > 30 and added_delay <= 180: cost = (added_delay - 30) * 20
    if added_delay > 180: cost = int(20 * (180-30) + 200 * (math.exp(0.05 * (added_delay - 180)) - 1))
    flights[int(delayed_flight_id[re.search("\d", delayed_flight_id).start():]) - 1]["delay"] = added_delay
    
    
    
    return cost

display()