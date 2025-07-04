Optimising flight disruptions in fleet planning

Optimising flight disruptions in fleet planning

A travel company’s aircraft fleet needs to be managed. The flight paths need to be registered well in advance, often months in advance of the scheduled departure, in order to maximise profits. However, there can often be unexpected situations which arise. For example, flights may be delayed due to mechanical issues, or weather events which mean the flight can not take off. Therefore, the travel company incurs losses. The loss of a company needs to be minimised. This is a variation of the bus synchronisation timetabling problem.

Assumptions made:

 - We are only considering the problems caused by random events which cause delays, and not the movement of passengers, or crew, which are valid reasons.

 - Turnover times between a flight landing and parking, and then departing the next flight, is a minimum of two hours

 - Flights can not be cancelled due to the travel company offering a package-based product

 - Costs incurred due to delays is determined by a piecewise function: below and including 30 mins, the delay is normal and minimal, hence the cost is 0. The cost above 30 mins and below 180 mins is proportional (multiplied by 20 FOR EVERY MINUTE AFTER 30 MINS), and above 180 mins, the cost grows exponentially for every minute. This is because due to European Laws passengers whose flights have been delayed by above 3 hours are entitled to compensation.

 - The cost function is a heavily simplified function and can definitely be made dynamic and more complex by involving aspects of data science and machine learning in the future

 - Assuming that the swapping of flights if they happen are instantaneous and does not require any time. Again, this is a simplified mechanism to make the model simpler, however obviously this would incur costs

 - If there is a 40 minute delay in one flight and another flight has no delay, swapping flights such that the first flight’s delay is reduced to 20 minutes and the second flight’s delay is increased to 20 minutes (both flights have a delay of 20 minutes) reduces the costs to the company. The relationship between cost of delay and delay time is non linear, so a much larger delay equates to a proportionally larger cost to the company. Therefore splitting the delay between two flights has significantly less cost to the airline

 - An exceptional delay is a delay over 3 hours. This increases the cost exponentially because passengers are entitled to compensation for delays above 3 hours

1. Create a graph with nodes representing airports and edges representing flights. These edges can be weighted with the cost of the flight.
Model hourly cost as $2000, so cost of the flight is 2000 * duration
Simple model with four flights
JFK → LHR : 7.2 hours
LHR → CDG : 1.3 hours
HND → DXB : 10.7 hours
AMS → SIN : 12.7 hours
Turnover buffer time of 1 hour
Using python networkx and matplotlib pyplot

After discussing this strategy, it has been established that the costs of flying are constants in this particular problem, because the hourly cost can not be optimised and has to be incurred regardless of circumstances

2. Simulate a delay and split it between two flights originating from the same airport
Add more flights from the same airport
Calculate a cost relating to delay using a non linear function
Split the delay and calculate new cost to compare to before
We need to check if there exists another plane which is in the same airport and departs at a time which is no later than the buffer time of 1 hour
Assume all the planes are of the same type
Assume that the cost of a delay is exponential based on the delay in n hours
Small cost for small delays e.g. up to 15 mins
Moderate up to 1.5 hours
Exponential after 1.5 hours

Why this strategy did not work - it only showed the paths between different airports, and the planes that would be taking them, however in a simulation this may not be necessary or will not help towards optimising fleet disruption or delays. It may need to be implemented in a different way, which may be too complicated for my current skill level.


New strategy - use a continually running simulation.

 - Simulation runs for a set period of time. Planes arrive and depart at their given time and this is logged and outputted

 - Simulate a delay at time = 0 by setting a delay to a certain flight and calculating delays for other flight paths which use the same plane downstream

 -  Implement plane switching.

 - To optimise slightly, apply a heuristic. This will be a monte carlo simulation of a set number of random plane swaps, and checking whether this actually provides an improvement or not

Heuristic:

 - Simulate injection of random delay to a set input of flights which are chained (a delay on one flight can lead to another) and can allow for swapping in certain delays

 - Random delays are created using a beta distribution which is a statistical distribution which allows for a certain degree of skewing in any direction. In the heuristic model, the distribution for choosing a random delay is skewed towards a smaller delay which is less than 60 minutes, as this is more realistic in real life

 - The heuristic is repeated a set number of iterations, and the total new cost is calculated which is divided by the iterations to determine the mean new cost after swapping planes.

 - The mean new cost is subtracted from a calculated original cost without swapping planes, as well as the percentage change in cost. Ideally, this percentage change should be a decrease, as the mean difference will be a positive value due to the original cost being greater than the new cost.

 - After running the simulation several times the average percentage change in cost is roughly 6 percent, which suggests that swapping planes is a valid decision in optimising flight scheduling disruptions due to delays


What could be improved in the future and next steps that can be taken:

 - Once I have more statistics and data science knowledge, I can add a more complex system with machine learning, which stores information about swaps that happened and their outcome, as well as other factors, and use this to inform the next decision of whether swapping is optimal or not

 - Add more mechanisms to reduce delays e.g. introduce passenger scenarios, e.g. waiting for passengers who are late, introducing ferrying of flights if necessary, altogether cancelling flights if it is extremely costly to the company despite the no cancellation policy

 - Furthermore, once a greater knowledge of computer science and data structures is obtained, returning to the graph model of nodes and edges representing graphs opens much more possibilities in optimisation, such as applying algorithms such as Dijkstra's Algorithm or other traversal algorithms in finding optimal paths. While more complex, it can introduce the possibility of also optimising computational efficiency, and will be able to run more simulations using more inputs.

 - Introducing a larger input set of data for more accurate results.

 - Mixed Integer Linear Programming, or Linear Programming in general, had been looked into to determine whether a swap of aircraft is optimal. This is a set of mathematical inequalities and expressions which are provided with a set of constraints, and must be solved. This can be solved with many commercial solvers. However, this proved to be too complicated for the scope of the project
 
 - Another optimisation algorithm is the Minimax algorithm. This is an algorithm which is well known for its use in strategic games, primarily known for its use in chess. This is an algorithm in which a certain aspect of the program has to be minimised or maximised. In this case, the delay needs to be minimised, or alternatively flight scheduling efficiency needs to be optimised. The algorithm uses a tree like structure to look into future worst case scenarios, and determine the most optimal path to traverse.
