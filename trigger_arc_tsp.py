
import argparse, time, random
from tsp_solver import solve_instance
from visualization import plot_tour

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("instance", help="Path to instance file")
    p.add_argument("--time", type=float, default=30, help="Time budget in seconds")
    p.add_argument("--seed", type=int, default=None, help="Random seed")
    p.add_argument("--no-plot", action="store_true", help="Disable plotting")
    args = p.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    t0 = time.time()
    tour, cost, arcs, arc_by_uv, trigger_map_by_trigger, arc_costs = solve_instance(
        args.instance, time_budget_seconds=args.time, seed=args.seed
    )
    t1 = time.time()
    print(f"Done in {t1 - t0:.2f}s. Cost={cost:.6f}")


    print("\nRendi i turit (me kostot reale):")
    for (aidx, applied) in arc_costs:
        u, v, _ = arcs[aidx]
        print(f"{u} -> {v} (arc {aidx}, cost={applied})")
    print(f"Total cost = {cost:.6f}\n")

  
    if not args.no_plot:
        plot_tour(tour, arcs, arc_by_uv, trigger_map_by_trigger)
