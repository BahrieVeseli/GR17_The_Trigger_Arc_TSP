import time
import random
from typing import List, Tuple, Dict
from cost_eval import compute_tour_cost, INF

def parse_instance(path: str):
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    header = raw_lines[0].split()
    n_nodes = int(header[0]); n_arcs = int(header[1]); n_rel = int(header[2])

    arcs: Dict[int, Tuple[int,int,float]] = {}
    arc_by_uv: Dict[Tuple[int,int], int] = {}

    for i in range(1, 1 + n_arcs):
        aidx, u, v, c = raw_lines[i].split()
        aidx = int(aidx); u = int(u); v = int(v); c = float(c)
        if c < 0:
            raise ValueError(f"Arc {aidx} ({u}->{v}) has negative cost {c}, which is not allowed.")
        arcs[aidx] = (u, v, c)
        arc_by_uv[(u, v)] = aidx

    relations = []
    rel_start = 1 + n_arcs
    for k in range(rel_start, rel_start + n_rel):
        parts = raw_lines[k].split()
        rel_idx = int(parts[0])
        trig_idx = int(parts[1]); trig_u = int(parts[2]); trig_v = int(parts[3])
        targ_idx = int(parts[4]); targ_u = int(parts[5]); targ_v = int(parts[6])
        new_cost = float(parts[7])
        if new_cost < 0:
            raise ValueError(f"Relation {rel_idx} sets negative cost {new_cost} for arc {targ_idx}, which is not allowed.")
        if (trig_u, trig_v) != arcs[trig_idx][:2]:
            raise ValueError(f"Relation {rel_idx} trigger arc mismatch: expected {arcs[trig_idx][:2]}, got {(trig_u,trig_v)}")
        if (targ_u, targ_v) != arcs[targ_idx][:2]:
            raise ValueError(f"Relation {rel_idx} target arc mismatch: expected {arcs[targ_idx][:2]}, got {(targ_u,targ_v)}")
        relations.append((trig_idx, targ_idx, new_cost))

    trigger_map_by_trigger: Dict[int, List[Tuple[int, float]]] = {}
    for trig_idx, targ_idx, newc in relations:
        trigger_map_by_trigger.setdefault(trig_idx, []).append((targ_idx, newc))

    return n_nodes, arcs, arc_by_uv, trigger_map_by_trigger

def greedy_construct(n_nodes, arcs, arc_by_uv, trigger_map_by_trigger, seed=None):
    rng = random.Random(seed)
    unvisited = set(range(n_nodes))
    current = 0
    tour = [current]
    unvisited.remove(current)
    while unvisited:
        best_v, best_c = None, INF
        for v in unvisited:
            a = arc_by_uv.get((current, v))
            if a is None:
                continue
            c = arcs[a][2]
            if c < best_c or (c == best_c and rng.random() < 0.5):
                best_v, best_c = v, c
        if best_v is None:
            best_v = rng.choice(list(unvisited))
        tour.append(best_v)
        unvisited.remove(best_v)
        current = best_v
    tour.append(0)
    return tour

def two_opt(tour: List[int], i: int, k: int) -> List[int]:
    return tour[:i] + list(reversed(tour[i:k+1])) + tour[k+1:]

def relocate(tour: List[int], i: int, j: int) -> List[int]:
    if i == 0 or i == len(tour)-1:
        return tour
    node = tour[i]
    new = tour[:i] + tour[i+1:]
    new = new[:j] + [node] + new[j:]
    if new[0] != 0:
        z = new.index(0)
        new = new[z:] + new[:z]
    if new[-1] != 0:
        new.append(0)
    return new

def local_search(tour, arcs, arc_by_uv, trigger_map_by_trigger, time_budget, start_time):
    best = tour
    best_cost, _ = compute_tour_cost(best, arcs, arc_by_uv, trigger_map_by_trigger)
    n = len(tour) - 1
    improved = True
    while improved and time.time() - start_time < time_budget:
        improved = False
        for i in range(1, n-1):
            for k in range(i+1, n):
                if time.time() - start_time >= time_budget: break
                cand = two_opt(best, i, k)
                c, _ = compute_tour_cost(cand, arcs, arc_by_uv, trigger_map_by_trigger)
                if c < best_cost:
                    best, best_cost = cand, c
                    improved = True
                    break
            if improved: break
        for i in range(1, n):
            for j in range(1, n):
                if time.time() - start_time >= time_budget: break
                if i == j: continue
                cand = relocate(best, i, j)
                c, _ = compute_tour_cost(cand, arcs, arc_by_uv, trigger_map_by_trigger)
                if c < best_cost:
                    best, best_cost = cand, c
                    improved = True
                    break
            if improved: break
    return best, best_cost

def double_bridge_perturbation(tour, rng):
    n = len(tour) - 1
    if n < 8: return tour[:]
    splits = sorted(rng.sample(range(1, n), 4))
    a,b,c,d = splits
    p1 = tour[:a]; p2 = tour[a:b]; p3 = tour[b:c]; p4 = tour[c:d]; p5 = tour[d:]
    new_tour = p1 + p3 + p2 + p4 + p5
    if new_tour[-1] != 0: new_tour.append(0)
    return new_tour

def iterated_local_search(init_tour, arcs, arc_by_uv, trigger_map_by_trigger, time_budget_seconds=30, seed=None):
    rng = random.Random(seed)
    start_time = time.time()
    best, best_cost = local_search(init_tour, arcs, arc_by_uv, trigger_map_by_trigger, time_budget_seconds, start_time)
    current, current_cost = best[:], best_cost
    while time.time() - start_time < time_budget_seconds:
        cand = double_bridge_perturbation(current, rng)
        cand, cand_cost = local_search(cand, arcs, arc_by_uv, trigger_map_by_trigger, time_budget_seconds, start_time)
        if cand_cost < current_cost or rng.random() < 0.05:
            current, current_cost = cand, cand_cost
            if cand_cost < best_cost:
                best, best_cost = cand, cand_cost
    _, arc_costs = compute_tour_cost(best, arcs, arc_by_uv, trigger_map_by_trigger)
    return best, best_cost, arc_costs

def solve_instance(path, time_budget_seconds=30, seed=None):
    n_nodes, arcs, arc_by_uv, trigger_map_by_trigger = parse_instance(path)
    init_tour = greedy_construct(n_nodes, arcs, arc_by_uv, trigger_map_by_trigger, seed=seed)
    best_tour, best_cost, arc_costs = iterated_local_search(
        init_tour, arcs, arc_by_uv, trigger_map_by_trigger, time_budget_seconds=time_budget_seconds, seed=seed
    )
    return best_tour, best_cost, arcs, arc_by_uv, trigger_map_by_trigger, arc_costs
