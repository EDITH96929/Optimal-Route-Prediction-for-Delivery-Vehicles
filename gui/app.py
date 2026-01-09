import streamlit as st
import json, os, sys, folium
from streamlit_folium import st_folium

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.dijkstra import find_optimal_route
from algorithms.tsp_solver import solve_tsp
from rl_agent.environment import DeliveryRouteEnv
from rl_agent.agent import QLearningAgent


# ---------------- Helper Functions ---------------- #

def load_graph():
    """Load Bhubaneswar graph."""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "bhubaneswar_graph.json")
    with open(path, "r") as f:
        return json.load(f)

def get_center(graph):
    """Get map center coordinates."""
    xs = [v["y"] for v in graph["locations"].values()]
    ys = [v["x"] for v in graph["locations"].values()]
    return sum(xs) / len(xs), sum(ys) / len(ys)

@st.cache_data(show_spinner=False)
def generate_map_html(graph, path):
    """Render Folium map and return HTML once (cached)."""
    center_lat, center_lon = get_center(graph)
    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="CartoDB Positron")

    # Add location markers + labels
    for name, data in graph["locations"].items():
        if path:
            if name == path[0]:
                color, label = "green", f"🏁 START: {name}"
            elif name == path[-1]:
                color, label = "red", f"🎯 DESTINATION: {name}"
            else:
                color, label = "blue", name
        else:
            color, label = "blue", name

        folium.CircleMarker(
            [data["y"], data["x"]],
            radius=7,
            color=color,
            fill=True,
            fill_opacity=1,
            tooltip=label,
        ).add_to(fmap)

        # small text labels beside nodes
        folium.map.Marker(
            [data["y"], data["x"]],
            icon=folium.DivIcon(
                html=f"<div style='font-size:11px;color:#111;font-weight:bold;text-align:center;'>{name}</div>"
            ),
        ).add_to(fmap)

    # Draw route line
    if path and len(path) > 1:
        coords = [
            [graph["locations"][p]["y"], graph["locations"][p]["x"]]
            for p in path if p in graph["locations"]
        ]
        folium.PolyLine(coords, color="orange", weight=6, opacity=0.85).add_to(fmap)

    # Return raw HTML (cached)
    return fmap._repr_html_()


# ---------------- Streamlit App ---------------- #

st.set_page_config(page_title="Optimal Route Prediction", page_icon="🚚", layout="wide")

st.title("🚚 Optimal Route Prediction – Bhubaneswar City")
st.markdown("""
### Domain Project | AI & Machine Learning
Predict **fastest** and **most fuel-efficient** delivery routes using Graph Algorithms & Reinforcement Learning.
""")

graph = load_graph()
locations = list(graph["locations"].keys())

# Sidebar controls
st.sidebar.header("⚙️ Controls")
mode = st.sidebar.radio("Mode", ["Graph Algorithm", "Multi-Delivery (TSP)", "Reinforcement Learning"])
metric = st.sidebar.selectbox("Optimize For", ["distance", "time", "fuel_cost"])
start = st.sidebar.selectbox("Start Location", locations)
target = st.sidebar.selectbox("Destination", locations)

# Persistent session state
if "path" not in st.session_state:
    st.session_state.path = []
if "info" not in st.session_state:
    st.session_state.info = ""
if "map_html" not in st.session_state:
    st.session_state.map_html = None

st.divider()

# ---------------- MODE LOGIC ---------------- #

if mode == "Graph Algorithm":
    st.subheader("📈 Shortest Path (Dijkstra Algorithm)")
    if st.button("Find Route"):
        with st.spinner("Calculating optimal route..."):
            total, path = find_optimal_route(start, target, weight_type=metric)

        if not path or len(path) < 2:
            st.error("⚠️ No valid route found between these locations.")
            st.session_state.map_html = None
        else:
            st.success("✅ Route Found")
            st.session_state.path = path
            st.session_state.info = f"Total {metric}: {total:.2f}"
            st.session_state.map_html = generate_map_html(graph, path)

elif mode == "Multi-Delivery (TSP)":
    st.subheader("🗺️ Multi-Stop Route Optimization")
    stops = st.multiselect("Select delivery stops (2–6 recommended)", locations)
    if st.button("Compute Optimal Route"):
        if len(stops) < 2:
            st.warning("Please select at least 2 stops.")
        else:
            with st.spinner("Computing optimal route..."):
                total, route = solve_tsp(stops, weight_type=metric)
            if not route:
                st.error("⚠️ Could not find a connected route for selected stops.")
            else:
                st.success("✅ Multi-stop route generated.")
                st.session_state.path = route
                st.session_state.info = f"Total {metric}: {total:.2f}"
                st.session_state.map_html = generate_map_html(graph, route)

elif mode == "Reinforcement Learning":
    st.subheader("🧠 AI Route Optimization (Q-Learning)")
    episodes = st.slider("Training Episodes", 100, 3000, 1000, 100)
    if st.button("Train RL Agent"):
        with st.spinner("Training RL agent... please wait ⏳"):
            env = DeliveryRouteEnv(start, target, weight_type=metric)
            agent = QLearningAgent(env)
            agent.learn(episodes)
            agent.save()
        st.success(f"🤖 Trained for {episodes} episodes and saved!")

    if st.button("Use Trained RL Agent"):
        if not os.path.exists("models/q_table.pkl"):
            st.error("❌ No trained model found. Train first.")
        else:
            with st.spinner("Predicting optimal route..."):
                env = DeliveryRouteEnv(start, target, weight_type=metric)
                agent = QLearningAgent(env)
                agent.load()
                path, cost = agent.get_optimal_route(start, target)
            if not path:
                st.error("⚠️ RL agent could not find a route.")
            else:
                st.success("🚀 RL Agent Predicted Route Successfully!")
                st.session_state.path = path
                st.session_state.info = f"Total {metric}: {cost:.2f}"
                st.session_state.map_html = generate_map_html(graph, path)

# ---------------- DISPLAY ---------------- #

if st.session_state.path:
    st.markdown(f"**Path:** {' → '.join(st.session_state.path)}")
if st.session_state.info:
    st.info(st.session_state.info)

# Render cached map HTML (NO FLICKER)
if st.session_state.map_html:
    st.components.v1.html(st.session_state.map_html, height=600, width=1100, scrolling=False)

st.markdown("---")
st.caption("Built with ❤️ using Python • Streamlit • Folium • Reinforcement Learning")
