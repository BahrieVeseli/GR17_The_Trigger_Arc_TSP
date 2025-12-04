N = [0, 1, 2, 3]  # lista nyjeve

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

trigger_relations = {
    (0, 1): [((0, 2), 5), ((1, 2), 8)],
    (1, 2): [((0, 1), 20)]
}

def calculate_cost(path, A, trigger_relations):
    total_cost = 0
    last_trigger = {}
    current_costs = A.copy()  
    passed_arcs = set() 

    for i in range(len(path) - 1):
        edge = (path[i], path[i+1])
        active_cost = current_costs[edge]

        if edge in trigger_relations:
            for t_edge, new_cost in trigger_relations[edge]:
                if t_edge not in passed_arcs:
                    current_costs[t_edge] = new_cost  

        last_trigger[edge] = edge
        total_cost += active_cost
        passed_arcs.add(edge)  

 
    last_edge = (path[-1], path[0])
    total_cost += current_costs[last_edge]

    return total_cost



path = [0, 1, 2, 3]
cost = calculate_cost(path, A, trigger_relations)
print(f"Cikli: {path} me kosto: {cost}")
