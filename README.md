# 🚚 Optimal Route Prediction for Delivery Vehicles

### 📘 Domain Project | AI & Machine Learning

**Objective:** Predict the *fastest* and *most fuel-efficient* delivery routes across Bhubaneswar using **Graph Algorithms** and **Reinforcement Learning (RL)**.
Developed with Python, Streamlit, and Q-Learning.

---

## 🧭 Project Overview

This project simulates a smart delivery route optimizer for logistics systems in Bhubaneswar city.
It automatically computes the most efficient path for one or multiple deliveries using:

* **Graph Algorithms** (Dijkstra, TSP)
* **Reinforcement Learning** (Q-Learning agent)
* **GUI Visualization** with Streamlit

The model can optimize based on **distance**, **travel time**, or **fuel consumption**.

---

## 🎯 Objectives

* Predict optimal routes between delivery points.
* Reduce travel time and fuel cost.
* Provide an interactive GUI to visualize routes.
* Implement a learning-based route predictor using Reinforcement Learning.

---

## 🧱 System Architecture

```
delivery-optimizer/
│
├── data/
│   └── bhubaneswar_graph.json          # Realistic city graph dataset
│
├── algorithms/
│   ├── dijkstra.py                     # Shortest path algorithm
│   └── tsp_solver.py                   # Multi-stop (TSP) optimization
│
├── rl_agent/
│   ├── environment.py                  # RL environment (Delivery simulator)
│   └── agent.py                        # Q-learning route agent
│
├── utils/
│   └── graph_generator.py              # Generates Bhubaneswar road dataset
│
├── gui/
│   └── app.py                          # Streamlit GUI interface
│
├── models/
│   └── q_table.pkl                     # Saved trained RL model
│
└── requirements.txt
```

---

## 🗺️ Data Description

**Dataset:** Generated synthetic Bhubaneswar road network with real landmark names.

Each road (edge) includes:

| Feature     | Description                  |
| ----------- | ---------------------------- |
| `distance`  | Distance in km               |
| `time`      | Estimated travel time (mins) |
| `fuel_cost` | Fuel consumption (liters)    |

**Nodes (locations):**
Master Canteen Square, Ram Mandir Square, KIIT Square, Airport, Kalpana Square, Baramunda, etc.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone or download the project

```bash
git clone https://github.com/<your-username>/delivery-optimizer.git
cd delivery-optimizer
```

### 2️⃣ Create virtual environment & install dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Generate Bhubaneswar dataset

```bash
python utils/graph_generator.py
```

### 4️⃣ Launch GUI

```bash
streamlit run gui/app.py
```

---

## 💻 How It Works

| Mode                       | Description                                                                                   |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| **Graph Algorithm**        | Uses **Dijkstra’s Algorithm** to compute the shortest route between two points.               |
| **Multi-Delivery (TSP)**   | Finds the best visiting order for multiple delivery stops (Travelling Salesman Problem).      |
| **Reinforcement Learning** | Uses **Q-Learning** to train an AI agent that learns optimal routing through trial and error. |

---

## 🧠 Reinforcement Learning Logic

| Concept        | Explanation                                  |
| -------------- | -------------------------------------------- |
| **State (s)**  | Current delivery location                    |
| **Action (a)** | Next location to move to                     |
| **Reward (r)** | Negative of travel cost (distance/time/fuel) |
| **Goal**       | Reach the target while minimizing total cost |

RL Algorithm:
[
Q(s,a) = Q(s,a) + α [r + γ \max Q(s', a') - Q(s,a)]
]

---

## 🧩 Technologies Used

| Component     | Tool / Library                   |
| ------------- | -------------------------------- |
| Language      | Python                           |
| Visualization | Streamlit, Matplotlib, NetworkX  |
| Algorithms    | Dijkstra, TSP, Q-Learning        |
| Environment   | DeliveryRouteEnv (custom)        |
| Data          | Synthetic Bhubaneswar city graph |

---

## 🚀 Output Preview

### 🗺️ Modes

* **Graph Algorithm** → Single route (Dijkstra)
* **Multi-Delivery** → Multiple stops (TSP)
* **Reinforcement Learning** → Learned optimal policy

### 🖼️ GUI Preview

* Select **start** and **destination**
* Choose **metric** (distance/time/fuel)
* Click **Find Route**
* View route visualization on Bhubaneswar map (Graph view)

---

## 📊 Sample Output

```
🚚 Optimal route from Master Canteen Square → KIIT Square (distance):
Master Canteen Square → Ram Mandir Square → Acharya Vihar → Jayadev Vihar → KIIT Square
Total distance: 12.85 km
```

```
🧠 RL Agent Trained (1000 episodes)
Predicted optimal route:
Master Canteen Square → Ram Mandir Square → KIIT Square
Total fuel_cost: 0.97 liters
```

---

## 🏗️ Future Improvements

* Integrate **real map visualization** (OpenStreetMap / Folium)
* Add **live traffic API** for dynamic route optimization
* Support **multiple vehicles**
* Deploy on **Streamlit Cloud / AWS**

---

## 🧑‍💻 Contributors

| Name                   | Role                              |
| ---------------------- | --------------------------------- |
| Sunil Kumar Swain      | AI/ML Developer, Project Lead     |
| College Domain Project | B.Tech (Computer Science / AI-ML) |

---

## 📚 References

* *Artificial Intelligence: A Modern Approach* – Russell & Norvig
* NetworkX Documentation: [https://networkx.org](https://networkx.org)
* Streamlit Documentation: [https://streamlit.io](https://streamlit.io)
* Sutton & Barto – *Reinforcement Learning: An Introduction*

---

## 🏁 Conclusion

This project demonstrates how **graph theory** and **reinforcement learning** can be combined to optimize real-world delivery logistics.
It not only predicts the **shortest** and **most efficient** routes but also showcases how an AI agent can **learn and adapt** to dynamic conditions in a delivery network.

**✅ Project Completed Successfully**
