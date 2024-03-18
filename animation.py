import osmnx as ox
import random
import heapq
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

place_name = "Capital Federal, Buenos Aires"
G = ox.graph_from_place(place_name, network_type="drive")

for edge in G.edges:
    maxspeed = 40
    if "maxspeed" in G.edges[edge]:
        maxspeed_value = G.edges[edge]["maxspeed"]
        if isinstance(maxspeed_value, list):
            speeds = [re.search(r'\d+', str(speed)).group() for speed in maxspeed_value]
            maxspeed = min(map(int, speeds))
        elif isinstance(maxspeed_value, str):
            maxspeed = int(re.search(r'\d+', maxspeed_value).group())
    G.edges[edge]["maxspeed"] = maxspeed
    G.edges[edge]["weight"] = G.edges[edge]["length"] / maxspeed

for node in G.nodes:
    G.nodes[node]["size"] = 0
for edge in G.edges:
    G.edges[edge]["color"] = "#d36206"


def style_unvisited_edge(edge):        
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 0.2
    G.edges[edge]["linewidth"] = 0.5

def style_visited_edge(edge):
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_active_edge(edge):
    G.edges[edge]["color"] = '#e8a900'
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_path_edge(edge):
    G.edges[edge]["color"] = "white"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def plot_graph():
    fig, ax = ox.plot_graph(
        G,
        node_size =  [ G.nodes[node]["size"] for node in G.nodes ],
        edge_color = [ G.edges[edge].get("color", "#d36206") for edge in G.edges ],
        edge_alpha = [ G.edges[edge].get("alpha", 0.2) for edge in G.edges ],
        edge_linewidth = [ G.edges[edge].get("linewidth", 0.5) for edge in G.edges ],
        node_color = "white",
        bgcolor = "#18080e",
        show=False
    )
    return fig, ax
frames_folder = "frames"

def dijkstra(orig, dest):
    fig, ax = plot_graph()
    def animate():
        for edge in G.edges:
            style_unvisited_edge(edge)
        for node in G.nodes:
            G.nodes[node]["visited"] = False
            G.nodes[node]["distance"] = float("inf")
            G.nodes[node]["previous"] = None
            G.nodes[node]["size"] = 0
        G.nodes[orig]["distance"] = 0
        G.nodes[orig]["size"] = 50
        G.nodes[dest]["size"] = 50
        pq = [(0, orig)]
        step = 0
        while pq:
            _, node = heapq.heappop(pq)
            if node == dest:
                break
            if G.nodes[node]["visited"]: continue
            G.nodes[node]["visited"] = True
            for edge in G.out_edges(node):
                style_visited_edge((edge[0], edge[1], 0))
                neighbor = edge[1]
                weight = G.edges[(edge[0], edge[1], 0)]["weight"]
                if G.nodes[neighbor]["distance"] > G.nodes[node]["distance"] + weight:
                    G.nodes[neighbor]["distance"] = G.nodes[node]["distance"] + weight
                    G.nodes[neighbor]["previous"] = node
                    heapq.heappush(pq, (G.nodes[neighbor]["distance"], neighbor))
                    for edge2 in G.out_edges(neighbor):
                        style_active_edge((edge2[0], edge2[1], 0))
            step += 1
            plot_graph()
            filename = os.path.join(frames_folder, f'frame_{step:03d}.png')
            plt.savefig(filename, dpi=100)
            plt.close()

    animate()

if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

start = random.choice(list(G.nodes))
end = random.choice(list(G.nodes))
print("Start = " + str(start))
print("End = " + str(end))
dijkstra(start, end)