import json
import math
import random

def generate_bhubaneswar_graph():
    """Generate a realistic graph with Bhubaneswar landmarks"""
    
    locations = {
        "Master Canteen Square": {"id": 0, "x": 85.836, "y": 20.268},
        "Railway Station": {"id": 1, "x": 85.838, "y": 20.269},
        "Kharavela Nagar": {"id": 2, "x": 85.837, "y": 20.272},
        "Ram Mandir Square": {"id": 3, "x": 85.843, "y": 20.275},
        "Kalpana Square": {"id": 4, "x": 85.841, "y": 20.252},
        "Lingaraj Temple": {"id": 5, "x": 85.834, "y": 20.244},
        "Airport (BPI)": {"id": 6, "x": 85.818, "y": 20.255},
        "CRP Square": {"id": 7, "x": 85.812, "y": 20.295},
        "Nayapalli": {"id": 8, "x": 85.816, "y": 20.288},
        "Jayadev Vihar": {"id": 9, "x": 85.824, "y": 20.296},
        "Patia Big Bazaar": {"id": 10, "x": 85.824, "y": 20.345},
        "KIIT Square": {"id": 11, "x": 85.825, "y": 20.348},
        "Infocity": {"id": 12, "x": 85.828, "y": 20.351},
        "Chandrasekharpur": {"id": 13, "x": 85.830, "y": 20.340},
        "Vani Vihar": {"id": 14, "x": 85.834, "y": 20.283},
        "Acharya Vihar": {"id": 15, "x": 85.832, "y": 20.288},
        "Rasulgarh": {"id": 16, "x": 85.851, "y": 20.274},
        "Palasuni": {"id": 17, "x": 85.858, "y": 20.281},
        "Mancheswar": {"id": 18, "x": 85.867, "y": 20.292},
        "Baramunda": {"id": 19, "x": 85.806, "y": 20.277}
    }

    edges = []
    names = list(locations.keys())

    # Connect each location to 3–5 nearby ones
    for loc_name, loc_data in locations.items():
        distances = []
        for other_name, other_data in locations.items():
            if loc_name != other_name:
                dist = math.sqrt(
                    (loc_data['x'] - other_data['x'])**2 +
                    (loc_data['y'] - other_data['y'])**2
                ) * 111  # Convert roughly degrees → km
                distances.append((other_name, dist))

        distances.sort(key=lambda x: x[1])
        num_connections = random.randint(3, 5)

        for other_name, dist in distances[:num_connections]:
            exists = any(
                (e['from'] == loc_name and e['to'] == other_name) or
                (e['from'] == other_name and e['to'] == loc_name)
                for e in edges
            )
            if not exists:
                distance = round(dist, 2)
                speed = random.uniform(25, 55)
                time = round(distance / speed * 60, 2)  # minutes
                fuel_cost = round(distance * random.uniform(0.08, 0.15), 2)
                edges.append({
                    "from": loc_name,
                    "to": other_name,
                    "distance": distance,
                    "time": time,
                    "fuel_cost": fuel_cost
                })

    graph = {
        "locations": locations,
        "edges": edges,
        "metadata": {
            "num_locations": len(locations),
            "num_roads": len(edges),
            "city": "Bhubaneswar"
        }
    }

    return graph


def save_graph(graph, filename="data/bhubaneswar_graph.json"):
    import os
    os.makedirs("data", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(graph, f, indent=2)
    print(f"✅ Bhubaneswar graph saved to {filename}")
    print(f"📍 Locations: {graph['metadata']['num_locations']}")
    print(f"🛣️  Roads: {graph['metadata']['num_roads']}")


if __name__ == "__main__":
    graph = generate_bhubaneswar_graph()
    save_graph(graph)
    print("🎉 Realistic Bhubaneswar dataset generated successfully!")
