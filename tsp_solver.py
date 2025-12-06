import sys, os, time, random, math
from typing import List, Tuple, Dict, Optional
from cost_eval import (
    INF,
    tour_arcs_from_nodes,
    compute_tour_cost_from_arcseq,
    compute_tour_cost
)

def parse_instance(path: str):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    tokens = []
    for ln in lines:
        clean = ln.replace("(", " ").replace(")", " ").replace(",", " ")
        tokens.extend(clean.split())
    if len(tokens) < 3:
        raise ValueError("Instance too short.")
    idx = 0
    n_nodes = int(tokens[idx]); idx+=1
    n_arcs = int(tokens[idx]); idx+=1
    n_rel = int(tokens[idx]); idx+=1
    arcs = {}
    arc_by_uv = {}
    for _ in range(n_arcs):
        aidx = int(tokens[idx]); u = int(tokens[idx+1]); v = int(tokens[idx+2]); cost = float(tokens[idx+3])
        idx += 4
        arcs[aidx] = (u, v, cost)
        arc_by_uv[(u,v)] = aidx
    relations = []
    while idx < len(tokens):
        nums = []
        lookahead = 6
        for j in range(lookahead):
            if idx+j >= len(tokens): break
            tok = tokens[idx+j]
            s = ''.join(ch for ch in tok if (ch.isdigit() or ch=='-' or ch=='.'))
            if s=="": continue
            try: nums.append(float(s))
            except: pass
        idx += max(1, min(lookahead, len(nums)+1))
        if len(nums) >= 3:
            trig = int(nums[0]); targ = int(nums[1]); newc = nums[2]
            relations.append((trig, targ, newc))
            continue
            if len(nums) >= 5:
                tfrom = int(nums[0]); tto = int(nums[1]); sfrom = int(nums[2]); sto = int(nums[3]); newc = nums[4]
                trig_idx = arc_by_uv.get((tfrom,tto))
                targ_idx = arc_by_uv.get((sfrom,sto))
                if trig_idx is not None and targ_idx is not None:
                    relations.append((trig_idx, targ_idx, newc))
                    continue
    return n_nodes, arcs, arc_by_uv, relations



def greedy_construct(n_nodes, arcs, arc_by_uv, trigger_map_by_trigger, attempts=200):
    best_t, best_c = None, INF
    for _ in range(attempts):
        start = 0; curr = start; visited = {start}; tour = [start]
        while len(visited) < n_nodes:
            cand = [(arcs[aidx][2], v) for v in range(n_nodes) if v not in visited and (aidx:=arc_by_uv.get((curr,v))) is not None]
            if not cand: break
            cand.sort(key=lambda x:x[0])
            _, v = random.choice(cand[:min(3,len(cand))])
            tour.append(v); visited.add(v); curr=v
        tour.append(start)
        cost, valid = compute_tour_cost(tour, arcs, arc_by_uv, trigger_map_by_trigger)
        if valid and cost < best_c: best_t, best_c = tour, cost
    return best_t, best_c


def two_opt_once(tour, arcs, arc_by_uv, trigger_map_by_trigger):
    n = len(tour)-1; best_t=tour; best_c,_=compute_tour_cost(tour, arcs, arc_by_uv, trigger_map_by_trigger)
    for i in range(1,n-1):
        for j in range(i+1,n):
            if j-i==0: continue
            cand = tour[:i]+tour[i:j+1][::-1]+tour[j+1:]
            cost, valid = compute_tour_cost(cand, arcs, arc_by_uv, trigger_map_by_trigger)
            if valid and cost < best_c:
                return cand, True
    return best_t, False

def relocate_once(tour, arcs, arc_by_uv, trigger_map_by_trigger):
    n = len(tour)-1
    for i in range(1,n):
        for j in range(1,n):
            if i==j: continue
            t = tour.copy(); node = t.pop(i); t.insert(j,node)
            cost, valid = compute_tour_cost(t, arcs, arc_by_uv, trigger_map_by_trigger)
            if valid and cost < compute_tour_cost(tour, arcs, arc_by_uv, trigger_map_by_trigger)[0]:
                return t, True
    return tour, False

def local_search_full(tour, arcs, arc_by_uv, trigger_map_by_trigger, max_no_improve=50):
    curr=tour; curr_cost,_=compute_tour_cost(curr, arcs, arc_by_uv, trigger_map_by_trigger)
    no_improve=0
    while no_improve<max_no_improve:
        cand,did=two_opt_once(curr, arcs, arc_by_uv, trigger_map_by_trigger)
        if did: curr= cand; no_improve=0; continue
        cand,did=relocate_once(curr, arcs, arc_by_uv, trigger_map_by_trigger)
        if did: curr= cand; no_improve=0; continue
        no_improve+=1
    return curr, compute_tour_cost(curr, arcs, arc_by_uv, trigger_map_by_trigger)[0]


def double_bridge(tour):
    n=len(tour)-1
    if n<8:
        mid=tour[1:-1]; random.shuffle(mid); return [tour[0]]+mid+[tour[0]]
    pos=sorted(random.sample(range(1,n),4)); a,b,c,d=pos
    A=tour[1:a+1]; B=tour[a+1:b+1]; C=tour[b+1:c+1]; D=tour[c+1:d+1]; E=tour[d+1:-0] if d+1<n else []
    return [tour[0]]+A+C+B+D+E+[tour[0]]

def iterated_local_search(initial_tour, arcs, arc_by_uv, trigger_map_by_trigger, time_limit=30.0, seed=None):
    random.seed(seed)
    start_time=time.time()
    best_tour=initial_tour
    best_cost,_=compute_tour_cost(best_tour, arcs, arc_by_uv, trigger_map_by_trigger)
    curr_tour=best_tour; curr_cost=best_cost; iter_no=0
    while time.time()-start_time<time_limit:
        curr_tour,curr_cost=local_search_full(curr_tour, arcs, arc_by_uv, trigger_map_by_trigger, max_no_improve=30)
        if curr_cost<best_cost:
            best_cost=curr_cost; best_tour=curr_tour.copy(); print(f"[ILS] new best {best_cost:.6f} at iter {iter_no}")
        pert=double_bridge(curr_tour)
        pert, pert_cost=local_search_full(pert, arcs, arc_by_uv, trigger_map_by_trigger, max_no_improve=20)
        if pert_cost<curr_cost or random.random()<0.05: curr_tour, curr_cost=pert, pert_cost
        iter_no+=1
    return best_tour, best_cost


def solve_instance(path, time_budget_seconds=30, seed=None):
    n_nodes, arcs, arc_by_uv, relations = parse_instance(path)
    trigger_map_by_trigger={}
    for trig,targ,newc in relations:
        trigger_map_by_trigger.setdefault(trig, []).append((targ,newc))
    print(f"Parsed: n={n_nodes}, arcs={len(arcs)}, relations={len(relations)}")
    init_tour, init_cost=greedy_construct(n_nodes, arcs, arc_by_uv, trigger_map_by_trigger, attempts=300)
    if init_tour is None:
        mid=list(range(1,n_nodes)); random.shuffle(mid); init_tour=[0]+mid+[0]
        init_cost,_=compute_tour_cost(init_tour, arcs, arc_by_uv, trigger_map_by_trigger)
        if init_cost>=INF: raise RuntimeError("No valid initial tour.")
    print(f"Initial cost: {init_cost:.6f}")
    best_tour, best_cost=iterated_local_search(init_tour, arcs, arc_by_uv, trigger_map_by_trigger, time_limit=time_budget_seconds, seed=seed)
    print(f"Best cost after ILS: {best_cost:.6f}")
    with open("solution.txt","w",encoding="utf-8") as f:
        f.write(" ".join(map(str,best_tour))+"\n")
        f.write(f"{best_cost:.6f}\n")

    return best_tour, best_cost, arcs, trigger_map_by_trigger
