import random
import pickle
import os
from collections import defaultdict
from .environment import DeliveryRouteEnv


class QLearningAgent:
    """
    Basic Q-learning agent for route optimization.
    Learns best moves based on rewards from DeliveryRouteEnv.
    """

    def __init__(self, env, alpha=0.3, gamma=0.9, epsilon=0.2):
        self.env = env
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate
        self.Q = defaultdict(float)

    def choose_action(self, state):
        """Epsilon-greedy action selection."""
        actions = self.env.get_valid_actions()
        if not actions:
            return None

        if random.random() < self.epsilon:
            return random.choice(actions)

        # pick best Q-value
        q_values = [self.Q[(state, a)] for a in actions]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(actions, q_values) if q == max_q]
        return random.choice(best_actions)

    def learn(self, episodes=1000):
        """Train the agent for multiple episodes."""
        for ep in range(episodes):
            state = self.env.reset()
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)
                if not action:
                    break

                next_state, reward, done, _ = self.env.step(action)
                next_actions = self.env.get_valid_actions()
                max_next_q = max([self.Q[(next_state, a)] for a in next_actions], default=0.0)

                # Q-learning update
                self.Q[(state, action)] = (
                    (1 - self.alpha) * self.Q[(state, action)]
                    + self.alpha * (reward + self.gamma * max_next_q)
                )

                state = next_state
                total_reward += reward

            if (ep + 1) % 100 == 0:
                print(f"Episode {ep+1}/{episodes} | Total Reward: {total_reward:.2f}")

        print("✅ Training complete!")

    def save(self, filename="models/q_table.pkl"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(dict(self.Q), f)
        print(f"💾 Q-table saved at {filename}")

    def load(self, filename="models/q_table.pkl"):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"No saved Q-table found at {filename}")
        with open(filename, "rb") as f:
            data = pickle.load(f)
        self.Q = defaultdict(float, data)
        print(f"✅ Q-table loaded from {filename}")

    def get_optimal_route(self, start, target):
        """Use learned Q-table to follow best route greedily."""
        self.env.start = start
        self.env.target = target
        state = self.env.reset()
        path = [state]
        cost = 0.0

        for _ in range(len(self.env.locations) * 2):
            actions = self.env.get_valid_actions()
            if not actions:
                break
            best_action = max(actions, key=lambda a: self.Q[(state, a)])
            _, reward, done, info = self.env.step(best_action)
            cost -= reward  # reward is negative cost
            state = best_action
            path.append(state)
            if done:
                break

        return path, cost


if __name__ == "__main__":
    # Example: Train agent to go from Master Canteen → KIIT Square
    env = DeliveryRouteEnv("Master Canteen Square", "KIIT Square", weight_type="distance")
    agent = QLearningAgent(env, alpha=0.3, gamma=0.9, epsilon=0.2)

    # Train the model
    agent.learn(episodes=1000)
    agent.save()

    # Test the learned policy
    path, total_cost = agent.get_optimal_route("Master Canteen Square", "KIIT Square")
    print("🚚 Learned Optimal Route:")
    print(" → ".join(path))
    print(f"Total Distance: {total_cost:.2f}")
