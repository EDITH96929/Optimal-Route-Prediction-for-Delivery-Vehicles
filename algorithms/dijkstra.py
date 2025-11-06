import json
import os
import heapq


def load_city_graph(filename="data/bhubaneswar_graph.json"):
    """Load the city graph safely no matter where the script is run from"""
    # Get absolute path to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes up from algorithms/
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"⚠️ Could not find {filepath}\n"
            f"Make sure bhubaneswar_graph.json is inside the project's data/ folder.\n"
            f"Expected full path: {filepath}"
        )

    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def build_adjacency_list(graph, weight_type="distance"):
    adjacency = {}
    for edge in graph["edges"]:
        src = edge["from"]
        dst = edge["to"]
        weight = edge[weight_type]
        adjacency.setdefault(src, []).append((dst, weight))
        adjacency.setdefault(dst, []).append((src, weight))
    return adjacency


def dijkstra(adjacency, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)

        if node == end:
            return cost, path

        for neighbor, weight in adjacency.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return float("inf"), []


def find_optimal_route(start, end, weight_type="distance"):
    graph = load_city_graph()
    adjacency = build_adjacency_list(graph, weight_type=weight_type)
    total_cost, path = dijkstra(adjacency, start, end)
    return total_cost, path


if __name__ == "__main__":
    start = "Master Canteen Square"
    end = "KIIT Square"
    metric = "distance"  # try "time" or "fuel_cost" also

    total_cost, path = find_optimal_route(start, end, weight_type=metric)
    print(f"🚚 Optimal route from {start} to {end} ({metric}):")
    print(" → ".join(path))
    print(f"Total {metric}: {total_cost:.2f}")
