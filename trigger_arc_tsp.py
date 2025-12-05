import argparse, random, time
from tsp_solver import solve_instance

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("instance", help="Path to instance file")
    p.add_argument("--time", type=int, default=30, help="Time budget in seconds")
    p.add_argument("--seed", type=int, default=None, help="Random seed")
    args = p.parse_args()

    random.seed(args.seed)
    t0 = time.time()

    best_tour, best_cost, arcs, trigger_map_by_trigger = solve_instance(
        args.instance, time_budget_seconds=args.time, seed=args.seed
    )

    t1 = time.time()
    print(f"Done in {t1-t0:.2f}s. Cost={best_cost:.6f}")


    try:
        from visualization import plot_tour
        plot_tour(best_tour, arcs, trigger_map_by_trigger)
    except ImportError:
        print("Matplotlib not available. Skipping plot.")
