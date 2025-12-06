INF = 1e15

def tour_arcs_from_nodes(tour_nodes, arc_by_uv):
    arc_seq=[]
    for i in range(len(tour_nodes)-1):
        a=arc_by_uv.get((tour_nodes[i], tour_nodes[i+1]))
        if a is None: return None
        arc_seq.append(a)
    return arc_seq

def compute_tour_cost_from_arcseq(arc_seq, arcs, trigger_map_by_trigger):
    last_activation={}
    total=0.0
    for a in arc_seq:
        total += last_activation.get(a, arcs[a][2])
        for (targ,newc) in trigger_map_by_trigger.get(a,[]):
            last_activation[targ]=newc
    return total

def compute_tour_cost(tour_nodes, arcs, arc_by_uv, trigger_map_by_trigger):
    arc_seq = tour_arcs_from_nodes(tour_nodes, arc_by_uv)
    if arc_seq is None: return INF, False
    return compute_tour_cost_from_arcseq(arc_seq, arcs, trigger_map_by_trigger), True
