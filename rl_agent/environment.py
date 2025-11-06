import json
import os
import random
import math
from algorithms.dijkstra import load_city_graph, build_adjacency_list


class DeliveryRouteEnv:
    """
    Reinforcement Learning Environment for route optimization.
    Each episode = one delivery trip from start to destination.
    """

    def __init__(self, start, target, weight_type="distance"):
        self.graph = load_city_graph()
        self.adjacency = build_adjacency_list(self.graph, weight_type=weight_type)
        self.locations = list(self.graph["locations"].keys())
        self.start = start
        self.target = target
        self.current = start
        self.weight_type = weight_type
        self.max_steps = len(self.locations) * 2
        self.steps = 0

    def reset(self):
        """Reset environment to start a new episode."""
        self.current = self.start
        self.steps = 0
        return self.current

    def step(self, action):
        """
        Take one step in the environment.
        Args:
            action: the next location name (must be a neighbor)
        Returns:
            next_state, reward, done, info
        """
        self.steps += 1

        if action not in [n for n, _ in self.adjacency[self.current]]:
            # Invalid action → penalty
            reward = -10
            done = False
            info = {"error": "Invalid move"}
            return self.current, reward, done, info

        # Cost to move
        cost = next(weight for n, weight in self.adjacency[self.current] if n == action)
        reward = -cost  # less distance/time/fuel = higher reward
        self.current = action

        done = self.current == self.target or self.steps >= self.max_steps
        info = {"cost": cost}
        return self.current, reward, done, info

    def get_valid_actions(self):
        """Return all valid neighboring locations."""
        return [n for n, _ in self.adjacency[self.current]]

    def render(self):
        """Optional: print current location (for debugging)."""
        print(f"🚗 Current: {self.current} | Target: {self.target} | Step: {self.steps}")


if __name__ == "__main__":
    # quick test
    env = DeliveryRouteEnv("Master Canteen Square", "KIIT Square", weight_type="distance")
    state = env.reset()
    print(f"Start at: {state}")

    for _ in range(10):
        actions = env.get_valid_actions()
        next_action = random.choice(actions)
        next_state, reward, done, info = env.step(next_action)
        print(f"Move → {next_action} | Reward: {reward:.2f}")
        if done:
            print("🏁 Destination reached or max steps exceeded")
            break
