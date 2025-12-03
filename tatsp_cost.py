def calculate_tatsp_cost(route, A, trigger_relations):


    total_cost = 0
    current_costs = A.copy()

    print("Rruga:", route)
    print("-------------------------------")

    for i in range(len(route) - 1):
        arc = (route[i], route[i + 1])
        cost = current_costs[arc]
        print(f"arc: {arc} me kosto aktuale: {cost}")

        if arc in trigger_relations:
            print(f"  Ky arc eshte trigger! Reset kostot:")
            for affected_arc, new_cost in trigger_relations[arc]:
                print(f"    {affected_arc} behet kosto: {new_cost}")
                current_costs[affected_arc] = new_cost

        total_cost += cost

 
    last_arc = (route[-1], route[0])
    print(f" arc: {last_arc} me kosto aktuale: {current_costs[last_arc]}")
    total_cost += current_costs[last_arc]

    print("-------------------------------")
    print(f"Kosto totale e rruges: {total_cost}\n")
    return total_cost


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


if __name__ == "__main__":
    path = [0, 1, 2, 3]
    calculate_tatsp_cost(path, A, trigger_relations)
