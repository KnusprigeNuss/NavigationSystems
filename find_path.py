import heapq

import pandas as pd
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.pyplot as plt
import folium
arclist = pd.read_csv('data/arclist.txt', sep='\s+', names=['end', 'time', 'distance', 'speedlimit', 'clazz', 'flags'])
nodelist = pd.read_csv('data/nodelist.txt', sep='\s+', names=['adjacent'])
nodepl = pd.read_csv('data/nodepl.txt', sep='\s+', names=['long', 'lat'])

dummy_arclist = pd.DataFrame({'end': [0], 'time': [0], 'distance': [0], 'speedlimit': [0], 'clazz': [0], 'flags': [0]})
dummy_nodelist = pd.DataFrame({'adjacent': [0]})
dummy_nodepl = pd.DataFrame({'long': [0.0], 'lat': [0.0]})

arclist = pd.concat([dummy_arclist, arclist], ignore_index=True)
nodelist = pd.concat([dummy_nodelist, nodelist], ignore_index=True)
nodepl = pd.concat([dummy_nodepl, nodepl], ignore_index=True)
# our closest node is 979
start = 979


def init_graph():
    graph = []
    for i in range(len(nodelist)-1):
        graph.append( {"node": i, "cost": float('inf'), "predecessor": None,"visited": False})
    graph[start]['cost'] = 0
    #dummy line
    graph[0]['visited'] = True

    return graph
def distance_update(i,neighbor,node_min_cost,graph,distances):
    alternative_distance = graph[node_min_cost]['cost'] + distances[i]
    if alternative_distance < graph[neighbor]['cost']:
        graph[neighbor]['cost'] = alternative_distance
        graph[neighbor]['predecessor'] = node_min_cost
    return graph
def dijkstra(start):
    graph = init_graph()
    iterations = 1
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
    for i in range(edges_node, edges_next):
        neighbors.append(arclist['end'][i])
        distances.append(arclist['distance'][i])
        times.append(arclist['time'][i])
    return neighbors, distances, times

def find_path(graph, start, end):
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = graph[current_node]['predecessor']
    path.reverse()
    return path




graph = dijkstra(start)
best_paths = []
best_paths.append(find_path(graph,start,9328))
best_paths.append(find_path(graph,start,6031))
best_paths.append(find_path(graph,start,8543))
m = folium.Map(location=(nodepl.loc[start, "long"], nodepl.loc[start, "lat"]), zoom_start=15)

for best_path in best_paths:
    coordinates = [(nodepl.loc[i, "long"], nodepl.loc[i, "lat"]) for i in best_path]
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)
m.save("map.html")







