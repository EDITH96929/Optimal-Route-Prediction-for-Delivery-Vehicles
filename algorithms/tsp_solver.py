import json
import itertools
import os
from .dijkstra import build_adjacency_list, dijkstra, load_city_graph


def compute_path_cost(adjacency, path, weight_type="distance"):
    """Calculate total cost (distance/time/fuel) for a given visiting order."""
    total = 0.0
    for i in range(len(path) - 1):
        start, end = path[i], path[i + 1]
        cost, _ = dijkstra(adjacency, start, end)
        total += cost
    return total


def solve_tsp(locations, start=None, end=None, weight_type="distance"):
    """
    Simple brute-force TSP for small sets of locations (<=8 recommended).
    """
    graph = load_city_graph()
    adjacency = build_adjacency_list(graph, weight_type=weight_type)

    if not start:
        start = locations[0]

    stops = [loc for loc in locations if loc != start]
    best_order = None
    best_cost = float("inf")

    for perm in itertools.permutations(stops):
        route = [start] + list(perm)
        if end:
            route.append(end)
        else:
            route.append(start)  # return to start

        total_cost = compute_path_cost(adjacency, route, weight_type)

        if total_cost < best_cost:
            best_cost = total_cost
            best_order = route

    return best_cost, best_order


if __name__ == "__main__":
    # Example usage
    locations = [
        "Master Canteen Square",
        "Ram Mandir Square",
        "Acharya Vihar",
        "Jayadev Vihar",
        "KIIT Square"
    ]

    metric = "distance"  # or "time" or "fuel_cost"
    best_cost, best_route = solve_tsp(locations, weight_type=metric)

    print("🚛 Optimal delivery route (multi-stop):")
    print(" → ".join(best_route))
    print(f"Total {metric}: {best_cost:.2f}")

