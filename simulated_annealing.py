import random
import math

A = {
    (0, 1): 10,
    (0, 2): 15,
    (0, 3): 20,
    (1, 0): 10,
    (1, 2): 35,
    (1, 3): 25,
    (2, 0): 15,
    (2, 1): 35,
    (2, 3): 30, 
    (3, 0): 20,
    (3, 1): 25,
    (3, 2): 30
}

TRIGGERS = {
    ((0, 1), (1, 2)): 5,
    ((2, 1), (3, 0)): 10
}

def tatsp_cost(route):
    total_cost = 0
    current_costs = A.copy()

    for i in range(len(route) - 1):
        arc = (route[i], route[i + 1])
        total_cost += current_costs[arc]


        for (trigger, affected), new_cost in TRIGGERS.items():
            if arc == trigger:
                current_costs[affected] = new_cost

    last_arc = (route[-1], route[0])
    total_cost += current_costs[last_arc]

    return total_cost

def generate_neighbor(route):
    new_route = route[:]
    i, j = random.sample(range(1, len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def simulated_annealing(nodes, cost_func):
    current_route = nodes[:]
    random.shuffle(current_route)
    current_cost = cost_func(current_route)
    best_route, best_cost = current_route[:], current_cost
    temp = 1000

    while temp > 0.01:
        neighbor = generate_neighbor(current_route)
        neighbor_cost = cost_func(neighbor)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_route, best_cost = current_route[:], current_cost

        temp *= 0.995

    return best_route, best_cost


if __name__ == "__main__":
    NODES = [0, 1, 2, 3]
    best_route, best_cost = simulated_annealing(NODES, tatsp_cost)

    print("Rruga me e mire e gjetur:", best_route)
    print("Kosto e rruges:", best_cost)
