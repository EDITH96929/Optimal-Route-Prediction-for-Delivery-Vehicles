import streamlit as st, os, json, sys, matplotlib.pyplot as plt, networkx as nx
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.dijkstra import find_optimal_route
from algorithms.tsp_solver import solve_tsp
from rl_agent.environment import DeliveryRouteEnv
from rl_agent.agent import QLearningAgent

def load_graph():
    with open("data/bhubaneswar_graph.json", "r") as f: return json.load(f)

def draw_route(graph, path):
    G = nx.Graph()
    for e in graph["edges"]: G.add_edge(e["from"], e["to"], weight=e["distance"])
    pos = {n:(d["x"],d["y"]) for n,d in graph["locations"].items()}
    fig, ax = plt.subplots(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=600, font_size=8)
    if len(path)>1:
        nx.draw_networkx_edges(G,pos,edgelist=list(zip(path[:-1],path[1:])),width=3,edge_color="red")
    st.pyplot(fig)

st.title("🚚 Optimal Route Prediction (Bhubaneswar)")
graph = load_graph()
locs = list(graph["locations"].keys())
mode = st.sidebar.radio("Mode", ["Graph Algorithm","Multi-Delivery (TSP)","Reinforcement Learning"])
metric = st.sidebar.selectbox("Optimize For",["distance","time","fuel_cost"])
start = st.sidebar.selectbox("Start",locs)
target = st.sidebar.selectbox("Destination",locs)

if mode=="Graph Algorithm":
    if st.button("Find Route"):
        total, path = find_optimal_route(start,target,weight_type=metric)
        st.success("✅ Route Found")
        st.write(" → ".join(path)); st.info(f"Total {metric}: {total:.2f}")
        draw_route(graph,path)
elif mode=="Multi-Delivery (TSP)":
    stops = st.multiselect("Select delivery stops",locs)
    if st.button("Optimize Route"):
        total, route = solve_tsp(stops,weight_type=metric)
        st.success("✅ Optimal Route Found")
        st.write(" → ".join(route)); st.info(f"Total {metric}: {total:.2f}")
        draw_route(graph,route)
else:
    ep = st.slider("Training episodes",100,3000,1000,100)
    if st.button("Train RL Agent"):
        env = DeliveryRouteEnv(start,target,metric); agent = QLearningAgent(env)
        agent.learn(ep); agent.save(); st.success("Agent trained ✅")
    if st.button("Use Trained Agent"):
        env = DeliveryRouteEnv(start,target,metric); agent = QLearningAgent(env)
        agent.load(); path,cost = agent.get_optimal_route(start,target)
        st.success("✅ Predicted Route"); st.write(" → ".join(path)); st.info(f"Total {metric}: {cost:.2f}")
        draw_route(graph,path)
