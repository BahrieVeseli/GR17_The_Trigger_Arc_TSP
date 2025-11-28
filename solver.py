import itertools
from main import calculate_cost, A, trigger_relations

def generate_cycles(nodes):
    start = nodes[0]
    other_nodes = nodes[1:]
    for perm in itertools.permutations(other_nodes):
        path = [start] + list(perm)
        yield path

def find_best_cycle(nodes, A, trigger_relations):
    best_cost = float("inf")
    best_path = None

    for path in generate_cycles(nodes):
        cost = calculate_cost(path, A, trigger_relations)
        print(f"Cikli {path} ka kosto {cost}")
        if cost < best_cost:
            best_cost = cost
            best_path = path

    return best_path, best_cost

if __name__ == "__main__":
    nodes = [0, 1, 2]
    best_path, best_cost = find_best_cycle(nodes, A, trigger_relations)
    print("----------------------------")
    print(f"Cikli më i mirë: {best_path}")
    print(f"Me koston: {best_cost}")
    print("----------------------------")
