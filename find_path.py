import heapq

import pandas as pd
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.pyplot as plt

arclist = pd.read_csv('data/arclist.txt', sep='\\s+', names=['end', 'time', 'distance', 'speedlimit', 'clazz', 'flags'])
nodelist = pd.read_csv('data/nodelist.txt', sep='\\s+', names=['adjacent'])
nodepl = pd.read_csv('data/nodepl.txt', sep='\\s+', names=['long', 'lat'])

# our closest node is 979
start = 979-1


def init_graph():
    graph = []
    for i in range(len(nodelist)-1):
        graph.append( {"node": i, "cost": float('inf'), "predecessor": None,"visited": False})
    graph[start]['cost'] = 0

    return graph
def distance_update(i,neighbor,node_min_cost,graph,distances):
    alternative_distance = graph[node_min_cost]['cost'] + distances[i]
    if alternative_distance < graph[neighbor]['cost']:
        graph[neighbor]['cost'] = alternative_distance
        graph[neighbor]['predecessor'] = node_min_cost
    return graph
def dijkstra(start):
    graph = init_graph()
    iterations = 0
    while iterations != len(graph):
        #TODO
        not_visited_nodes = [node for node in graph if not node['visited']]
        not_visited_node_ids = [node['node'] for node in not_visited_nodes]
        print(iterations)
        node_min_cost = min(not_visited_nodes, key=lambda x: x['cost'])["node"]
        graph[node_min_cost]['visited'] = True

        neighbors, distances, times = getNeighbors(node_min_cost)
        for i,neighbor in enumerate(neighbors):
            if neighbor in not_visited_node_ids:
                graph = distance_update(i,neighbor,node_min_cost,graph,distances)
        iterations+=1
    return graph

def getNeighbors(node):
    edges_node = nodelist['adjacent'][node]
    edges_next = nodelist['adjacent'][node+1]
    neighbors = []
    distances = []
    times = []
    for i in range(edges_node-1, edges_next-1):
        neighbors.append(arclist['end'][i])
        distances.append(arclist['distance'][i])
        times.append(arclist['time'][i])
    return neighbors, distances, times




dijkstra(start)






