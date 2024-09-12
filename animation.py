import math
import osmnx as ox
import random
import heapq
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import networkx

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
        bgcolor = "#000000",
        show=False
    )
    return fig, ax
frames_folder = "frames"

def dijkstra(orig, dest, start_frame=0):
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
            if step >= start_frame:
                plot_graph()
                filename = os.path.join(frames_folder, f'frame_{step:03d}.png')
                plt.savefig(filename, dpi=100)
                plt.close()
        return step
    animate()

def a_star(orig, dest, start_frame=0):
    frames_folder = "frames"
    step = 0
    
    def distance(node1, node2):
        x1, y1 = G.nodes[node1]["x"], G.nodes[node1]["y"]
        x2, y2 = G.nodes[node2]["x"], G.nodes[node2]["y"]
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    for node in G.nodes:
        G.nodes[node]["previous"] = None
        G.nodes[node]["size"] = 0
        G.nodes[node]["g_score"] = float("inf")
        G.nodes[node]["f_score"] = float("inf")
    
    for edge in G.edges:
        style_unvisited_edge(edge)
    
    G.nodes[orig]["size"] = 50
    G.nodes[dest]["size"] = 50
    G.nodes[orig]["g_score"] = 0
    G.nodes[orig]["f_score"] = distance(orig, dest)
    pq = [(G.nodes[orig]["f_score"], orig)]
    
    while pq:
        if step >= start_frame:
            plot_graph()
            filename = os.path.join(frames_folder, f'frame_{step:03d}.png')
            plt.savefig(filename, dpi=100)
            plt.close()
        _, node = heapq.heappop(pq)
        if node == dest:
            break
        for edge in G.out_edges(node):
            style_visited_edge((edge[0], edge[1], 0))
            neighbor = edge[1]
            tentative_g_score = G.nodes[node]["g_score"] + distance(node, neighbor)
            if tentative_g_score < G.nodes[neighbor]["g_score"]:
                G.nodes[neighbor]["previous"] = node
                G.nodes[neighbor]["g_score"] = tentative_g_score
                G.nodes[neighbor]["f_score"] = tentative_g_score + distance(neighbor, dest)
                heapq.heappush(pq, (G.nodes[neighbor]["f_score"], neighbor))
                for edge2 in G.out_edges(neighbor):
                    style_active_edge((edge2[0], edge2[1], 0))
        step += 1

if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)


choice = input("1: Random start and end points\n2: Custom start and end points\n> ")
algorithm_choice = input("Choose algorithm (1: Dijkstra, 2: A*): ")

if algorithm_choice == '1':
    algorithm = dijkstra
elif algorithm_choice == '2':
    algorithm = a_star
else:
    print("Invalid choice")
    exit()

if choice == '1':
    start = random.choice(list(G.nodes))
    end = random.choice(list(G.nodes))
    print("Start = " + str(start))
    print("End = " + str(end))
    restartFrame = input("Input frame to start animation from: ")
    algorithm(start, end, int(restartFrame))
elif choice == '2':
    start = input("Start Point: ")
    end = input("End Point: ")
    print("Start = " + str(start))
    print("End = " + str(end)) 
    restartFrame = input("Input frame to start animation from: ")
    algorithm(int(start), int(end), int(restartFrame))
else:
    print("Invalid choice")
    exit()